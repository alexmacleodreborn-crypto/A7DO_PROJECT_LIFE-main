# morphology/muscles.py

class Muscle:
    """
    Generates force at energy cost.
    """

    def __init__(self, strength: float):
        self.strength = strength

    def contract(self, effort: float) -> float:
        if effort > self.strength:
            raise RuntimeError("Muscle overload")
        return effort


class Muscles:
    """
    Aggregate muscle groups for the body.
    """

    def __init__(self):
        self.axial = Muscle(strength=0.5)
        self.limbs = Muscle(strength=0.5)
