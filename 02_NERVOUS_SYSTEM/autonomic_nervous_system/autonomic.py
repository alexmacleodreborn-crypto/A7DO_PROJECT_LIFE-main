# autonomic_nervous_system/autonomic.py

class AutonomicNervousSystem:
    """
    Survival-critical regulation.
    """

    def __init__(self):
        self.sympathetic = 0.0
        self.parasympathetic = 0.0
        self.functional = False

    def grow(self, rate: float):
        self.sympathetic = min(1.0, self.sympathetic + rate)
        self.parasympathetic = min(1.0, self.parasympathetic + rate)
        if self.sympathetic > 0.6 and self.parasympathetic > 0.6:
            self.functional = True
