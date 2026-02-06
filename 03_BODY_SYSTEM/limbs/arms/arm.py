# limbs/arms/arm.py

from limbs.limb import Limb


class Arm(Limb):
    """
    Arm-specific readiness (grasping).
    """

    def __init__(self, side: str):
        super().__init__(f"{side}_arm")
        self.hand_grasp = False

    def update(self, nervous_ready: bool):
        if self.maturity > 0.8 and nervous_ready:
            self.hand_grasp = True
