import socket
import time
import pickle
import cv2
from cv2 import dilate, erode
from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from roboviz import MapVisualizer
import numpy as np
from scipy.interpolate import interp1d
from path_finder import get_directions, get_next_loc


clientAddress = "192.168.137.80"
clientPort = 20001
serverPort = 20002
serverAddress = "192.168.137.148"

bufferSize = 4096
# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((serverAddress, serverPort))

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


def update_map(curr_map, points):
    for p in points:
        print('p is ', p)
        curr_map[int(p[0]) * MAP_SIZE_PIXELS + int(p[1])] = BEEN_THERE


EMPTY = 1
VISITED = 2
BLOCKED = 3
THRESH = 129


def label_map(curr_map, points):
    curr = np.array(curr_map)
    curr = curr.reshape((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
    cv2.imwrite("Original.png", curr)
    kernel = np.ones((2, 2), np.uint8)
    img_erosion = erode(curr, kernel, iterations=2)
    new_img = dilate(img_erosion, kernel, iterations=3)
    return new_img
    cv2.imwrite('Erosion.png', np.array(img_erosion))
    cv2.imwrite('Dilation.png', np.array(new_img))
    new_map = np.zeros((MAP_SIZE_PIXELS, MAP_SIZE_PIXELS))
    for i in range(MAP_SIZE_PIXELS):
        for j in range(MAP_SIZE_PIXELS):
            new_map[i, j] = BLOCKED if new_img[i, j] < THRESH else EMPTY
            if (i, j) in points:
                new_map[i, j] = VISITED
    return new_map


def send_track(track):
    UDPServerSocket.sendto(pickle.dumps(track), (clientAddress, clientPort))


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
    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles = None
    start = time.time()
    reach_dest_flag = True
    new_loc = None
    track=[]
    idx_hor=True
    last_messege_time = time.time()
    while True:
        array = np.array([])
        message_full = UDPServerSocket.recvfrom(bufferSize)
        message = message_full[0]
        address = message_full[1]
        temp = np.frombuffer(np.array(message), dtype=np.float64)
        array = np.reshape(temp, (-1, 2))
        # Update SLAM with current Lidar scan and scan angles if adequate
        if len(array) > MIN_SAMPLES:
            distances = [item[1] for item in array]
            angles = [item[0] for item in array]
            f = interp1d(angles, distances, fill_value='extrapolate')
            distances = list(f(np.arange(360)))  # slam.update wants a list
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
        update_map(mapbytes, points)
        new_map = label_map(mapbytes, points)
        # Display map and robot pose, exiting gracefully if user closes it
        if not viz.display(x / 1000., y / 1000., theta, mapbytes):
            exit(0)
        # TODO find loc
        loc=[int(x / 1000.), int(y / 1000.)]
        print(loc)
        if time.time() - start > 30 or reach_dest_flag:
            cv2.imwrite("new_map.png", new_map)
            new_loc = get_next_loc(new_map, loc, theta)
            track = []
            start = time.time()
            reach_dest_flag = False
            idx_hor=loc[0]<new_loc[0]
        track = get_directions(new_loc, loc, theta,track,idx_hor)
        if time.time() - last_messege_time > 2:
            last_messege_time = time.time()
            send_track(track)

    # Shut down the lidar connection
    lidar.stop()
    lidar.disconnect()
