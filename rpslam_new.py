#!/usr/bin/env python3

'''
rpslam.py : BreezySLAM Python with SLAMTECH RP A1 Lidar

Copyright (C) 2018 Simon D. Levy

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''

from breezyslam.algorithms import RMHC_SLAM
from breezyslam.sensors import RPLidarA1 as LaserModel
from roboviz import MapVisualizer
import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar as Lidar
import time

MAP_SIZE_PIXELS         = 500
MAP_SIZE_METERS         = 10
LIDAR_DEVICE            = '/dev/ttyUSB0'
TIMEC=1

# Ideally we could use all 250 or so samples that the RPLidar delivers in one
# scan, but on slower computers you'll get an empty map and unchanging position
# at that rate.
MIN_SAMPLES   =  100
SCAN_BYTE = b'\x20'
SCAN_TYPE = 129


# Screen width & height
W = 640
H = 480


# Set up pygame and the display
# os.putenv('SDL_FBDEV', '/dev/fb1')



# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'


# used to scale data to fit on the screen
max_distance = 0




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


def lidar_measurments(self, max_buf_meas=500):
    lidar.set_pwm(800)
    status, error_code = self.health

    cmd = SCAN_BYTE
    self._send_cmd(cmd)
    dsize, is_single, dtype = self._read_descriptor()
    if dsize != 5:
        raise RPLidarException('Wrong info reply length')
    if is_single:
        raise RPLidarException('Not a multiple response mode')
    if dtype != SCAN_TYPE:
        raise RPLidarException('Wrong response data type')
    while True:
        raw = self._read_response(dsize)
        self.log_bytes('debug', 'Received scan response: ', raw)
        if max_buf_meas:
            data_in_buf = self._serial_port.in_waiting
            if data_in_buf > max_buf_meas * dsize:
                self.log('warning',
                         'Too many measurments in the input buffer: %d/%d. '
                         'Clearing buffer...' %
                         (data_in_buf // dsize, max_buf_meas))
                self._serial_port.read(data_in_buf // dsize * dsize)
        yield _process_scan(raw)


def lidar_scans(self, max_buf_meas=500, min_len=5):
    scan = []
    iterator = lidar_measurments(lidar, max_buf_meas)
    for new_scan, quality, angle, distance in iterator:
        if new_scan:
            if len(scan) > min_len:
                yield scan
            scan = []
        if quality > 0 and distance > 0:
            scan.append((quality, angle, distance))



if __name__ == '__main__':
    scan_data = [0] * 360
    # Connect to Lidar unit
    lidar = Lidar(None, PORT_NAME)

    # Create an RMHC SLAM object with a laser model and optional robot model
    slam = RMHC_SLAM(LaserModel(), MAP_SIZE_PIXELS, MAP_SIZE_METERS)

    # Set up a SLAM display
    viz = MapVisualizer(MAP_SIZE_PIXELS, MAP_SIZE_METERS, 'SLAM')

    # Initialize an empty trajectory
    trajectory = []

    # Initialize empty map
    mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    # Create an iterator to collect scan data from the RPLidar
    #iterator = lidar.iter_scans()


    # We will use these to store previous scan in case current scan is inadequate
    previous_distances = None
    previous_angles    = None

    # First scan is crap, so ignore it
    # next(iterator)
    distances = []
    angles = []
    start=time.time()
    try:
        for scan in lidar_scans(lidar):
            #for (_, angle, distance) in scan:
            #     scan_data[min([359, floor(angle)])] = distance
            #process_data(scan_data)
            # Extract distances and angles from triples
            distances = [item[2] for item in scan]
            angles = [item[1] for item in scan]
            #print(time.time()-start)
            #print(scan)
            if time.time()-start>TIMEC:
            # Update SLAM with current Lidar scan and scan angles if adequate
                if len(distances) > MIN_SAMPLES:
                	#print("wowwwww")
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
                #print(mapbytes)

                # Display map and robot pose, exiting gracefully if user closes it
                if not viz.display(x / 1000., y / 1000., theta, mapbytes):
                    exit(0)
                start=time.time();

    except KeyboardInterrupt:
        print('Stoping.')
    lidar.stop()
    lidar.disconnect()
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
