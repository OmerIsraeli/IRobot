import socket
import time
import pickle
import numpy as np

address = "132.64.143.30"
msgFromClient = "Hello UDP Server"
bytesToSend = str.encode(msgFromClient)
serverAddressPort = (address, 20001)
bufferSize = 4096
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Send to server using created UDP socket
i = 1

import os
from math import cos, sin, pi, floor
import pygame
from adafruit_rplidar import RPLidar as Lidar
import time

# Set up pygame and the display
os.putenv('SDL_FBDEV', '/dev/fb1')
# pygame.init()
# lcd = pygame.display.set_mode((320, 240))
# pygame.mouse.set_visible(False)
# lcd.fill((0, 0, 0))
# pygame.display.update()

# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = Lidar(None, PORT_NAME)
# used to scale data to fit on the screen
max_distance = 0
SIZE_POCKET = 200
scan_data = [0] * 360


def process_data(data):
    # Do something useful with the data
    pass


def sent_data(data):
    #     data=concat_dist_angles(distances, angles)

    #     UDPClientSocket.sendall(('%6d'.encode() % len(data)), serverAddressPort )
    UDPClientSocket.sendto(data, serverAddressPort)
    # print(i)
    # i += 1


def main():
    try:
        # print(lidar.get_info())
        for scan in lidar.iter_scans():
            #     for (_, angle, distance) in scan:
            #         scan_data[min([359, floor(angle)])] = distance
            #     process_data(scan_data)
            #             NOR=np.random.choice(len(scan),min(SIZE_POCKET,len(scan)),replace=False)

            #             new_scan = np.array(scan)[NOR,:]

            #             distances = [item[2] for item in scan]
            #             angles = [item[1] for item in scan]
            new_scan = np.array([(item[1], item[2]) for item in scan])
            #             print(len(distances))
            print(new_scan)
            #             data = np.array((distances,angles))
            sent_data(new_scan.tobytes())


    except KeyboardInterrupt:
        print('Stopping.')
    lidar.stop()
    lidar.disconnect()


def concat_dist_angles(distances, angles):
    arr = (distances, angles)
    data_string = pickle.dumps(arr)
    return data_string


if __name__ == '__main__':
    main()
