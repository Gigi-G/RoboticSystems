#
# test_manipulator.py
#

import sys
sys.path.insert(0, '../../lib')

from models.manipulator import *
from models.robot import *
from gui.three_joints_gui import *

from PyQt5.QtWidgets import QApplication

class ManipulatorRobot(RoboticSystem):

    def __init__(self):
        super().__init__(1e-3) # delta_t = 1e-3
        self.arm = ThreeJointsPlanarArm(0.2, 0.2, 0.02,
                                        0.5, 0.5, 0.5,
                                        0.8)

    def run(self):
        t1 = 4.0
        t2 = 5.0
        t3 = 1.0
        self.arm.evaluate(self.delta_t, t1, t2, t3)
        return True

    def get_joint_positions(self):
        return self.arm.get_joint_positions()

    def get_pose_degrees(self):
        return self.arm.get_pose_degrees()



if __name__ == '__main__':
    robot = ManipulatorRobot()
    app = QApplication(sys.argv)
    ex = ManipulatorWindow(robot)
    sys.exit(app.exec_())
