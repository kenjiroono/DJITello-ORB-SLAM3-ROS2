#!/usr/bin/env python3
from inputs import get_gamepad

# ROS2 imports
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Empty
from geometry_msgs import msg


class GamepadPublisher(Node):
    def __init__(self):
        super().__init__('gamepadPublisher')
        
        self.tello_flying = False

        # Gamepad setup 
        self.joy_min_val = 10000
        self.joy_max_val = 32766
        self.joy_step = (self.joy_max_val - self.joy_min_val) / 100
        self.trigger_step = 2.55 # min=0 ~ max=255 
        self.twist_msg = msg.Twist()

        # Setup data publish 
        self.pub_land = self.create_publisher(Empty, 'land', 1)
        self.pub_takeoff = self.create_publisher(Empty, 'takeoff', 1)
        self.pub_flip = self.create_publisher(String, 'flip', 1)
        self.pub_control = self.create_publisher(msg.Twist, 'control', 1)
        self.pub_emergency = self.create_publisher(Empty, 'emergency', 1)

        self.timer = self.create_timer(0.002, self.timer_callback)

    def timer_callback(self):
        # Get Xbox controller(USB) input and publish geometry_msgs.Twist
        events = get_gamepad()
        for event in events:
            if event.code == 'BTN_WEST' and self.tello_flying == False:
                self.tello_flying = True
                self.pub_takeoff.publish(Empty())
                print(event.ev_type, event.code, event.state)

            elif event.code == 'BTN_SOUTH' and self.tello_flying == True:
                self.tello_flying = False
                self.pub_land.publish(Empty())
                print(event.ev_type, event.code, event.state)

            elif event.code == 'BTN_MODE':
                self.tello_flying = False
                self.pub_emergency.publish(Empty())
                print(event.ev_type, event.code, event.state)

            else:
                self.gamepadControl(event)

    def gamepadControl(self, event):
        # Rotate on Z axis
        if event.code == 'ABS_X':
            if event.state < -self.joy_min_val:
                self.twist_msg.angular.z = (event.state + self.joy_min_val) / self.joy_step
            elif event.state > self.joy_min_val:
                self.twist_msg.angular.z = (event.state - self.joy_min_val) / self.joy_step
            else:
                self.twist_msg.angular.z = 0.0

        # Yaw
        if event.code == 'ABS_RX':
            if event.state < -self.joy_min_val:
                self.twist_msg.linear.x = (event.state + self.joy_min_val) / self.joy_step
            elif event.state > self.joy_min_val:
                self.twist_msg.linear.x = (event.state - self.joy_min_val) / self.joy_step
            else:
                self.twist_msg.linear.x = 0.0

        # Pitch
        if event.code == 'ABS_RY':
            if event.state < -self.joy_min_val:
                self.twist_msg.linear.y = -(event.state + self.joy_min_val) / self.joy_step
            elif event.state > self.joy_min_val:
                self.twist_msg.linear.y = -(event.state - self.joy_min_val) / self.joy_step
            else:
                self.twist_msg.linear.y = 0.0

        # Elevation
        if event.code == 'ABS_Z':
            self.twist_msg.linear.z = event.state / self.trigger_step

        if event.code == 'ABS_RZ':
            self.twist_msg.linear.z = -event.state / self.trigger_step

        self.pub_control.publish(self.twist_msg)



def main(args=None):
    rclpy.init(args=args)
    gamepadPublisher = GamepadPublisher()
    rclpy.spin(gamepadPublisher)
    gamepadPublisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()