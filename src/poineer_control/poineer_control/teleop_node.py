#!/usr/bin/env python3
import sys
import select
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

INSTRUCTIONS = """
-----------------------------------------
Pioneer 3-DX Keyboard Teleoperation Node
-----------------------------------------
Moving around:
        w
   a    s    d

w/s : forward / backward
a/d : rotate left / right
space : force stop (zero velocity)
q : quit
-----------------------------------------
"""

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        # Create publisher on /cmd_vel topic with queue size 10
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.linear_speed = 0.5   # m/s
        self.angular_speed = 1.0  # rad/s
        self.get_logger().info('Teleop Node Started.')

    def publish_twist(self, linear_x: float, angular_z: float):
       msg = Twist()
       msg.linear.x = linear_x
       msg.angular.z = angular_z
       self.publisher_.publish(msg)
       self.get_logger().info(f'Published Twist: linear_x={linear_x}, angular_z={angular_z}')

def get_key(settings):
    """Reads a single keypress from stdin without blocking."""
    tty.setraw(sys.stdin.fileno())
    # select.select waits up to 0.1s for input
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def main(args=None):
    # Save original terminal settings
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args=args)
    node = TeleopNode()

    print(INSTRUCTIONS)

    try:
        while rclpy.ok():
            key = get_key(settings)
            if key == 'w':
                node.publish_twist(node.linear_speed, 0.0)
            elif key == 's':
                node.publish_twist(-node.linear_speed, 0.0)
            elif key == 'a':
                node.publish_twist(0.0, node.angular_speed)
            elif key == 'd':
                node.publish_twist(0.0, -node.angular_speed)
            elif key == ' ':
                node.publish_twist(0.0, 0.0)
            elif key == 'q' or key == '\x03':  # 'q' or Ctrl+C
                node.publish_twist(0.0, 0.0)
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Always restore terminal state and stop robot on exit
        node.publish_twist(0.0, 0.0)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()