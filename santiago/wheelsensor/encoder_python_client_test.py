'''
Runs a client that interfaces with an Arduino Uno, which has a rotary encoder
connected to it. The Arduino reports encoder position changes through the
serial monitor with a timestamp, which the client reads and stores. 

By Cody Jarrett based on old wheelclient.py used for the optical mouse wheelsensor.
'''

import sys
import serial
import struct
import time
import numpy as np

SERIAL_PORT_PATH = '/dev/ttyACM0'
SERIAL_BAUD = 115200
SERIAL_TIMEOUT = None

opcode = {
    'OK'                    : 0xaa,
    'TEST_CONNECTION'       : 0x02,
    'SET_THRESHOLD_MOVE'    : 0x06,
    'GET_THRESHOLD_MOVE'    : 0x07,
    'SET_THRESHOLD_STOP'    : 0x08,
    'GET_THRESHOLD_STOP'    : 0x09,
    'SET_SAMPLING_PERIOD'   : 0x0a,
    'GET_SAMPLING_PERIOD'   : 0x0b,
    'GET_SERVER_VERSION'    : 0x0e,
    'TEST'                  : 0xee,
    'ERROR'                 : 0xff,
}
for k,v in opcode.iteritems():
    opcode[k]=chr(v)


class RotaryClient(object):
    def __init__(self, connectnow=True):
        '''
        Rotary encoder client for the Arduino Uno
        '''
        self.ser = serial.Serial(SERIAL_PORT_PATH, SERIAL_BAUD, timeout=SERIAL_TIMEOUT)
    def test_connection(self):
        self.ser.write(opcode['TEST_CONNECTION'])
        connectionStatus = self.ser.read()
        if connectionStatus == opcode['OK']:
            return 'OK'
        else:
            return 'No connection'
    def get_version(self):
        '''Return version number from server as a string'''
        self.ser.write(opcode['GET_SERVER_VERSION'])
        versionString = self.ser.readline()
        return versionString.strip()
    def reset(self):
        self.ser.setDTR(False)
	time.sleep(0.5)
	self.ser.setDTR(True)
    def set_sampling_period(self, value):
        self.ser.write(opcode['SET_SAMPLING_PERIOD'])
        packedValue = struct.pack('<l', value)
        self.ser.write(packedValue)
    def get_sampling_period(self):
        self.ser.write(opcode['GET_SAMPLING_PERIOD'])
        valueStr = self.ser.readline()
        return int(valueStr.strip())
    def set_threshold_move(self, value):
        self.ser.write(opcode['SET_THRESHOLD_MOVE'])
        packedValue = struct.pack('<l', value)
        self.ser.write(packedValue)
    def get_threshold_move(self):
        self.ser.write(opcode['GET_THRESHOLD_MOVE'])
        valueStr = self.ser.readline()
        return int(valueStr.strip())
    def get_time_and_position(self):
        valueStr = self.ser.readline().strip().split(' ')
        return valueStr
    def flush_serial_buffers(self):
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

if __name__ == '__main__':

    # Specify which side of behavior rig the encoder is on
    encoderSide = 'left'
    #encoderSide = 'right'

    # Set encoder side multiplier
    if encoderSide == 'left':
        encoderSideMultiplier = -1.0
    else:
        encoderSideMultiplier = 1.0

    # Set up variables for tracking how long Python client runs
    runtime = 10
    run = True

    # Set period for Arduino to sample from encoder
    samplingPeriod = 20 # In milliseconds
    # Set velocity threshold for movement recognition on Arduino
    thresholdMove = 10

    # Set up lists for storing time and position during experiment
    timeList = []
    posList = []

    print('samplingPeriod = {}'.format(samplingPeriod))
    print('thresholdMove = {}'.format(thresholdMove))
    
    # Make serial connection with Arduino
    client = RotaryClient()
    # Reset Arduino Uno
    client.reset()
    # Flush serial monitor
    client.flush_serial_buffers()

    # Set samplingPeriod and thresholdMove variables
    client.set_sampling_period(samplingPeriod) # In milliseconds
    client.set_threshold_move(thresholdMove)
    
    # Wait a little longer for Arduino to finish resetting
    time.sleep(3)

    # Begin client timer
    startTime = time.time()

    print('Client started')
    # Start sampling from Arduino
    while run:
        # Get data from serial port, strip newlines, and split into time and pos
        data = client.get_time_and_position()
        print(data)
        # Convert ms time data from Arduino to seconds and put it in timeList
        timeList.append(float(data[0]) / 1000)
        # Convert position data from Arduino to int and put it in posList
        posList.append(int(data[1]) * encoderSideMultiplier)
        # Check if Python script needs to stop running
        if (time.time() - startTime) > runtime:
            run = False

    # Convert time and position lists to numpy arrays
    timeArray = np.array(timeList)
    posArray = np.array(posList)

    # Save time and position arrays to a single .npz file
    np.savez('/home/jarauser/Desktop/EncoderPosTime.npz', time=timeArray,
         position=posArray)


