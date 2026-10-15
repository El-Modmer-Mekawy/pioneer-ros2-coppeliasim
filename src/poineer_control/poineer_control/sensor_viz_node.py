#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
import matplotlib.pyplot as plt


class SensorVizNode(Node):
    def __init__(self):
        super().__init__('sensor_viz_node')

        # use_array:=false (default) -> /ultrasonic_sensors is std_msgs/String (CSV)
        # use_array:=true            -> /ultrasonic_sensors is Float32MultiArray
        self.declare_parameter('use_array', False)
        use_array = self.get_parameter('use_array').value


        self.subscription = self.create_subscription(
                String, '/ultrasonic_sensors', self.csv_callback, 10)

        # Store latest 16 sensor readings
        self.num_sensors = 16
        self.sensor_readings = [0.0] * self.num_sensors
        self.sensor_indices = [f'S{i+1}' for i in range(self.num_sensors)]

        # Matplotlib interactive mode
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize=(10, 5))

        # 20 Hz timer to redraw the plot
        self.timer = self.create_timer(0.05, self.update_plot)
        self.get_logger().info(
            f'Sensor Visualization Node Started ({"array" if use_array else "CSV string"} mode). '
            'Waiting for data...')

    def csv_callback(self, msg: String):
        try:
            vals = [float(x) for x in msg.data.split(',')]
        except ValueError:
            self.get_logger().warn('Could not parse sensor message')
            return
        if len(vals) == self.num_sensors:
            self.sensor_readings = vals

    def array_callback(self, msg: Float32MultiArray):
        if len(msg.data) == self.num_sensors:
            self.sensor_readings = list(msg.data)

    def update_plot(self):
        """Timer callback that redraws the bar graph in real time."""
        self.ax.clear()
        colors = ['crimson' if d < 0.8 else 'steelblue' for d in self.sensor_readings]
        self.ax.bar(self.sensor_indices, self.sensor_readings, color=colors, edgecolor='black')
        self.ax.set_ylim(0, 5.5)
        self.ax.set_xlabel('Ultrasonic Sensor Index (1 to 16)')
        self.ax.set_ylabel('Distance Reading (m)')
        self.ax.set_title('Pioneer 3-DX Real-Time Ultrasonic Sensor Readings')
        self.ax.grid(axis='y', linestyle='--', alpha=0.6)
        plt.pause(0.001)


def main(args=None):
    rclpy.init(args=args)
    node = SensorVizNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        plt.close('all')
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()