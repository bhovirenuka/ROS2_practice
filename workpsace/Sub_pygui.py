import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from std_msgs.msg import String
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
minimal_subscriber = MinimalSubscriber()
executor = MultiThreadedExecutor()        
print("HMI preparation complete")
gui = QMainWindow()

gui.setWindowTitle("Test ROS2 GUI")
gui.setGeometry(100, 100, 240, 240)
        #gui.move(100, 100)
value_label = 'Value'
button = QPushButton("Button", parent=gui)
button.move(60, 10)
button.clicked.connect(minimal_subscriber.listener_callback)
rclpy.spin(minimal_subscruber)
app = QApplication(sys.argv)
gui.show()                                                
#print("HMI preparation complete")
app.exec_()
rclpy.spin(minimal_subscruber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
minimal_subcriber.destroy_node()
rclpy.shutdown()


if __name__ == '__main__':
    main()


    