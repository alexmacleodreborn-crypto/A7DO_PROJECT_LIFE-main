# limbs/limb.py

class Limb:
    """
    Base limb growth + readiness state.
    """

    def __init__(self, name: str):
        self.name = name
        self.present = False
        self.maturity = 0.0
        self.muscle_strength = 0.0
        self.range_of_motion = 0.0
        self.motor_control = False

    def grow(self, rate: float):
        self.maturity = min(1.0, self.maturity + rate)
        self.muscle_strength = min(1.0, self.muscle_strength + rate)
        self.range_of_motion = min(1.0, self.range_of_motion + rate)
        if self.maturity > 0.2:
            self.present = True
        if self.maturity > 0.7:
            self.motor_control = True
