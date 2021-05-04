import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar as Lidar
import time

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
pygame.init()
lcd = pygame.display.set_mode((320, 240))
pygame.mouse.set_visible(False)
lcd.fill((0, 0, 0))
pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'

# used to scale data to fit on the screen
max_distance = 0
scan_data = [0] * 360


def process_data(data):
    # Do something useful with the data
    pass


def sent_data(distances, angles):
    pass


def main():
    lidar = Lidar(None, PORT_NAME)
    try:
        print(lidar.get_info())
        for scan in lidar.iter_scans():
        #     for (_, angle, distance) in scan:
        #         scan_data[min([359, floor(angle)])] = distance
        #     process_data(scan_data)
            distances = [item[2] for item in scan]
            angles = [item[1] for item in scan]
            sent_data(distances,angles)
    except KeyboardInterrupt:
        print('Stopping.')
    lidar.stop()
    lidar.disconnect()


if __name__ == '__main__':
    main()
