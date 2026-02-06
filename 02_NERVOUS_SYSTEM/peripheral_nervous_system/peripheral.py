# peripheral_nervous_system/peripheral.py

class PeripheralNervousSystem:
    """
    Sensory + motor readiness thresholds.
    """

    def __init__(self):
        self.sensory_ready = False
        self.motor_ready = False
        self.maturity = 0.0

    def grow(self, rate: float):
        self.maturity = min(1.0, self.maturity + rate)
        if self.maturity > 0.5:
            self.sensory_ready = True
        if self.maturity > 0.7:
            self.motor_ready = True
