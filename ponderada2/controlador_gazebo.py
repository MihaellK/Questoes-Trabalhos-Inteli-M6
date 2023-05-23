import csv
import rclpy

from rclpy.node import Node

from turtlesim.msg import Pose 
from geometry_msgs.msg import Twist
from collections import deque

from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion

MAX_DIFF = 0.1


class MissionControl(deque):
    def __init__(self, csv_file="pontos.csv"):
        super().__init__()
        with open(csv_file) as csv_file_var:
            csv_reader = csv.reader(csv_file_var, delimiter=',')
            for row in csv_reader:
                new_pose = Pose()
                new_pose.x, new_pose.theta = [float(x) for x in row]
                self.enqueue(new_pose)

    def enqueue(self, x):
        super().append(x)

    def dequeue(self):
        return super().popleft()

class Pose():
    def __init__(self, x=0.0, y=0.0, theta=0.0):
        self.x = x
        self.y = y
        self.theta = theta
    def __repr__(self):
        return f'(x={self.x:.2f}, y={self.y:.2f}, theta={self.theta:.2f})'
    
    # retorna quando 2 poses(classe) são adicionadas '+'
    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        self.theta += other.theta
        return self

    # retorna quando 2 poses(classe) são subtraidas '-'
    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        self.theta -= other.theta
        return self

class TurtleController(Node):
    def __init__(self, mission_control, control_period=0.02):
        super().__init__('turtlecontroller')
        # pose inicial
        self.pose = Pose(x=-40.0)
        # instanciando definidor de posição
        self.setpoint = Pose(x=-40.0)
        # Mission control
        self.mission_control = mission_control
        self.publisher = self.create_publisher(
            msg_type=Twist,
            topic='/cmd_vel',
            qos_profile=10
        )
        # subscrição
        self.subscription = self.create_subscription(
            msg_type=Odometry,
            topic='/odom',
            callback=self.pose_callback,
            qos_profile=10
        )
        self.control_timer = self.create_timer(
            timer_period_sec=control_period,
            callback=self.control_callback
        )

    def control_callback(self):
        if self.pose.x == -40.0:
            self.get_logger().info("Aguardando primeira pose...")
            return
        msg = Twist()
        # var armazena a diff da pos atual e da setada
        x_diff = self.setpoint.x - self.pose.x
        y_diff = self.setpoint.y - self.pose.y
        z_diff = self.setpoint.theta - self.pose.theta
        if self.pose == self.setpoint:
            msg.linear.x, msg.linear.y = 0.0, 0.0
            self.update_setpoint()
        if abs(x_diff) > MAX_DIFF:
            msg.linear.x = 0.5 if x_diff > 0 else -0.5
        else:
            msg.linear.x = 0.0
        if abs(z_diff) > MAX_DIFF:
            msg.angular.z = 0.5 if y_diff > 0 else -0.5
        else:
            msg.angular.z = 0.0

        self.publisher.publish(msg)

    def update_setpoint(self):
        try:
            self.setpoint = self.pose + self.mission_control.dequeue()
            self.get_logger().info(f"Cheguei em {self.pose}, vou para {self.setpoint}")
        except IndexError:
            self.get_logger().info("O trajeto finalizou")
            exit()


    def pose_callback(self, msg: Odometry):
        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z
        _, _, theta = euler_from_quaternion([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y, msg.pose.pose.orientation.z, msg.pose.pose.orientation.w])

        self.pose = Pose(x=x,  y=y, theta=theta)
        if self.setpoint.x == -40.0:
            self.update_setpoint()
        self.get_logger().info(f'A tartaruga está em x={x}, y={y}, theta={z}')


def main(args=None):
    rclpy.init(args=args)
    mc = MissionControl()
    tc = TurtleController(mc)
    rclpy.spin(tc)
    tc.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()