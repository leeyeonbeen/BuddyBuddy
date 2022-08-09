#!/usr/bin/python3
import os, sys
import select
import rclpy
import time
from rclpy.node import Node

from std_msgs.msg import Header, String, Int32
from geometry_msgs.msg import Twist, Vector3
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class MoveTurtle(Node):
    def __init__(self):
        global pre_vel
        global stop
        super().__init__('Move_Turtle')
        qos_profile = QoSProfile(depth=10)
        self.sub1 = self.create_subscription(String,'bus_come',self.turn_to_turtle,qos_profile)
        self.sub2 = self.create_subscription(Int32,'closer',self.move_to_turtle,qos_profile)
        pre_vel = 0
        stop = 0
    
    def turn_to_turtle(self, msg):
        global pre_vel
        global pub1
        global pub2
        global detect_sign
        global twist
        global control_linear_velocity
        global control_angular_velocit

        self.get_logger().info('Received message: {0}'.format(msg.data))
        if msg.data == 'move':
            turtlebot_go = 1   
        elif msg.data == 'bus_recognition':
            turtlebot_go = 2
            
        qos = QoSProfile(depth=10)
        self.pub1 = self.create_publisher(Twist, 'cmd_vel', qos)
        self.pub2 = self.create_publisher(Int32,'detection_sign', qos)
        detect_sign = Int32()
        twist = Twist()
        
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0
        
        if turtlebot_go == 1:
            control_linear_velocity = 0.0
            control_angular_velocity = 0.05    
            twist.linear.x = control_linear_velocity
            twist.angular.z = control_angular_velocity
            self.pub1.publish(twist)
            pre_vel = 1
        elif turtlebot_go == 2:
            if pre_vel == 1:
                #go
                control_linear_velocity = 0.2
                control_angular_velocity = 0.0
                twist.linear.x = control_linear_velocity
                twist.angular.z = control_angular_velocity 
                self.pub1.publish(twist)
                pre_vel = 2 
                detect_sign.data = 1 
                self.pub2.publish(detect_sign)
                           
                   
    def move_to_turtle(self, msg):
        global pre_vel
        global pub1
        global pub2
        global detect_sign
        global twist
        global control_linear_velocity
        global control_angular_velocit
        
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        twist.linear.y = 0.0
        twist.linear.z = 0.0
        twist.angular.x = 0.0
        twist.angular.y = 0.0

        turtle_go = 0
        pre_vel = 2
        stop = 0
        detect_sign.data= 0 
        self.pub2.publish(detect_sign)
        
        #stop
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub1.publish(twist)
        time.sleep(3)
                    
        #turn
        control_linear_velocity = 0.0
        control_angular_velocity = 1.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub1.publish(twist)
        time.sleep(3)
                
        #back
        control_linear_velocity = 0.2
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub1.publish(twist)
        time.sleep(4)
                
        #turn
        control_linear_velocity = 0.0
        control_angular_velocity = 1.1
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub1.publish(twist)
        time.sleep(3)
                
        #stop
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        twist.linear.x = control_linear_velocity
        twist.angular.z = control_angular_velocity
        self.pub1.publish(twist)

            

if __name__ == '__main__':
    rclpy.init(args=None)
    moveTturtle = MoveTurtle()
    try:
        rclpy.spin(moveTturtle)
    except KeyboardInterrupt:
        moveTturtle.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        moveTturtle.destroy_node()
        rclpy.shutdown()