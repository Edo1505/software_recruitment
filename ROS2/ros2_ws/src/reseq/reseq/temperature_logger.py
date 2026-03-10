import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

# Define the TemperatureLogger node
class TemperatureLogger(Node):
    def __init__(self, log_file):

        self.filename = log_file

        super().__init__('temperature_logger')
        self.subscription = self.create_subscription(
            Float32,
            '/temperature',
            self.temperature_callback,
            10)
        

    def temperature_callback(self, msg):
        temperature = msg.data
        if temperature > 50.0:
            log = f"temperature detected: {temperature:.2f}°C"
            self.get_logger().info(log)

            with open(self.filename, "a") as f:
                    f.write(f"{log}\n")

def main(args=None):
    rclpy.init(args=args)

    logger = TemperatureLogger("log.txt")

    rclpy.spin(logger)

    logger.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
