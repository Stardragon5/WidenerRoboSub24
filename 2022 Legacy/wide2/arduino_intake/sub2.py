#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
import time

global start_time
global target_position_x
global min_x_speed
global x_speed
global Kp
global Kd
global current_error_x
global current_position_x
global current_velo_x
global current_accel_x
global der_x
global current_time
global flag

start_time = time.time()
target_position_x = -10.0
min_x_speed = -200
x_speed = 0.0
Kp = 10
Kd = 0
current_error_x = 0.0
current_position_x = 0.0
current_velo_x = 0.0001
prior_velo_x = 0.0
current_accel_x = 0.0
der_x = 0.0
current_time = 0.0
flag = 0

###############################################
import board
import time
import busio
import adafruit_pca9685
i2c = busio.I2C(board.SCL, board.SDA)

hat = adafruit_pca9685.PCA9685(i2c)
x=15
hat.frequency = 250

motor_forward_left = hat.channels[14]
motor_forward_right = hat.channels[15]
motor_up_left = hat.channels[10]
motor_up_right = hat.channels[11]
motor_side_front = hat.channels[13]
motor_side_back = hat.channels[12]
total = 0xffff
time.sleep(7)

########################################################

def drop(flag, current_accel_x):
    global start_time
    global target_position_x
    global min_x_speed
    global x_speed
    global Kp
    global Kd
    global current_error_x
    global current_position_x
    global current_velo_x
    global prior_velo_x
    global der_x
    global current_time
    global temp
    
    if (flag == 0):
        current_velo_x = 0.0
        prior_velo_x = 0.0
        print(current_velo_x)
        current_time = time.time()
    
    if(time.time() <= start_time+15.0):
        #Define previous and current time
        prior_time = current_time
        current_time = time.time()

        #Define previous and current velo
        prior_velo_x = current_velo_x
        #prior_velo_x = 0.0
        #temp = 1
        #temp = current_accel_x*(current_time-prior_time)
        current_velo_x = prior_velo_x+(current_accel_x*(current_time-prior_time))
        #current_velo_x = prior_velo_x - temp

        #Define previous and current position
        prior_position_x = current_position_x
        current_position_x = prior_position_x+current_velo_x*(current_time-prior_time)
        #Define previous and current error
        prior_error_x = current_error_x
        current_error_x = target_position_x-current_position_x

        
        #Calculate derivative
        der_x = (current_error_x-prior_error_x)/(current_time-prior_time) 
        #der = time.time()
        x_speed = Kp*current_error_x+Kd*der_x
        

        #Safety Check for Max Speed
        if(x_speed < min_x_speed):
            x_speed = min_x_speed

    else:
        #Power Motors Off
        x_speed = 0

    #rospy.loginfo(current_time-prior_time)
    #rospy.loginfo((current_time-prior_time))
    #print(current_velo_x)
    #rospy.loginfo(Kp)
    rospy.loginfo(current_position_x)
    #rospy.loginfo(der_x)
    rospy.loginfo(x_speed)
    motor_forward_left.duty_cycle = int(total*(x_speed+1500)/4000)
    motor_forward_right.duty_cycle = int(total*(x_speed+1500)/4000)


def callback(accel_x):
    global flag
    current_accel_x = accel_x.data+0.24
    #rospy.loginfo(current_accel_x)
    #rospy.loginfo(prior_velo_x)
    rospy.loginfo('---------------------')
    rospy.loginfo(time.time()-start_time)

    drop(flag,current_accel_x)
    flag = 1
    pub.publish(x_speed)

#subscribe to depth topic
def listener():
    global pub
    pub=rospy.Publisher('motor_speed', Float64, queue_size=10)
    rospy.Subscriber("t_accel_x", Float64, callback)
    rospy.init_node('listener', anonymous=True)
    rospy.spin()



if __name__ == '__main__':

    listener()
   