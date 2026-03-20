# motor_control/gross_motor.py

class GrossMotor:
    """
    Walking, reaching, lifting.
    """

    def __init__(self):
        self.last_action = None

    def execute(self, command: str):
        self.last_action = command
        return {"gross_motor": command}
