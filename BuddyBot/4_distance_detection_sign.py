#!/usr/bin/env python
import os, sys
import rclpy
import time
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import Header, String, Int32


class Distance(Node):
    def __init__(self):
        global dis
        super().__init__('distance_detection')
        qos_profile = QoSProfile(depth=10)
        self.sub = self.create_subscription(Int32,'detection_sign',self.subscribe_detection_sign,qos_profile)
        dis = 10

    def subscribe_detection_sign(self, msg):
        global dis
        self.get_logger().info('Received message: {0}'.format(msg.data))
        qos = QoSProfile(depth=10)
        self.pub = self.create_publisher(Int32, 'closer', qos)
        while msg.data == 1:
            dis = dis - 1
            print("Distance : ", dis, "cm")
            if dis <= 5:
                msg_pub = Int32()
                msg_pub.data = dis
                self.pub.publish(msg_pub)
                break
            time.sleep(1)
        dis = 10



if __name__ == '__main__':
    rclpy.init(args=None)
    distance = Distance()
    try:
        rclpy.spin(distance)
    except KeyboardInterrupt:
        distance.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        distance.destroy_node()
        rclpy.shutdown()