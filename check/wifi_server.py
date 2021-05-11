import socket
import time
import pickle

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
#from roboviz import MapVisualizer

localIP = "132.64.143.201"
localPort = 20001
bufferSize = 4096
msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
# Listen for incoming datagrams


MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10

TIMEC=1

# Ideally we could use all 250 or so samples that the RPLidar delivers in one
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES   =  10
SCAN_BYTE = b'\x20'
SCAN_TYPE = 129


# Screen width & height
W = 640
H = 480


def _process_scan(raw):
    '''Processes input raw data and returns measurment data'''
    new_scan = bool(raw[0] & 0b1)
    inversed_new_scan = bool((raw[0] >> 1) & 0b1)
    quality = raw[0] >> 2
    if new_scan == inversed_new_scan:
        raise RPLidarException('New scan flags mismatch')
    check_bit = raw[1] & 0b1
    if check_bit != 1:
        raise RPLidarException('Check bit not equal to 1')
    angle = ((raw[1] >> 1) + (raw[2] << 7)) / 64.
    distance = (raw[3] + (raw[4] << 8)) / 4.
    return new_scan, quality, angle, distance


if __name__ == '__main__':

    # Connect to Lidar unit


    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display
    #viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')

    # Initialize an empty trajectory
    trajectory = []

    # Initialize empty map
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    # Create an iterator to collect scan data from the RPLidar
    #iterator = lidar.iter_scans()


    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles    = None
    while True:
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        decoded_msg = data_arr = pickle.loads(message)


        #clientMsg = "Message from Client:{}".format(message)
        #print(decoded_msg)
        # scan_data = [0] * 360
        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(data_arr) > MIN_SAMPLES:
            #print("wowwwww")
            distances=[item[0] for item in data_arr]
            angles = [ item[1] for item in data_arr]
            slam.update(distances, scan_angles_degrees=angles)
            previous_distances = distances.copy()
            previous_angles = angles.copy()

        # If not adequate, use previous
        elif previous_distances is not None:
            slam.update(previous_distances, scan_angles_degrees=previous_angles)

        # Get current robot position
        x, y, theta = slam.getpos()

        # Get current map bytes as grayscale
        slam.getmap(mapbytes)
        print(mapbytes)

        # Display map and robot pose, exiting gracefully if user closes it
        # if not viz.display(x / 1000., y / 1000., theta, mapbytes):
        #     exit(0)
        start=time.time()

    # while True:
    #
    #     # Extract (quality, angle, distance) triples from current scan
    #     items = [item for item in next(iterator)]



    # Shut down the lidar connection
    lidar.stop()
    lidar.disconnect()

"""
Consume LIDAR measurement file and create an image for display.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2019 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""








scan_data = [0] * 360