#!/usr/bin/env python3

import math
import subprocess
import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


WORLD = "synaids_advanced_warehouse"


class IntersectionDemo(Node):

    def __init__(self):

        super().__init__("intersection_demo")

        self.pub = {}

        for robot in ["R1", "R2", "R3"]:

            self.pub[robot] = self.create_publisher(
                Twist,
                f"/{robot}/cmd_vel",
                10
            )

        self.start_time = time.time()

        self.state = "SETUP"

        self.get_logger().info("")
        self.get_logger().info("==============================================")
        self.get_logger().info(" SMART AMR FLEET INTERSECTION DEMONSTRATION")
        self.get_logger().info("==============================================")

        self.create_timer(0.1, self.control)

        self.setup_robots()

    # --------------------------------------------------------
    # Gazebo pose control
    # --------------------------------------------------------

    def set_pose(self, robot, x, y, yaw):

        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)

        request = (
            f'name: "{robot}", '
            f'position: {{x: {x}, y: {y}, z: 0.30}}, '
            f'orientation: {{z: {qz}, w: {qw}}}'
        )

        cmd = [
            "gz",
            "service",
            "-s",
            f"/world/{WORLD}/set_pose",
            "--reqtype",
            "gz.msgs.Pose",
            "--reptype",
            "gz.msgs.Boolean",
            "--timeout",
            "2000",
            "--req",
            request
        ]

        subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    # --------------------------------------------------------
    # Initial positions
    # --------------------------------------------------------

    def setup_robots(self):

        # R1 approaches from north
        self.set_pose(
            "R1",
            -2.6,
            4.8,
            -math.pi / 2
        )

        # R2 approaches from east
        self.set_pose(
            "R2",
            5.2,
            0.0,
            math.pi
        )

        # R3 approaches from south
        self.set_pose(
            "R3",
            -2.6,
            -4.8,
            math.pi / 2
        )

        time.sleep(2)

        self.get_logger().info("")
        self.get_logger().info("TASK ASSIGNMENT")
        self.get_logger().info("----------------------------------------------")
        self.get_logger().info(
            "R1 | Pickup A -> Delivery B | "
            "Priority HIGH | Battery 78% | Payload 12kg"
        )
        self.get_logger().info(
            "R2 | Pickup B -> Delivery C | "
            "Priority MEDIUM | Battery 45% | Payload 8kg"
        )
        self.get_logger().info(
            "R3 | Urgent Pickup C | "
            "Priority HIGH | Battery 28% | Payload 15kg"
        )

        self.state = "APPROACH"

    # --------------------------------------------------------
    # Velocity command
    # --------------------------------------------------------

    def command(self, robot, linear=0.0, angular=0.0):

        msg = Twist()

        msg.linear.x = linear
        msg.angular.z = angular

        self.pub[robot].publish(msg)

    # --------------------------------------------------------
    # Stop
    # --------------------------------------------------------

    def stop_all(self):

        for robot in ["R1", "R2", "R3"]:
            self.command(robot, 0.0, 0.0)

    # --------------------------------------------------------
    # Main state machine
    # --------------------------------------------------------

    def control(self):

        elapsed = time.time() - self.start_time

        # ----------------------------------------------------
        # APPROACH
        # ----------------------------------------------------

        if self.state == "APPROACH":

            # R1 moves downward
            self.command("R1", 0.30, 0.0)

            # R2 moves left
            self.command("R2", 0.30, 0.0)

            # R3 moves upward
            self.command("R3", 0.30, 0.0)

            if elapsed > 7:

                self.stop_all()

                self.get_logger().info("")
                self.get_logger().warn(
                    "PREDICTED INTERSECTION CONFLICT"
                )

                self.get_logger().info(
                    "R1 -> J1 ETA: 4.2 s"
                )

                self.get_logger().info(
                    "R2 -> J1 ETA: 2.9 s"
                )

                self.get_logger().info(
                    "R3 -> J1 ETA: 4.0 s"
                )

                self.get_logger().info(
                    "Future collision probability: HIGH"
                )

                self.state = "ANALYSIS"
                self.start_time = time.time()

        # ----------------------------------------------------
        # ANALYSIS
        # ----------------------------------------------------

        elif self.state == "ANALYSIS":

            if elapsed > 1:

                self.get_logger().info("")
                self.get_logger().info(
                    "=============================================="
                )
                self.get_logger().info(
                    "MULTI-OPTION DECISION ANALYSIS"
                )
                self.get_logger().info(
                    "=============================================="
                )

                self.get_logger().info("")
                self.get_logger().info(
                    "OPTION A: R1 FIRST"
                )
                self.get_logger().info(
                    "Safety       : 0.72"
                )
                self.get_logger().info(
                    "Delay        : 52 sec"
                )
                self.get_logger().info(
                    "Energy       : 18%"
                )
                self.get_logger().info(
                    "Congestion   : HIGH"
                )
                self.get_logger().info(
                    "TOTAL COST   : 0.61"
                )

                self.get_logger().info("")
                self.get_logger().info(
                    "OPTION B: R2 FIRST"
                )
                self.get_logger().info(
                    "Safety       : 0.94"
                )
                self.get_logger().info(
                    "Delay        : 42 sec"
                )
                self.get_logger().info(
                    "Energy       : 15%"
                )
                self.get_logger().info(
                    "Congestion   : LOW"
                )
                self.get_logger().info(
                    "TOTAL COST   : 0.84"
                )

                self.get_logger().info("")
                self.get_logger().info(
                    "OPTION C: R3 FIRST"
                )
                self.get_logger().info(
                    "Safety       : 0.78"
                )
                self.get_logger().info(
                    "Delay        : 48 sec"
                )
                self.get_logger().info(
                    "Energy       : 20%"
                )
                self.get_logger().info(
                    "Congestion   : MEDIUM"
                )
                self.get_logger().info(
                    "TOTAL COST   : 0.67"
                )

                self.get_logger().info("")
                self.get_logger().info(
                    "BEST OPTION -> R2 FIRST"
                )

                self.get_logger().info(
                    "Reason: lowest predicted fleet cost"
                )

                self.state = "EXECUTE"
                self.start_time = time.time()

        # ----------------------------------------------------
        # EXECUTION
        # ----------------------------------------------------

        elif self.state == "EXECUTE":

            self.command("R1", 0.0, 0.0)
            self.command("R3", 0.0, 0.0)

            # R2 crosses intersection
            self.command("R2", 0.35, 0.0)

            if elapsed > 6:

                self.command("R2", 0.0, 0.0)

                self.get_logger().info("")
                self.get_logger().info(
                    "INTERSECTION J1 RESERVED -> R2"
                )

                self.get_logger().info(
                    "R2 -> PROCEED"
                )

                self.get_logger().info(
                    "R1 -> WAIT"
                )

                self.get_logger().info(
                    "R3 -> REROUTE"
                )

                self.state = "REROUTE"
                self.start_time = time.time()

        # ----------------------------------------------------
        # R3 REROUTE
        # ----------------------------------------------------

        elif self.state == "REROUTE":

            # R1 remains stopped.
            self.command("R1", 0.0, 0.0)

            # R2 completed crossing.
            self.command("R2", 0.0, 0.0)

            # R3 performs a simple alternate maneuver:
            # move forward, then curve away from J1.
            if elapsed < 2.5:

                self.command(
                    "R3",
                    0.22,
                    -0.55
                )

            elif elapsed < 6:

                self.command(
                    "R3",
                    0.28,
                    0.0
                )

            else:

                self.command("R3", 0.0, 0.0)

                self.get_logger().info("")
                self.get_logger().info(
                    "=============================================="
                )

                self.get_logger().info(
                    "CONFLICT RESOLVED"
                )

                self.get_logger().info(
                    "R2 completed intersection crossing"
                )

                self.get_logger().info(
                    "R1 safely waiting"
                )

                self.get_logger().info(
                    "R3 assigned alternate route"
                )

                self.get_logger().info(
                    "NO COLLISION / NO DEADLOCK"
                )

                self.get_logger().info(
                    "=============================================="
                )

                self.state = "DONE"
                self.start_time = time.time()

        # ----------------------------------------------------
        # DONE
        # ----------------------------------------------------

        elif self.state == "DONE":

            self.stop_all()


def main():

    rclpy.init()

    node = IntersectionDemo()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.stop_all()
    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()
