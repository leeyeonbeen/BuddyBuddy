#!/usr/bin/python3
import os, sys
import select
import rclpy
import time
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

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

TURTLEBOT3_MODEL = os.environ['TURTLEBOT3_MODEL']

e = """
Communications Failed
"""
turtlebot_go = 0
turtlebot_turn = 0
turtlebot_back = 0

vel_msg = Twist()

class Bussub(Node):
    def __init__(self):
        super().__init__('bussub')
        qos_profile = QoSProfile(depth=10)
        self.bussub = self.create_subscription(String,'bus_come',self.subscribe_topic_message,qos_profile)
            
    def subscribe_topic_message(self, msg):
        global turtlebot_go
        global turtlebot_turn
        global turtlebot_back
        
        self.get_logger().info('Received message: {0}'.format(msg.data))
        if msg.data == 'bus_arrive':
            turtlebot_go = 1
        elif msg.data == 'turn':
            turtlebot_turn = 1
        elif msg.data == 'back':
            turtlebot_back = 1   

class MoveTurtle(Node):

    def __init__(self):
        super().__init__('moveTurtle')
        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(Twist, 'cmd_vel', qos)
        self.timer = self.create_timer(4, self.timer_callback)
       
         
        status = 0
        target_linear_velocity = 0.0
        target_angular_velocity = 0.0
        control_linear_velocity = 0.0
        control_angular_velocity = 0.0
        
        
    def timer_callback(self):
        global turtlebot_go
        global turtlebot_turn
        global turtlebot_back
        
        if turtlebot_go == 1:
            target_linear_velocity = 0.2
            target_angular_velocity = 0.0
            control_linear_velocity = 0.2
            control_angular_velocity = 0.0
            #self.print_vels(target_linear_velocity, target_angular_velocity)
            turtlebot_go = 0
        elif turtlebot_turn == 1:
            target_linear_velocity = 0.0
            target_angular_velocity = 0.7
            control_linear_velocity = 0.0
            control_angular_velocity = 0.7
            #self.print_vels(target_linear_velocity, target_angular_velocity)
            turtlebot_turn = 0
        elif turtlebot_back == 1:
            target_linear_velocity = 0.2
            target_angular_velocity = 0.0
            control_linear_velocity = 0.2
            control_angular_velocity = 0.0
            #self.print_vels(target_linear_velocity, target_angular_velocity)
            turtlebot_back = 0
        else:
            target_linear_velocity = 0.0
            target_angular_velocity = 0.0
            control_linear_velocity = 0.0
            control_angular_velocity = 0.0
            #self.print_vels(target_linear_velocity, target_angular_velocity)
            turtlebot_go = 0
            turtlebot_turn = 0
            turtlebot_back = 0
        twist = Twist()

        #control_linear_velocity = self.make_simple_profile(control_linear_velocity,target_linear_velocity,(LIN_VEL_STEP_SIZE / 2.0))

        twist.linear.x = control_linear_velocity
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        #control_angular_velocity = self.make_simple_profile(control_angular_velocity,target_angular_velocity,(ANG_VEL_STEP_SIZE / 2.0))

        twist.angular.x = 0.0
        twist.angular.y = 0.0
        twist.angular.z = control_angular_velocity

        self.pub.publish(twist)
        print("Pub")

    
    def print_vels(target_linear_velocity, target_angular_velocity):
        print('currently:\tlinear velocity {0}\t angular velocity {1} '.format(
        target_linear_velocity,
        target_angular_velocity))

    def make_simple_profile(output, input, slop):
        if input > output:
            output = min(input, output + slop)
        elif input < output:
            output = max(input, output - slop)
        else:
            output = input

        return output


    def constrain(input_vel, low_bound, high_bound):
        if input_vel < low_bound:
            input_vel = low_bound
        elif input_vel > high_bound:
            input_vel = high_bound
        else:
            input_vel = input_vel

        return input_vel


    def check_linear_limit_velocity(velocity):
        if TURTLEBOT3_MODEL == 'burger':
            return constrain(velocity, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
        else:
            return constrain(velocity, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)


    def check_angular_limit_velocity(velocity):
        if TURTLEBOT3_MODEL == 'burger':
            return constrain(velocity, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
        else:
            return constrain(velocity, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)


if __name__ == '__main__':
    rclpy.init(args=None)
    
    bussub = Bussub()
    moveturtle = MoveTurtle()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(bussub)
    executor.add_node(moveturtle)

    executor_thread = threading.Thread(target=executor.spin, daemon=True)
    executor_thread.start()
    rate = bussub.create_rate(2)
    try:
        while rclpy.ok():
            rate.sleep()
    except KeyboardInterrupt:
        pass
    
    rclpy.shutdown()
    executor_thread.join() 