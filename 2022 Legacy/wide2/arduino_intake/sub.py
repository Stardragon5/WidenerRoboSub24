#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
import time

global start_time
global target_depth
global max_depth_speed
global Kp
global Kd
global current_error
global current_depth
global current_time
global der

start_time = time.time()
target_depth = 2.0
max_depth_speed = 150
Kp = 0
Kd = 0
current_error = 0
current_depth = 0
current_time = 0
der = 0

def drop():

    global start_time
    global target_depth
    global depth_speed
    global max_depth_speed
    global Kp
    global Kd
    global current_error
    global current_depth
    global current_time
    global der
    if(time.time() <= start_time+15.0):
        #Define previous and current error
        prior_error = current_error
        current_error = target_depth-current_depth

        #Define previous and current time
        prior_time = current_time
        current_time = time.time()

        #Calculate derivative
        #der = (current_error-prior_error)/(current_time-prior_time) 
        #der = time.time()
        depth_speed = Kp*current_error+Kd*der
        rospy.loginfo(der)

        #Safety Check for Max Speed
        if(depth_speed > max_depth_speed):
            depth_speed = max_depth_speed

    else:
        #Power Motors Off
        depth_speed = 0

    #Publish depth_speed to motor_speed topic
    
    #rospy.init_node('talker', anonymous=True)


def callback(depth):
    rospy.loginfo(depth.data)
    current_depth = depth.data
    rospy.loginfo(start_time)
    rospy.loginfo(time.time())

    drop()
    pub.publish(depth_speed)

#subscribe to depth topic
def listener():
    global pub
    pub=rospy.Publisher('motor_speed', Float64, queue_size=10)
    rospy.Subscriber("t_depth", Float64, callback)
    rospy.init_node('listener', anonymous=True)
    rospy.spin()



if __name__ == '__main__':

    listener()