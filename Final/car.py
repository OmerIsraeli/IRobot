import time
import serial
import keyboard

ser = serial.Serial('COM9', 115200)
STOP = '1'
PAUSE= 'p'

LEDS = 't'
flag = False


def car_move():
    while True:
        if keyboard.is_pressed('w'):
            move('w')
        if keyboard.is_pressed('s'):
            move('s')
        if keyboard.is_pressed('a'):
            move('a')
        if keyboard.is_pressed('d'):
            move('d')
        if keyboard.is_pressed('p'):
            move('p')
        if keyboard.is_pressed(STOP):
            time.sleep(0.7)
            ser.write(STOP.encode('utf-8'))


def move(key):
    key_was_pressed = False
    while keyboard.is_pressed(key):
        if not key_was_pressed:
            ser.write(key.encode('utf-8'))
            key_was_pressed = True
        print(key)
    ser.write(PAUSE.encode('utf-8'))


# def control_led():
#     global key_was_pressed
#     if not key_was_pressed:
#         ser.write(LEDS.encode('utf-8'))
#         key_was_pressed = True
#         time.sleep(0.2)
#     else:
#         ser.write(LEDS.encode('utf-8'))
#         key_was_pressed = False


if __name__ == '__main__':
    car_move()