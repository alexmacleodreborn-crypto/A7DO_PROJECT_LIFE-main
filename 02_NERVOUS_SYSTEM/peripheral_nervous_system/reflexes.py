# peripheral_nervous_system/reflexes.py

class ReflexArc:
    """
    Immediate response without reasoning.
    """

    def __init__(self, name: str = "reflex"):
        self.name = name
        self.active = False

    def activate(self, nervous_ready: bool):
        if nervous_ready:
            self.active = True

    def respond(self, stimulus):
        return {"reflex": stimulus, "active": self.active}
