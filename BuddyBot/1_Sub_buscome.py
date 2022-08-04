#!/usr/bin/env python
import os, sys
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String


class Bussub(Node):
    def __init__(self):
        super().__init__('bussub')
        qos_profile = QoSProfile(depth=10)
        self.bussub = self.create_subscription(String,'bus_come',self.subscribe_topic_message,qos_profile)

    def subscribe_topic_message(self, msg):
        self.get_logger().info('Received message: {0}'.format(msg.data))


        

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