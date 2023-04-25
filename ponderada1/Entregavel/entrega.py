#!/usr/bin/env python3
from time import sleep
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist



class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(0.1, self.move_turtle)
        self.twist_msg_ = Twist()

    def move_turtle(self):
        self.twist_msg_.linear.x = 2.3
        self.twist_msg_.angular.z = 0.0
        self.publisher_.publish(self.twist_msg_)
        sleep(1.0) # Intervalo de um segundo para o próximo movimento
        
        # Velocidade angular configurada para 2.4
        self.twist_msg_.linear.x = 0.0
        self.twist_msg_.angular.z = 2.4
        self.publisher_.publish(self.twist_msg_)
        sleep(1.0) # Intervalo de um segundo para o próximo movimento

        self.twist_msg_.linear.x = -2.3
        self.twist_msg_.angular.z = 0.0
        self.publisher_.publish(self.twist_msg_)
        sleep(1.0)


        
            



def main(args=None):
    rclpy.init()
    turtle_controller = TurtleController()
    rclpy.spin(turtle_controller)
    turtle_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
