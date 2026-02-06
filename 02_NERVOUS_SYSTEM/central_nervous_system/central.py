# central_nervous_system/central.py

class CentralNervousSystem:
    """
    Brain + spinal cord maturation and readiness.
    """

    def __init__(self):
        self.brain_maturity = 0.0
        self.spinal_maturity = 0.0
        self.functional = False

    def grow(self, rate: float):
        self.brain_maturity = min(1.0, self.brain_maturity + rate)
        self.spinal_maturity = min(1.0, self.spinal_maturity + rate)
        if self.brain_maturity > 0.7 and self.spinal_maturity > 0.7:
            self.functional = True
