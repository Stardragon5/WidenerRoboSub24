#!/usr/bin/env python3
import roslib #; roslib.load_manifest('numpy_tutorials') 
import rospy
from std_msgs.msg import String
from std_msgs.msg import Int32
from std_msgs.msg import Float64
import serial

ser = serial.Serial('/dev/ttyACM1', 115200)

def arduino():
 while not rospy.is_shutdown():

   #reading data from arduino into list
   data = ser.readline()
   data2 = data.decode('utf-8')
   data_list = data2.split(':')

   #assigning all data in the list
   leak = int(data_list[1])
   internal_pressure = float(data_list[2])
   magnetic_x = float(data_list[3])
   magnetic_y = float(data_list[4])
   magnetic_z = float(data_list[5])
   accel_x = float(data_list[6])
   accel_y = float(data_list[7])
   accel_z = float(data_list[8])
   gyro_x = float(data_list[9])
   gyro_y = float(data_list[10])
   gyro_z = float(data_list[11])
   external_pressure = float(data_list[12])
   depth = float(data_list[13])

   rospy.loginfo(accel_x)
   pub_leak.publish(leak)
   pub_accel_x.publish(accel_x)
   pub_accel_y.publish(accel_y)
   pub_accel_z.publish(accel_z)
   pub_gyro_z.publish(gyro_z)
   pub_depth.publish(depth)
   #rospy.sleep(1.0)


if __name__ == '__main__':
  try:
    pub_leak = rospy.Publisher('t_leak', Int32, queue_size = 10)
    pub_accel_x = rospy.Publisher('t_accel_x', Float64, queue_size = 10)
    pub_accel_y = rospy.Publisher('t_accel_y', Float64, queue_size = 10)
    pub_accel_z = rospy.Publisher('t_accel_z', Float64, queue_size = 10)
    pub_gyro_z = rospy.Publisher('t_gyro_z', Float64, queue_size = 10)
    pub_depth = rospy.Publisher('t_depth', Float64, queue_size = 10)
    rospy.init_node('arduino')
    arduino()
  except rospy.ROSInterruptException:
    pass
