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


def send(ins):
    # print(ins)
    ins = [('w',1)] + ins
    car_move_auto(ins)


def car_move_auto(ins):
    key=''
    ind=0
    while ind<len(ins):
        print(ind)
        key=ins[ind][0]
        timee=ins[ind][1]
        ind+=1
        time.sleep(0.1)
        move_auto(key,timee)
        if keyboard.is_pressed(STOP):
            time.sleep(0.7)
            ser.write(STOP.encode('utf-8'))


def move_auto(key,timee):
    key_was_pressed = False
    start=time.time()
    now=start
    while now-start< timee :
        if not key_was_pressed:
            ser.write(key.encode('utf-8'))
            key_was_pressed =True
        now=time.time()
    ser.write(STOP.encode('utf-8'))


def terminate():
    ser.write(STOP.encode('utf-8'))

if __name__ == '__main__':
    car_move()