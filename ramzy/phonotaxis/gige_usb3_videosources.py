import cv2
import numpy as np
from typing import Optional, Tuple, Union
from phonotaxis.videosource import VideoSource


class PySpinVideoSource(VideoSource):
    """PySpin (FLIR Spinnaker) video source implementation for USB3/GigE cameras."""
    
    def __init__(self, camera_index: int = 0):
        # Lazy import to prevent crash if PySpin SDK is not installed
        try:
            global PySpin
            import PySpin
        except ImportError as e:
            raise ImportError(
                "PySpin module not found. Please install the FLIR Spinnaker SDK "
                "and its corresponding Python bindings."
            ) from e

        self.camera_index = camera_index
        self.system: Optional[PySpin.System] = None
        self.cam_list: Optional[PySpin.CameraList] = None
        self.cam: Optional[PySpin.Camera] = None
        self._fps: float = 30.0
        self._width: int = 0
        self._height: int = 0

    def open(self) -> bool:
        if self.cam is not None:
            return True
            
        try:
            self.system = PySpin.System.GetInstance()
            self.cam_list = self.system.GetCameras()
            
            if self.cam_list.GetSize() <= self.camera_index:
                self.release()
                return False
                
            self.cam = self.cam_list.GetByIndex(self.camera_index)
            self.cam.Init()
            
            nodemap = self.cam.GetNodeMap()
            handling_mode = PySpin.CEnumerationPtr(nodemap.GetNode("AcquisitionMode"))
            if PySpin.IsAvailable(handling_mode) and PySpin.IsWritable(handling_mode):
                mode_continuous = handling_mode.GetEntryByName("Continuous")
                if PySpin.IsAvailable(mode_continuous) and PySpin.IsReadable(mode_continuous):
                    handling_mode.SetIntValue(mode_continuous.GetValue())
            
            self._width = int(PySpin.CIntegerPtr(nodemap.GetNode("Width")).GetValue())
            self._height = int(PySpin.CIntegerPtr(nodemap.GetNode("Height")).GetValue())
            
            fps_node = PySpin.CFloatPtr(nodemap.GetNode("AcquisitionFrameRate"))
            if PySpin.IsAvailable(fps_node) and PySpin.IsReadable(fps_node):
                self._fps = fps_node.GetValue()

            self.cam.BeginAcquisition()
            return True
        except PySpin.SpinnakerException:
            self.release()
            return False

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if self.cam is None:
            return False, None
            
        try:
            image_result = self.cam.GetNextImage(1000)
            if image_result.IsIncomplete():
                image_result.Release()
                return False, None
                
            converted_image = image_result.Convert(PySpin.PixelFormat_BGR8, PySpin.HQ_LINEAR)
            frame = converted_image.GetNDArray().copy()
            
            image_result.Release()
            return True, frame
        except PySpin.SpinnakerException:
            return False, None

    def release(self) -> None:
        try:
            if self.cam is not None:
                if self.cam.IsStreaming():
                    self.cam.EndAcquisition()
                self.cam.DeInit()
                self.cam = None
            if self.cam_list is not None:
                self.cam_list.Clear()
                self.cam_list = None
            if self.system is not None:
                self.system.ReleaseInstance()
                self.system = None
        except PySpin.SpinnakerException:
            pass

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def frame_width(self) -> int:
        return self._width

    @property
    def frame_height(self) -> int:
        return self._height


class AravisVideoSource(VideoSource):
    """Aravis (glib-gi) video source implementation for generic GigE/USB3 Vision cameras."""
    
    def __init__(self, camera_id: Optional[str] = None):
        # Lazy import using GObject Introspection
        try:
            global Aravis
            import gi
            gi.require_version('Aravis', '0.8')
            from gi.repository import Aravis
        except (ImportError, ValueError) as e:
            raise ImportError(
                "Aravis dependencies missing. Ensure 'gi' is installed and "
                "the Aravis-0.8 library/typelib is available on your system."
            ) from e

        self.camera_id = camera_id
        self.camera: Optional[Aravis.Camera] = None
        self.stream: Optional[Aravis.Stream] = None
        self._fps: float = 30.0

    def open(self) -> bool:
        if self.camera is not None:
            return True
            
        try:
            Aravis.update_device_list()
            self.camera = Aravis.Camera.new(self.camera_id)
            if self.camera is None:
                return False
                
            self.stream = self.camera.create_stream(None, None)
            if self.stream is None:
                self.release()
                return False
                
            payload = self.camera.get_payload()
            for _ in range(5):
                self.stream.push_buffer(Aravis.Buffer.new_allocate(payload))
                
            self._fps = self.camera.get_frame_rate()
            self.camera.start_acquisition()
            return True
        except Exception:
            self.release()
            return False

    def read(self) -> Tuple[bool, Optional[np.ndarray]]:
        if self.stream is None or self.camera is None:
            return False, None
            
        buffer = self.stream.timeout_pop_buffer(1000000)
        if buffer is None:
            return False, None
            
        try:
            if buffer.get_status() == Aravis.BufferStatus.SUCCESS:
                data = buffer.get_data()
                width = buffer.get_image_width()
                height = buffer.get_image_height()
                pixel_format = buffer.get_image_pixel_format()
                
                if pixel_format == Aravis.PIXEL_FORMAT_MONO_8:
                    frame = np.frombuffer(data, dtype=np.uint8).reshape((height, width))
                elif pixel_format in (Aravis.PIXEL_FORMAT_BAYER_RG_8, Aravis.PIXEL_FORMAT_BAYER_BG_8, 
                                      Aravis.PIXEL_FORMAT_BAYER_GB_8, Aravis.PIXEL_FORMAT_BAYER_GR_8):
                    raw = np.frombuffer(data, dtype=np.uint8).reshape((height, width))
                    conversion_map = {
                        Aravis.PIXEL_FORMAT_BAYER_RG_8: cv2.COLOR_BayerRG2BGR,
                        Aravis.PIXEL_FORMAT_BAYER_BG_8: cv2.COLOR_BayerBG2BGR,
                        Aravis.PIXEL_FORMAT_BAYER_GB_8: cv2.COLOR_BayerGB2BGR,
                        Aravis.PIXEL_FORMAT_BAYER_GR_8: cv2.COLOR_BayerGR2BGR
                    }
                    frame = cv2.cvtColor(raw, conversion_map[pixel_format])
                else:
                    frame = np.frombuffer(data, dtype=np.uint8)
                
                self.stream.push_buffer(buffer)
                return True, frame
            else:
                self.stream.push_buffer(buffer)
                return False, None
        except Exception:
            self.stream.push_buffer(buffer)
            return False, None

    def release(self) -> None:
        if self.camera is not None:
            try:
                self.camera.stop_acquisition()
            except Exception:
                pass
            self.camera = None
            
        if self.stream is not None:
            self.stream = None

    @property
    def fps(self) -> float:
        if self.camera is not None:
            try:
                self._fps = self.camera.get_frame_rate()
            except Exception:
                pass
        return self._fps

    @property
    def frame_width(self) -> int:
        if self.camera is not None:
            try:
                _, _, width, _ = self.camera.get_region()
                return width
            except Exception:
                return 0
        return 0

    @property
    def frame_height(self) -> int:
        if self.camera is not None:
            try:
                _, _, _, height = self.camera.get_region()
                return height
            except Exception:
                return 0
        return 0