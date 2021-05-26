import socket
import select
import pickle
import numpy as np
from adafruit_rplidar import RPLidar as Lidar


serverAddress = "132.64.143.30"
clientPort = 20001
serverPort = 20002
clientAddress = "127.0.0.1"
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
            print(new_scan)
            readable, writable, exceptional = select.select([UDPClientSocket],
                                                            [UDPClientSocket],
                                                            [UDPClientSocket])
            if UDPClientSocket in writable:
                sent_data(new_scan.tobytes())
            if UDPClientSocket in readable:
                data, addr = UDPClientSocket.recvfrom(1024)
                print(data)
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
