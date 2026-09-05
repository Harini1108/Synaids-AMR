import math
import rclpy

from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist


class FleetCoordinator(Node):

    def __init__(self):
        super().__init__('fleet_coordinator')

        self.robots = {
            'R1': None,
            'R2': None,
            'R3': None
        }

        self.priority = {
            'R1': 3,
            'R2': 2,
            'R3': 1
        }

        self.prediction_time = 3.0
        self.warning_distance = 2.0
        self.conflict_distance = 1.0

        self.last_status = {}
        self.cmd_publishers = {}

        for robot in ['R1', 'R2', 'R3']:

            self.create_subscription(
                Odometry,
                f'/{robot}/odom',
                lambda msg, r=robot: self.odom_callback(r, msg),
                10
            )

            self.cmd_publishers[robot] = self.create_publisher(
                Twist,
                f'/{robot}/cmd_vel',
                10
            )

        self.timer = self.create_timer(
            0.2,
            self.detect_conflicts
        )

        self.get_logger().info(
            'PREDICTIVE FLEET COORDINATOR ACTIVE'
        )

    def odom_callback(self, robot, msg):
        self.robots[robot] = {
            'x': msg.pose.pose.position.x,
            'y': msg.pose.pose.position.y,
            'vx': msg.twist.twist.linear.x,
            'vy': msg.twist.twist.linear.y
        }

    def stop_robot(self, robot):
        msg = Twist()
        msg.linear.x = 0.0
        msg.linear.y = 0.0
        msg.angular.z = 0.0
        self.cmd_publishers[robot].publish(msg)

    def detect_conflicts(self):

        pairs = [
            ('R1', 'R2'),
            ('R1', 'R3'),
            ('R2', 'R3')
        ]

        for a, b in pairs:

            if self.robots[a] is None or self.robots[b] is None:
                continue

            ra = self.robots[a]
            rb = self.robots[b]

            dx = rb['x'] - ra['x']
            dy = rb['y'] - ra['y']

            distance = math.hypot(dx, dy)

            future_ax = ra['x'] + ra['vx'] * self.prediction_time
            future_ay = ra['y'] + ra['vy'] * self.prediction_time

            future_bx = rb['x'] + rb['vx'] * self.prediction_time
            future_by = rb['y'] + rb['vy'] * self.prediction_time

            predicted_distance = math.hypot(
                future_bx - future_ax,
                future_by - future_ay
            )

            if distance <= self.conflict_distance:
                status = 'CONFLICT'
            elif predicted_distance <= self.conflict_distance:
                status = 'PREDICTED_CONFLICT'
            elif distance <= self.warning_distance:
                status = 'WARNING'
            else:
                status = 'SAFE'

            pair = f'{a}<->{b}'

            if self.last_status.get(pair) != status:

                self.last_status[pair] = status

                self.get_logger().info(
                    f'{pair} | '
                    f'CURRENT={distance:.2f}m | '
                    f'PREDICTED={predicted_distance:.2f}m | '
                    f'STATUS={status}'
                )

            if status in ['CONFLICT', 'PREDICTED_CONFLICT']:

                if self.priority[a] > self.priority[b]:
                    winner = a
                    loser = b
                else:
                    winner = b
                    loser = a

                self.stop_robot(loser)

                action_key = pair + '_ACTION'

                if self.last_status.get(action_key) != loser:

                    self.last_status[action_key] = loser

                    self.get_logger().warn(
                        f'CONFLICT RESPONSE: '
                        f'{winner} PRIORITY > {loser} | '
                        f'{loser} STOPPED'
                    )


def main(args=None):

    rclpy.init(args=args)

    node = FleetCoordinator()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == '__main__':
    main()
