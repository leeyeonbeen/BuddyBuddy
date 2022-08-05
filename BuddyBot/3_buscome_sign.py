import os
import select
import sys
import rclpy
import time
import threading
from rclpy.node import Node

from std_msgs.msg import Header, String, Int32
from geometry_msgs.msg import Twist
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

def get_key(settings):
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        tty.setraw(sys.stdin.fileno())
        rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
        if rlist:
            key = sys.stdin.read(1)
        else:
            key = ''

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        return key
        
class Bus_recognition(Node):
    def __init__(self):
        super().__init__('bus_recognition')
        qos_profile = QoSProfile(depth=10)
        self.bus_recognition = self.create_subscription(String,'bus_recognition',self.move_turtle,qos_profile)
        

    def move_turtle(self, msg):
        settings = None
        if os.name != 'nt':
            settings = termios.tcgetattr(sys.stdin)

        qos = QoSProfile(depth=10)
        #self.node = rclpy.create_node('teleop_keyboard')
        self.pub = self.create_publisher(String, 'bus_come', qos)
    
        self.get_logger().info('Received message: {0}'.format(msg.data))

        try:
            while(1):
                key = get_key(settings)
                if key == 's': #예약 완료 신호가 보내지면 두리번거리기
                    msg = String()
                    msg.data = 'move'
                    self.pub.publish(msg)
                    print("move")
                elif msg.data == 'bus_recognition': #버스를 인식하면 버스 앞까지 가기
                    msg = String()
                    msg.data = 'bus_arrive'
                    self.pub.publish(msg)
                    print("bus arrive")
                    time.sleep(4)
                
                    msg.data = 'stop'
                    self.pub.publish(msg)
                    print("stop")
                    time.sleep(3)
            
                    msg.data = 'turn'
                    self.pub.publish(msg)
                    print("turn")   
                    time.sleep(4)
                
                    msg.data = 'back'
                    self.pub.publish(msg)
                    print("back")
                    time.sleep(4)
                
                    msg.data = 'turn'
                    self.pub.publish(msg)
                    print("turn")  
                    time.sleep(4)
                
                    msg.data = 'stop'
                    self.pub.publish(msg)
                    print("stop")           
                else:
                    if (key == '\x03'):
                        break

        except Exception as e:
            print(e)

        finally:
            if os.name != 'nt':
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    rclpy.init(args=None)
    bus_recognition = Bus_recognition()
    try:
        rclpy.spin(bus_recognition)
    except KeyboardInterrupt:
        bus_recognition.get_logger().info('Keyboard Interrupt (SIGINT)')
    finally:
        bus_recognition.destroy_node()
        rclpy.shutdown()  