#!usr/bin/env python3
import rospy
from std_msgs.msg import Int32
import board
import time
import busio
import adafruit_pca9685
from std_msgs.msg import String
from std_msgs.msg import Float64

#PWM Board Initialization
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)
hat.frequency = 250
total = 0xffff

#Motor Assignments
motor_up_left = hat.channels[10]
motor_up_right = hat.channels[11]
motor_side_back = hat.channels[12]
motor_side_front = hat.channels[13]
motor_forward_left = hat.channels[14]
motor_forward_right = hat.channels[15]

#Other Variable Initialization
input_color = 0
input_leak = 0

def initialize():
    print('Initializing')
    motor_up_left.duty_cycle = int(total*1500/4000)
    motor_up_right.duty_cycle = int(total*1500/4000)
    motor_side_back.duty_cycle = int(total*1500/4000)
    motor_side_front.duty_cycle = int(total*1500/4000)
    motor_forward_left.duty_cycle = int(total*1500/4000)
    motor_forward_right.duty_cycle = int(total*1500/4000)
    time.sleep(5)
    print('Initialization Complete')

def accel(m10,m11,m12,m13,m14,m15):
    print('Starting Accel')
    m10_goal = -1*m10*400
    m11_goal = -1*m11*400
    m12_goal = -1*m12*400
    m13_goal = m13*400
    m14_goal = -1*m14*400
    m15_goal = -1*m15*400
    for x in range(1,200):
        m10_val = (1500+(x/200)*m10_goal)
        m11_val = (1500+(x/200)*m11_goal)
        m12_val = (1500+(x/200)*m12_goal)
        m13_val = (1500+(x/200)*m13_goal)
        m14_val = (1500+(x/200)*m14_goal)
        m15_val = (1500+(x/200)*m15_goal)
        motor_up_left.duty_cycle = int(total*m10_val/4000)
        motor_up_right.duty_cycle = int(total*m11_val/4000)
        motor_side_back.duty_cycle = int(total*m12_val/4000)
        motor_side_front.duty_cycle = int(total*m13_val/4000)
        motor_forward_left.duty_cycle = int(total*m14_val/4000)
        motor_forward_right.duty_cycle = int(total*m15_val/4000)
        time.sleep(0.005)
    print('Accel Complete')

def decel(m10,m11,m12,m13,m14,m15):
    print('Starting Decel')
    m10_goal = -1*m10*400
    m11_goal = -1*m11*400
    m12_goal = -1*m12*400
    m13_goal = m13*400
    m14_goal = -1*m14*400
    m15_goal = -1*m15*400
    for x in range(1,200):
        m10_val = (1500+((200-x)/200)*m10_goal)
        m11_val = (1500+((200-x)/200)*m11_goal)
        m12_val = (1500+((200-x)/200)*m12_goal)
        m13_val = (1500+((200-x)/200)*m13_goal)
        m14_val = (1500+((200-x)/200)*m14_goal)
        m15_val = (1500+((200-x)/200)*m15_goal)
        motor_up_left.duty_cycle = int(total*m10_val/4000)
        motor_up_right.duty_cycle = int(total*m11_val/4000)
        motor_side_back.duty_cycle = int(total*m12_val/4000)
        motor_side_front.duty_cycle = int(total*m13_val/4000)
        motor_forward_left.duty_cycle = int(total*m14_val/4000)
        motor_forward_right.duty_cycle = int(total*m15_val/4000)
        time.sleep(0.005)
    print('Decel Complete')
    
def motorspeed(m10,m11,m12,m13,m14,m15):
    accel(m10,m11,m12,m13,m14,m15)
    time.sleep(15)
    decel(m10,m11,m12,m13,m14,m15)
    
def forward():
    print('Forward')
    initialize()
    motorspeed(-0.15, -0.15, 0.0, 0.0, 0.9, 0.9)
    initialize()

def backward():
    print('Backward')
    initialize()
    motorspeed(0.2, 0.2, 0.0, 0.0, -0.9, -0.9)
    initialize()

def left_turn():
    print('Left Turn')
    initialize()
    motorspeed(0.0, 0.0, 0.0, 0.0, -0.5, 0.5)
    initialize()

def right_turn():
    print('Right Turn')
    initialize()
    motorspeed(0.0, 0.0, 0.0, 0.0, 0.5, -0.5)
    initialize()
    
def left_slide():
    print('Left Slide')
    initialize()
    motorspeed(0.0, 0.0, 0.30, 0.25, 0.0, 0.0)
    initialize()

def right_slide():
    print('Right Slide')
    initialize()
    motorspeed(0.0, 0.0, -0.30, -0.25, 0.0, 0.0)
    initialize()

#Color Data Parsing    
def callback(color):
    global input_color
    input_color = color.data
    
#Leak Data Parsing
def callback2(leak):
    global input_leak
    input_leak = leak.data

if __name__ == '__main__':
    #Initialize Node
    rospy.init_node('Color_Grabber', anonymous=True)

    #Set up Subscriber
    rospy.Subscriber("camera_color", Int32, callback)
    rospy.Subscriber("leak", Int32, callback2)
    #Get Parameter Values
    frequency = rospy.get_param('~frequency', 2)

    #Variable Configuration
    rate = rospy.Rate(frequency)

    #Data Collection Loop
    while not rospy.is_shutdown():
	#subscribe to color topic
   	    #0 = Nope
            #1 = Red
            #2 = Orange
            #3 = Yellow
   	    #4 = Green
	    #5 = Blue
	    #6 = Purple
	    #7 = Black
        if input_color == 0:
            pass
        elif input_color == 1:
            forward()
            
        elif input_color == 2:
            backward()

        elif input_color == 3:
            left_turn()

        elif input_color == 4:
            right_turn()

        elif input_color == 5:
            left_slide()

        elif input_color == 6:
            right_slide()
      
	    #Output for debugging
        rospy.loginfo('Color #: ')
        rospy.loginfo(input_color)
        rospy.loginfo('Leak: ')
        rospy.loginfo(input_leak)
        rospy.loginfo('-----')

        #Safety exits
        if input_leak == 1:
            rospy.loginfo('Leak Detected! Abort abort abort')
            break
        if input_color == 7:
            rospy.loginfo('Black Detected: Killing Program')
            break

        rate.sleep()
    
    #Ensure motors are stopped before ending
    initialize()
