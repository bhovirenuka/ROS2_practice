#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


import sys

from PySide6.QtWidgets import (
    QMainWindow, QApplication,
    QLabel, QCheckBox, QComboBox, QListWidget, QLineEdit,
    QLineEdit, QSpinBox, QDoubleSpinBox, QSlider
)
from PySide6.QtCore import Qt,QRunnable, Slot, QThreadPool, QTimer, QObject, Signal
from PySide6.QtGui import QPixmap

GUI_NODE_NAME = "gui_node"
TOPIC_1_NAME = "robot_news"


class GUINode(Node):
    def __init__(self):
        super().__init__(GUI_NODE_NAME)


class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    '''
    message = Signal(object)


        

class Worker(QRunnable):
    '''
    Worker thread
    '''
    def __init__(self):
        super(Worker, self).__init__()

        self.signals = WorkerSignals()

    @Slot()  # QtCore.Slot
    def run(self):
      
        print("Thread start")
      
        self.node = GUINode()


        self.node.subscriber_ = self.node.create_subscription(
            String, TOPIC_1_NAME, self.callback_show_node1_data, 10)
        self.node.get_logger().info(GUI_NODE_NAME + " has been started!1")

        rclpy.spin(self.node)
        rclpy.shutdown()
       
        print("Thread complete")

    def callback_show_node1_data(self, msg):
         self.node.get_logger().info(msg.data)
         self.signals.message.emit(msg.data)




class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My GUI App")
        self.widget = QLabel("Hello")
        font = self.widget.font()
        font.setPointSize(30)
        self.widget.setFont(font)
        self.widget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.setCentralWidget(self.widget)
        
        worker = Worker()
        self.threadpool = QThreadPool()
        self.threadpool.start(worker)

        worker.signals.message.connect(self.callback_showMessage)

    
    def callback_showMessage(self, message):
        #print("%s" % message)
        self.widget.setText(message)




def main(args=None):
    rclpy.init(args=args)

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


if __name__ == "__main__":
    main()