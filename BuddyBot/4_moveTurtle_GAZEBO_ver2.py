#!/usr/bin/python3
import os, sys
import select
import rclpy
import threading
import time
from rclpy.node import Node

from std_msgs.msg import Header, String, Int32
from geometry_msgs.msg import Twist, Vector3
from rclpy.qos import QoSProfile
from std_msgs.msg import String


if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

class Bussub(Node):
    def __init__(self):
        super().__init__('bussub')
        qos_profile = QoSProfile(depth=10)
        self.bussub = self.create_subscription(String,'bus_come',self.move_to_turtle,qos_profile)
            
    def move_to_turtle(self, msg):
        global turtlebot_go
        
        self.get_logger().info('Received message: {0}'.format(msg.data))
        
        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', qos)
        twist = Twist()
        
        control_linear_velocity = 0.2
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = control_angular_velocity
        self.pub.publish(twist)
        time.sleep(4)
        
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub.publish(twist)
        time.sleep(3)
        
        control_linear_velocity = 0.0
        control_angular_velocity = 1.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub.publish(twist)
        time.sleep(3)
        
        control_linear_velocity = 0.2
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub.publish(twist)
        time.sleep(4)
        
        control_linear_velocity = 0.0
        control_angular_velocity = 1.1
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub.publish(twist)
        time.sleep(3)
        
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub.publish(twist)
  

if __name__ == '__main__':
    rclpy.init(args=None)
    bussub = Bussub()
    try:
        rclpy.spin(bussub)
    except KeyboardInterrupt:
        bussub.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        bussub.destroy_node()
        rclpy.shutdown()