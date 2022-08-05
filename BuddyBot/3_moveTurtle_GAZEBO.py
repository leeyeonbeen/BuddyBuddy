#!/usr/bin/python3
import os, sys
import select
import rclpy
import threading
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
        
        if msg.data == 'bus_arrive':
            turtlebot_go = 1   
        elif msg.data == 'back':
            turtlebot_go = 1 
        elif msg.data == 'turn':
            turtlebot_go = 2
        elif msg.data == 'turn_2':
            turtlebot_go = 3  
        elif msg.data == 'stop':
            turtlebot_go = 0
        
        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', qos)
        
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        
        if turtlebot_go == 1:
            control_linear_velocity = 0.2
            control_angular_velocity = 0.0
            turtlebot_go = 0
        elif turtlebot_go == 2:
            control_linear_velocity = 0.0
            control_angular_velocity = 1.0           
            turtlebot_go= 0
        elif turtlebot_go == 3:
            control_linear_velocity = 0.0
            control_angular_velocity = 1.1           
            turtlebot_go= 0
        else:
            control_linear_velocity = 0.0
            control_angular_velocity = 0.0          
            turtlebot_go = 0
        twist = Twist()
        
        twist.linear.x = control_linear_velocity
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
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