#!/usr/bin/env python3
import board
import time
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)

hat = adafruit_pca9685.PCA9685(i2c)

hat.frequency = 250

motor_forward_left = hat.channels[14]
motor_forward_right = hat.channels[15]
motor_up_left = hat.channels[10]
motor_up_right = hat.channels[11]
motor_side_front = hat.channels[13]
motor_side_back = hat.channels[12]
total = 0xffff

time.sleep(7)
i=150
x=150
y=166
y2=120
z=130

#Forward Accel
def fwdaccel(a,b):
    print('Forward Accel')
    while (a>b):
        motor_forward_left.duty_cycle = int(total*a/400)
        motor_forward_right.duty_cycle = int(total*a/400)
        a=a-0.1
        time.sleep(0.02)

def fwddecel(a,b):
    print('Forward Decel')
    while (a<b):
        motor_forward_left.duty_cycle = int(total*a/400)
        motor_forward_right.duty_cycle = int(total*a/400)
        a=a+0.1
        time.sleep(0.02)

def downaccel(a,b):
    print('Down Accel')
    while (a<b):
        motor_up_left.duty_cycle = int(total*a/400)
        motor_up_right.duty_cycle = int(total*a/400)
        a=a+0.3
        time.sleep(0.02)

def updecel(a,b):
    print('Up Decel')
    while (a>b):
        motor_up_left.duty_cycle = int(total*a/400)
        motor_up_right.duty_cycle = int(total*a/400)
        a=a-0.3
        time.sleep(0.01)

print('Down Motion')
downaccel(x, y)
motor_up_left.duty_cycle = int(total*y/400)
motor_up_right.duty_cycle = int(total*y/400)
time.sleep(7)          

#motor_up_left.duty_cycle = int(total*x/400)
#motor_up_right.duty_cycle = int(total*x/400)
# time.sleep(5)              #hold y position

#fwdaccel(x, z)
#updecel(x, y2)

#print('Forward Motion')
#motor_forward_left.duty_cycle = int(total*z/400)
#motor_forward_right.duty_cycle = int(total*z/400)
#time.sleep(5)               #move forwards

#fwddecel(z, x)
updecel(y, x)

print('Shutting Off')
motor_forward_left.duty_cycle = int(total*x/400)
motor_forward_right.duty_cycle = int(total*x/400)
time.sleep(5)

# updecel(y-2, x)
motor_up_left.duty_cycle = int(total*x/400)
motor_up_right.duty_cycle = int(total*x/400)
time.sleep(5)               #back to 0


# for i in range (0,10,1):
#     time.sleep(0.5)
#     motor_up_left.duty_cycle = int(total*y/400)
#     motor_up_right.duty_cycle = int(total*y/400)
#     time.sleep(0.5)
#     motor_up_left.duty_cycle = int(total*x/40)
#     motor_up_right.duty_cycle = int(total*x/40)
# time.sleep(1)


