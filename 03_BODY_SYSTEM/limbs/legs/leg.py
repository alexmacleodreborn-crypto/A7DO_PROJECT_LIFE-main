# limbs/legs/leg.py

from limbs.limb import Limb


class Leg(Limb):
    """
    Leg-specific readiness (weight bearing).
    """

    def __init__(self, side: str):
        super().__init__(f"{side}_leg")
        self.weight_bearing = False

    def update(self, nervous_ready: bool):
        if self.maturity > 0.85 and nervous_ready:
            self.weight_bearing = True
