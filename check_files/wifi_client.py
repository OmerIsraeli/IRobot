import socket
import select
import pickle
import numpy as np
from adafruit_rplidar import RPLidar as Lidar
from car import car_move_auto

serverAddress = "192.168.137.148"
clientPort = 20001
serverPort = 20002
clientAddress = "192.168.137.80"
# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPClientSocket.bind((clientAddress, clientPort))	
# Send to server using created UDP socket


# Setup the RPLidar
PORT_NAME = '/dev/ttyUSB0'
lidar = Lidar(None, PORT_NAME)


def sent_data(data):
    UDPClientSocket.sendto(data, (serverAddress, serverPort))


def main():
    try:
        for scan in lidar.iter_scans():
            new_scan = np.array([(item[1], item[2]) for item in scan])
            #print(new_scan)
            readable, writable, exceptional = select.select([UDPClientSocket],
                                                            [UDPClientSocket],
                                                            [UDPClientSocket])
            sent_data(new_scan.tobytes())
            if UDPClientSocket in readable:
                data, addr = UDPClientSocket.recvfrom(1024)
                new_data = pickle.loads(data)
                print(new_data)
                new_data+=[('p',0.1,0)]
                #car_move_auto(new_data)
                
    except KeyboardInterrupt:
        print('Stopping.')
    lidar.stop()
    lidar.disconnect()


if __name__ == '__main__':
    main()
