import os
import select
import sys
import rclpy
import time

from std_msgs.msg import Header, String, Int32
from geometry_msgs.msg import Twist
from rclpy.qos import QoSProfile

if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

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
    
def main():
    settings = None
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rclpy.init()

    qos = QoSProfile(depth=10)
    node = rclpy.create_node('Bus_Sign')
    pub = node.create_publisher(String, 'bus_come', qos)
    
    
    try:
        while(1):
            key = get_key(settings)
            if key == 'w': #버스 잠시후 도착 신호 받음 
                msg = String()
                msg.data = 'move'
                pub.publish(msg)
                print("move")  
            else:
                if (key == '\x03'):
                    break

    except Exception as e:
        print(e)

    finally:
        if os.name != 'nt':
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


if __name__ == '__main__':
    main() 