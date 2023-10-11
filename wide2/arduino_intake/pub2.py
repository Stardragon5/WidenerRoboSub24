#!/usr/bin/env python3
import rospy
import serial
import sys
import time
from std_msgs.msg import Int32
from sensor_msgs.msg import Imu, MagneticField

imu_raw = Imu() #Raw IMU data
mag_msg = MagneticField()   #Magnetometer data

if __name__ == '__main__':
    #Initiate Node
    rospy.init_node("Serial_Parsing")

    #Sensor measurement publishers
    pub_raw = rospy.Publisher('imu/raw', Imu, queue_size=1)
    pub_mag = rospy.Publisher('imu/mag', MagneticField, queue_size=1)
    pub_leak = rospy.Publisher('leak', Int32, queue_size = 10)

    # Get parameter values
    port = rospy.get_param('~port', '/dev/ttyACM0')
    frame_id = rospy.get_param('~frame_id', 'imu_link')
    frequency = rospy.get_param('~frequency', 5)

    #Open Serial Port at port
    try:
        ser = serial.Serial(port, 115200)
    except serial.serialutil.SerialException:
        rospy.logerr("IMU not found at port" + port +". Check the port in the launch file.")
        sys.exit(0)

    #Variable Configuration
    rate = rospy.Rate(frequency)
    seq = 0

    #Data Collection Loop
    while not rospy.is_shutdown():
        #Reading data from arduino into list
        data = ser.readline()
        data2 = data.decode('utf-8')
        data_list = data2.split(':')

        #Assigning all data in the list
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

        #Publish leak sensor
        pub_leak.publish(leak)

        #Publish raw IMU data
        imu_raw.header.stamp = rospy.Time.now()
        imu_raw.header.frame_id = frame_id
        imu_raw.header.seq = seq
        imu_raw.orientation_covariance[0] = -1
        imu_raw.linear_acceleration.x = accel_x
        imu_raw.linear_acceleration.y = accel_y
        imu_raw.linear_acceleration.z = accel_z
        imu_raw.linear_acceleration_covariance[0] = -1
        imu_raw.angular_velocity.x = gyro_x
        imu_raw.angular_velocity.y = gyro_y
        imu_raw.angular_velocity.z = gyro_z
        imu_raw.angular_velocity_covariance[0] = -1
        pub_raw.publish(imu_raw)

        #Publish magnetometer data
        mag_msg.header.stamp = rospy.Time.now()
        mag_msg.header.frame_id = frame_id
        mag_msg.header.seq = seq
        mag_msg.magnetic_field.x = magnetic_x
        mag_msg.magnetic_field.y = magnetic_y
        mag_msg.magnetic_field.z = magnetic_z
        pub_mag.publish(mag_msg)

        #Update other variables
        seq = seq+1
    rate.sleep()
ser.close()


