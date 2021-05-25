import socket
import time
import pickle

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from roboviz import MapVisualizer
import numpy as np
from scipy.interpolate import interp1d
#from .path_finder import get_directions

# from roboviz import MapVisualizer

localIP = "132.64.143.30"
localIP_IMG = "127.0.0.1"
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


MAP_SIZE_PIXELS = 500
MAP_SIZE_METERS = 10

mm_to_px = MAP_SIZE_PIXELS / (MAP_SIZE_METERS * 1000)
BEEN_THERE = 0


TIMEC = 1

# Ideally we could use all 250 or so samples that the RPLidar delivers in one
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES = 10
SCAN_BYTE = b'\x20'
SCAN_TYPE = 129

# Screen width & height
W = 640
H = 480


def b2img(mapbytes, pixels=MAP_SIZE_PIXELS):
    map = np.zeros((pixels, pixels))
    for i in range(pixels):
        for j in range(pixels):
            map[i][j] = mapbytes[i * pixels + j]
    return map


def send_img(img):
    UDPServerSocket_IMG = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket_IMG.sendto(img, (localIP_IMG, localPort_IMG))


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


def update_map(curr_map, points):
    for p in points:
        print('p is ' , p)
        curr_map[int(p[0]) * MAP_SIZE_PIXELS + int(p[1])] = BEEN_THERE


EMPTY = 1
VISITED = 2
BLOCKED = 3
THRESH = 20

def label_map(curr_map, points):
    #labels = {b'\x00': EMPTY, b'\x7F': VISITED, BEEN_THERE: BLOCKED}
    print(curr_map)
    return curr_map
    new_map = np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
    for i in range(MAP_SIZE_PIXELS):
        for j in range(MAP_SIZE_PIXELS):
            if (i, j) in points:
                new_map[i, j] = VISITED
            else:
                new_map[i, j] = BLOCKED if curr_map[i * MAP_SIZE_PIXELS + j] < THRESH else EMPTY

    return new_map


if __name__ == '__main__':

    # Connect to Lidar unit

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)
    # Set up a SLAM display
    viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')
    # Initialize an empty trajectory
    trajectory = []

    # Initialize empty map
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    points = []
    # Create an iterator to collect scan data from the RPLidar
    # iterator = lidar.iter_scans()

    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles = None
    start = time.time()
    while True:
        # size = int(UDPServerSocket.recv(6))
        # print(size)
        array = np.array([])
        # while size > len(array):
        message_full = UDPServerSocket.recvfrom(bufferSize)
        message = message_full[0]
        address = message_full[1]
        #print(message)
        temp = np.frombuffer(np.array(message), dtype=np.float64)
        # print(temp)
        array = np.reshape(temp, (-1, 2))
        #print(array)

        # clientMsg = "Message from Client:{}".format(message)
        # print(decoded_msg)
        # scan_data = [0] * 360
        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(array) > MIN_SAMPLES:
            # print("wowwwww")
            distances = [item[1] for item in array]
            angles = [item[0] for item in array]

            f = interp1d(angles, distances, fill_value='extrapolate')
            distances = list(f(np.arange(360)))  # slam.update wants a list
            # istances = array[0]
            # angles = array[1]
            # print("distances: ",distances,"\n angles: ",angles,"\n")
            # slam.update(distances, scan_angles_degrees=angles)
            slam.update(distances)
            previous_distances = distances.copy()
            previous_angles = angles.copy()

        # If not adequate, use previous
        elif previous_distances is not None:
            slam.update(previous_distances, scan_angles_degrees=previous_angles)

        # Get current robot position and add it to path
        x, y, theta = slam.getpos()
        points.append((np.floor(y * mm_to_px), np.floor(x * mm_to_px)))
        # Get current map bytes as grayscale
        slam.getmap(mapbytes)
        # print(mapbytes)
        # for byte in mapbytes:
        #     if byte != 127:
        #         #print("erez")
        # img=b2img(mapbytes,MAP_SIZE_PIXELS)
        # if(time.time()-start>2):
        #     send_img(img)
        #     start = time.time()

        update_map(mapbytes, points)
        # Display map and robot pose, exiting gracefully if user closes it
        if not viz.display(x / 1000., y / 1000., theta, mapbytes):
            exit(0)
        new_map = label_map(mapbytes, points)
        raise exception()
        track = get_directions(new_map,loc,theta)
        #print(2 in new_map)
        #print(1 in new_map)
        #print(0 in new_map)
        # start=time.time()

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
