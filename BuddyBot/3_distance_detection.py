from dis import dis
import RPi.GPIO as gpio
import time
import rclpy

from std_msgs.msg import Header, String, Int32
from rclpy.qos import QoSProfile

gpio.setmode(gpio.BCM)

trig = 13
echo = 19

print("start")

gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)

rclpy.init()
    
qos = QoSProfile(depth=10)
node = rclpy.create_node('distance_detection')
pub = node.create_publisher(Int32, 'closer', qos)

try :
    while True :
      gpio.output(trig, False)
      time.sleep(0.5)

      gpio.output(trig, True)
      time.sleep(0.00001)
      gpio.output(trig, False)

      while gpio.input(echo) == 0 :
        pulse_start = time.time()

      while gpio.input(echo) == 1 :
        pulse_end = time.time()

      pulse_duration = pulse_end - pulse_start
      distance = pulse_duration * 17000
      distance = round(distance, 2)

      msg = Int32()
      pub.publish(msg)
      msg.data = distance
      print("Distance : ", distance, "cm")
except :
    gpio.cleanup()