"""
Record video and trigger events from video using a FLIR Blackfly S camera.
"""

import sys
import os
import time
import cv2
import numpy as np
import PySpin
from typing import Dict, List, Optional, Tuple
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QThread, pyqtSignal, Qt, QObject

# --- Configuration ---
FOURCC_CODEC = cv2.VideoWriter_fourcc(*'MP4V')  # Codec for AVI files. 'MP4V' for .mp4
RECORDING_FPS = 60  # Fallback FPS if camera node is unreadable
DEFAULT_BLACK_THRESHOLD = 128  # Trigger sound when average pixel intensity is less than this
DEFAULT_MINIMUM_AREA = 4000  # Minimum area of the largest contour to consider it significant

class VideoThread(QThread):
    """
    A QThread subclass for handling PySpin video capture and processing in a separate thread.
    """
    camera_error_signal = pyqtSignal(str)
    frame_processed = pyqtSignal(float, np.ndarray, tuple, object)

    def __init__(self, camera_index=0, mode='grayscale', tracking=False, debug=False):
        super().__init__()
        self.camera_index = camera_index
        self._run_flag = True
        
        # PySpin components
        self.system = None
        self.cam_list = None
        self.cam = None
        
        self.out = None 
        self.fps = None
        self.mode = mode
        self.tracking = tracking
        self.recording_status = False  
        self.filepath = None  
        self.threshold = DEFAULT_BLACK_THRESHOLD  
        self.minarea = DEFAULT_MINIMUM_AREA  

        # MASK masking parameters
        self.mask_enabled = False  
        self.mask_coords = None  

        # Store tracking
        self.timestamps = []
        self.points = []  

        self.debug = debug
        self.initialize_camera()

    def set_threshold(self, threshold):
        self.threshold = threshold
        
    def set_minarea(self, minarea):
        self.minarea = minarea

    def set_circular_mask(self, coords):
        if len(coords) != 3:
            raise ValueError("Circular mask requires exactly 3 coordinates: [center_x, center_y, radius]")
        self.mask_coords = coords
        self.mask_enabled = True
        if self.debug:
            print(f"Circular MASK set: center ({coords[0]}, {coords[1]}), radius {coords[2]}")

    def set_rectangular_mask(self, coords):
        if len(coords) != 4:
            raise ValueError("Rectangular mask requires exactly 4 coordinates: [x1, y1, x2, y2]")
        self.mask_coords = coords
        self.mask_enabled = True
        if self.debug:
            print(f"Rectangular MASK set: ({coords[0]}, {coords[1]}) to ({coords[2]}, {coords[3]})")

    def set_rectangular_mask_from_center(self, center_x, center_y, width, height):
        half_width = width // 2
        half_height = height // 2
        x1 = max(0, center_x - half_width)
        y1 = max(0, center_y - half_height)
        x2 = center_x + half_width
        y2 = center_y + half_height
        self.set_rectangular_mask([x1, y1, x2, y2])

    def disable_mask(self):
        self.mask_enabled = False
        self.mask_coords = None
        if self.debug:
            print("MASK masking disabled")

    def get_mask(self):
        if not self.mask_enabled or self.mask_coords is None:
            return None
        
        if len(self.mask_coords) == 3:
            center_x, center_y, radius = self.mask_coords
            return {
                'type': 'circular', 'coords': self.mask_coords,
                'center_x': center_x, 'center_y': center_y,
                'radius': radius, 'enabled': self.mask_enabled
            }
        elif len(self.mask_coords) == 4:
            x1, y1, x2, y2 = self.mask_coords
            return {
                'type': 'rectangular', 'coords': self.mask_coords,
                'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'enabled': self.mask_enabled
            }
        return None

    def set_mode(self, mode):
        if mode not in ['grayscale', 'binary']:
            raise ValueError("Mode must be 'grayscale' or 'binary'.")
        self.mode = mode

    def store_tracking_data(self, timestamp, points):
        if self.tracking:
            self.timestamps.append(timestamp)
            while len(self.points) < len(points):
                self.points.append([])
            for i, point in enumerate(points):
                self.points[i].append(point)
                
    def initialize_camera(self):
        try:
            self.system = PySpin.System.GetInstance()
            self.cam_list = self.system.GetCameras()
            
            if self.cam_list.GetSize() == 0:
                self.camera_error_signal.emit("No FLIR cameras detected.")
                self.cam_list.Clear()
                self.system.ReleaseInstance()
                self._run_flag = False
                return

            # Note: camera_index will map directly to camera enumeration
            self.cam = self.cam_list.GetByIndex(self.camera_index)
            self.cam.Init()

            # Set to continuous acquisition mode
            nodemap = self.cam.GetNodeMap()
            node_acq_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
            if PySpin.IsAvailable(node_acq_mode) and PySpin.IsWritable(node_acq_mode):
                node_acq_mode_continuous = node_acq_mode.GetEntryByName('Continuous')
                if PySpin.IsAvailable(node_acq_mode_continuous) and PySpin.IsReadable(node_acq_mode_continuous):
                    node_acq_mode.SetIntValue(node_acq_mode_continuous.GetValue())

        except PySpin.SpinnakerException as e:
            self.camera_error_signal.emit(f"Spinnaker SDK initialization error: {e}")
            self._run_flag = False

    def start_recording(self, filepath=None):
        if filepath is not None:
            self.filepath = filepath
            self.initialize_video_writer(self.filepath)
            self.recording_status = True
            print(f"Video recording started: {self.filepath}")
        else:
            print("Video recording not started: No output file set or writer not initialized.")
        
    def stop_recording(self):
        self.recording_status = False
        print("Video recording stopped.")
            
    def initialize_video_writer(self, filepath):
        dir_path = os.path.dirname(self.filepath)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            # Query the Blackfly S for width/height
            frame_width = self.cam.Width.GetValue()
            frame_height = self.cam.Height.GetValue()

            self.out = cv2.VideoWriter(self.filepath, FOURCC_CODEC, self.fps,
                                        (frame_width, frame_height))
            if not self.out.isOpened():
                raise IOError(f"Could not open video writer for {self.filepath}.")
            print(f"Recording video to {self.filepath} at {self.fps} FPS, resolution {frame_width}x{frame_height}")
        except Exception as e:
            self.camera_error_signal.emit(f"Error initializing video writer: {e}")
            self.stop()
        
    def run(self):
        # Retrieve framerate from the camera
        try:
            nodemap = self.cam.GetNodeMap()
            node_frame_rate = PySpin.CFloatPtr(nodemap.GetNode('AcquisitionFrameRate'))
            if PySpin.IsAvailable(node_frame_rate) and PySpin.IsReadable(node_frame_rate):
                self.fps = node_frame_rate.GetValue()
            else:
                self.fps = RECORDING_FPS
                print('Warning: Unable to read valid FPS node. Using default:', self.fps)
        except PySpin.SpinnakerException:
            self.fps = RECORDING_FPS
            print('Warning: FPS node exception. Using default:', self.fps)
            
        print('Camera reported FPS:', self.fps)

        try:
            self.cam.BeginAcquisition()
        except PySpin.SpinnakerException as e:
            self.camera_error_signal.emit(f"Failed to begin acquisition: {e}")
            self._run_flag = False

        while self._run_flag:
            try:
                # 1000ms timeout for frame grabbing
                image_result = self.cam.GetNextImage(1000)
                
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                    image_result.Release()
                    continue

                timestamp = time.time() 

                # Convert PySpin Image to OpenCV compatible BGR array
                image_converted = image_result.Convert(PySpin.PixelFormat_BGR8, PySpin.HQ_LINEAR)
                frame = image_converted.GetNDArray()
                
                # Immediately release memory to PySpin internal buffers
                image_result.Release()

                if self.recording_status and self.out is not None:
                    self.out.write(frame)

                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                processed_frame, points, contour = self.process_frame(gray_frame)

                self.store_tracking_data(timestamp, points)
                self.frame_processed.emit(timestamp, processed_frame, points, contour)

            except PySpin.SpinnakerException as e:
                self.camera_error_signal.emit(f"Spinnaker read exception: {e}")
                self._run_flag = False

        self._cleanup_resources()

    def _cleanup_resources(self):
        """Strictly ordered PySpin resource release to prevent crashes."""
        if self.out:
            self.out.release()
            
        if self.cam is not None:
            try:
                if self.cam.IsInitialized():
                    self.cam.EndAcquisition()
                    self.cam.DeInit()
            except PySpin.SpinnakerException:
                pass
            del self.cam
            
        if self.cam_list is not None:
            self.cam_list.Clear()
            del self.cam_list
            
        if self.system is not None:
            self.system.ReleaseInstance()
            del self.system
            
        print("Video thread stopped and PySpin resources released.")

    def apply_circular_mask(self, frame):
        if not self.mask_enabled or self.mask_coords is None or len(self.mask_coords) != 3:
            return frame
        masked_frame = frame.copy()
        height, width = frame.shape
        center_x, center_y, radius = self.mask_coords
        
        if radius <= 0:
            return frame
            
        y_coords, x_coords = np.ogrid[:height, :width]
        distance_from_center = np.sqrt((x_coords - center_x)**2 + (y_coords - center_y)**2)
        mask_outside_circle = distance_from_center > radius
        masked_frame[mask_outside_circle] = 255
        return masked_frame

    def apply_mask(self, frame):
        if not self.mask_enabled or self.mask_coords is None:
            return frame
            
        if len(self.mask_coords) == 3:
            return self.apply_circular_mask(frame)
        elif len(self.mask_coords) == 4:
            return self.apply_rectangular_mask(frame)
        return frame

    def apply_rectangular_mask(self, frame):
        if not self.mask_enabled or self.mask_coords is None or len(self.mask_coords) != 4:
            return frame
            
        masked_frame = frame.copy()
        height, width = frame.shape
        x1, y1, x2, y2 = self.mask_coords
        
        x1, y1 = max(0, x1), max(0, y1)
        x2 = min(width, x2) if x2 is not None else width
        y2 = min(height, y2) if y2 is not None else height
        
        if x1 >= x2 or y1 >= y2:
            return frame
            
        mask = np.ones_like(frame) * 255
        mask[y1:y2, x1:x2] = 0
        masked_frame[mask == 255] = 255
        return masked_frame

    def process_frame(self, frame):
        if not self.tracking:
            return (frame, (), None)
        
        masked_frame = self.apply_mask(frame)
        max_value = 255 
        inverted_frame = cv2.bitwise_not(masked_frame)
        
        ret, binary_frame = cv2.threshold(inverted_frame, max_value-self.threshold,
                                          max_value, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(binary_frame, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        centroid = (-1,-1)  
        largest_area = 0
        largest_contour = None

        if contours:
            for indc, cnt in enumerate(contours):
                area = cv2.contourArea(cnt)
                if area > largest_area:
                    largest_area = area
                    largest_contour = cnt
            if largest_contour is not None and largest_area > self.minarea:
                mom = cv2.moments(largest_contour)
                if mom["m00"] != 0:
                    cX = int(mom["m10"] / mom["m00"])
                    cY = int(mom["m01"] / mom["m00"])
                    centroid = (cX, cY)
        points = (centroid,) 
        
        if self.mode == 'grayscale':
            processed_frame = frame
        elif self.mode == 'binary':
            processed_frame = cv2.bitwise_not(binary_frame)
            
        if self.debug:
            print(f"Centroid: {centroid} \t Largest area: {largest_area}")
        return (processed_frame, points, largest_contour)
    
    def append_to_file(self, h5file):
        if len(self.timestamps) == 0:
            raise UserWarning('No tracking data found. Make sure tracking was enabled (tracking=True).')
        
        try:
            tracking_group = h5file.create_group('/videoTracking')
            tracking_group.create_dataset('timestamps', data=np.array(self.timestamps))
            
            if len(self.points) > 0 and len(self.points[0]) > 0:
                centroid_x = np.array([point[0] for point in self.points[0]])
                centroid_y = np.array([point[1] for point in self.points[0]])
                
                tracking_group.create_dataset('centroid_x', data=centroid_x)
                tracking_group.create_dataset('centroid_y', data=centroid_y)
            else:
                tracking_group.create_dataset('centroid_x', data=np.array([]))
                tracking_group.create_dataset('centroid_y', data=np.array([]))
            
            return tracking_group
            
        except Exception as e:
            raise RuntimeError(f'Error saving video tracking data to file: {str(e)}')
        
    def stop(self):
        self._run_flag = False
        self.wait()


class VideoInterface(QObject):
    """
    Interface between video events and state machine.
    """
    def __init__(self,
                 video_thread: VideoThread,
                 zones: Optional[Dict[str, Tuple[str, tuple]]] = None,
                 event_offset: int = 0,
                 debug: bool = False,
                 parent: Optional[QObject] = None):
        super().__init__(parent)
        
        self.video_thread = video_thread
        self.debug = debug
        self.zones = {}
        self.previous_zone_states = {}  
        self.state_machine = None
        self.event_mapping: Dict[str, int] = {}
        
        if zones is not None:
            for zone_name, (zone_type, coords) in zones.items():
                self.add_zone(zone_name, zone_type, coords)
        
        self.events = {}
        event_index = event_offset  
        for zone_name in self.zones.keys():
            self.events[f'{zone_name}in'] = event_index
            event_index += 1
            self.events[f'{zone_name}out'] = event_index
            event_index += 1
        
        if self.video_thread is not None:
            self.video_thread.frame_processed.connect(self.on_frame_processed)
            
        if self.debug:
            print(f"VideoInterface initialized with {len(self.zones)} zones")
            print(f"Events: {self.events}")
    
    def add_zone(self, zone_name: str, zone_type: str, coords: tuple):
        if zone_type not in ['circular', 'rectangular']:
            raise ValueError(f"Invalid zone type '{zone_type}'. Must be 'circular' or 'rectangular'")
        
        if zone_type == 'circular':
            if len(coords) != 3:
                raise ValueError(f"Circular zone requires 3 coordinates (center_x, center_y, radius), got {len(coords)}")
        elif zone_type == 'rectangular':
            if len(coords) != 4:
                raise ValueError(f"Rectangular zone requires 4 coordinates (x1, y1, x2, y2), got {len(coords)}")
        
        self.zones[zone_name] = {'type': zone_type, 'coords': coords}
        if zone_name not in self.previous_zone_states:
            self.previous_zone_states[zone_name] = False
        
        if self.debug:
            print(f"Added {zone_type} zone '{zone_name}' with coords {coords}")
    
    def remove_zone(self, zone_name: str):
        if zone_name in self.zones:
            del self.zones[zone_name]
            del self.previous_zone_states[zone_name]
            if self.debug:
                print(f"Removed zone '{zone_name}'")
    
    def get_events(self) -> Dict[str, int]:
        return self.events.copy()
    
    def connect_state_machine(self, state_machine):
        self.state_machine = state_machine
        self.event_mapping = self.get_events()
        if self.debug:
            print(f"Connected to state machine with {len(self.event_mapping)} events")
    
    def disconnect_state_machine(self):
        self.state_machine = None
        self.event_mapping.clear()
        if self.debug:
            print("Disconnected from state machine")
    
    def point_in_zone(self, point: Tuple[int, int], zone_name: str) -> bool:
        if zone_name not in self.zones:
            return False
        
        zone = self.zones[zone_name]
        x, y = point
        
        if x < 0 or y < 0:
            return False
        
        if zone['type'] == 'circular':
            center_x, center_y, radius = zone['coords']
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            return distance <= radius
        elif zone['type'] == 'rectangular':
            x1, y1, x2, y2 = zone['coords']
            return x1 <= x <= x2 and y1 <= y <= y2
        return False
    
    def on_frame_processed(self, timestamp: float, frame: np.ndarray, points: Tuple):
        if not self.state_machine or not self.state_machine.is_active:
            return
        
        if not points or len(points) == 0:
            return
        
        tracked_point = points[0]
        
        for zone_name in self.zones.keys():
            is_in_zone = self.point_in_zone(tracked_point, zone_name)
            was_in_zone = self.previous_zone_states[zone_name]
            
            if is_in_zone and not was_in_zone:
                event_name = f'{zone_name}in'
                if event_name in self.event_mapping:
                    event_index = self.event_mapping[event_name]
                    self.state_machine.process_input(event_index)
            
            elif not is_in_zone and was_in_zone:
                event_name = f'{zone_name}out'
                if event_name in self.event_mapping:
                    event_index = self.event_mapping[event_name]
                    self.state_machine.process_input(event_index)
            
            self.previous_zone_states[zone_name] = is_in_zone
    
    def get_zone_info(self, zone_name: str) -> Optional[Dict]:
        return self.zones.get(zone_name)
    
    def get_all_zones(self) -> Dict[str, Dict]:
        return self.zones.copy()
    
    def is_point_in_any_zone(self, point: Tuple[int, int]) -> List[str]:
        zones_containing_point = []
        for zone_name in self.zones.keys():
            if self.point_in_zone(point, zone_name):
                zones_containing_point.append(zone_name)
        return zones_containing_point

class VideoThreadBlackDetect(VideoThread):
    """
    A specialized video thread that detects black screens and triggers a signal.
    """
    black_screen_detected_signal = pyqtSignal()
    
    def __init__(self, camera_index=0, mode='grayscale', tracking=False, debug=False, threshold=DEFAULT_BLACK_THRESHOLD):
        super().__init__(camera_index, mode, tracking, debug)
        self.black_threshold = threshold

    def process_frame(self, frame):
        avg_intensity = np.mean(frame)
        if avg_intensity < self.black_threshold:
            self.black_screen_detected_signal.emit()
        return (frame, (), None) 

def count_video_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return 0
    
    frame_count = 0
    while True:
        ret, _ = cap.read()
        if not ret:
            break
        frame_count += 1
    
    cap.release()
    return frame_count