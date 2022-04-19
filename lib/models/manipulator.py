#
# manipulator.py
#


import math
from data.geometry import *

GRAVITY = 9.81

class ArmElement:

    def __init__(self, _L, _M, _b):
        self.w = 0
        self.theta = 0
        self.L = _L
        self.M = _M
        self.b = _b

    def evaluate(self, delta_t, _input_torque):
        w = self.w - GRAVITY * delta_t * math.cos(self.theta) - \
            (self.b * delta_t * self.w * self. L) / self.M + \
            delta_t * _input_torque / (self.M * self.L)
        self.theta = self.theta + delta_t * self.w
        self.w = w

    def get_pose(self):
        return (self.L * math.cos(self.theta), self.L * math.sin(self.theta) )

# --------------------------------------------------------------------------------

class ThreeJointsPlanarArm:

    def __init__(self, _L1, _L2, _L3, _M2, _M3, _Mend, _b):
        self.element_1 = ArmElement(_L1, _M2 + _M3 + _Mend, _b)
        self.element_2 = ArmElement(_L2, _M3 + _Mend, _b)
        self.element_3 = ArmElement(_L3, _Mend, _b)

    def evaluate(self, delta_t, _T1, _T2, _T3):
        self.element_1.evaluate(delta_t, _T1)
        self.element_2.evaluate(delta_t, _T2)
        self.element_3.evaluate(delta_t, _T3)

    def get_pose_degrees(self):
        return ( math.degrees(self.element_1.theta),
                 math.degrees(self.element_2.theta),
                 math.degrees(self.element_3.theta) )

    def get_pose(self):
        (x1, y1) = self.element_1.get_pose()

        (_x2, _y2) = self.element_2.get_pose()
        (x2, y2) = local_to_global(x1, y1, self.element_1.theta, _x2, _y2)

        alpha = self.element_1.theta + self.element_2.theta + self.element_3.theta
        (x3, y3) = local_to_global(x2, y2, alpha, self.element_3.L, 0)

        return [ (x1, y1), (x2, y2), (x3, y3) ]

