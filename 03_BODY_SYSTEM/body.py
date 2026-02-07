# body.py

class Body:
    """
    High-level body composition.
    """

    def __init__(self, skeleton=None, muscles=None, nervous_system=None, limbs=None):
        self.skeleton = skeleton
        self.muscles = muscles
        self.nervous_system = nervous_system
        self.limbs = limbs or []


class DevelopmentalBody:
    """
    Developmental body model covering pregnancy -> birth -> infancy.
    """

    def __init__(self, stage="pregnancy"):
        self.stage = stage

        self.energy = 1.0
        self.strain = 0.0
        self.integrity = 1.0
        self.temperature = 0.5

        self.pain = 0.0
        self.comfort = 1.0

        self.posture = "curled"
        self.last_action = None

    def update(self, load=0.0, intake=0.0):
        self.energy = max(0.0, min(1.0, self.energy + intake - load * 0.1))
        self.strain = max(0.0, min(1.0, self.strain + load - 0.05))
        self.integrity = min(1.0, self.integrity + 0.01)

        self.pain = max(0.0, self.strain - self.integrity)
        self.comfort = max(0.0, 1.0 - self.pain)

        if self.stage in ["birth", "infancy"]:
            if self.pain > 0.4:
                self.last_action = "pain_withdrawal"
                self.strain *= 0.7
            else:
                self.last_action = None

    def snapshot(self):
        return {
            "stage": self.stage,
            "energy": self.energy,
            "strain": self.strain,
            "integrity": self.integrity,
            "temperature": self.temperature,
            "pain": self.pain,
            "comfort": self.comfort,
            "posture": self.posture,
            "last_action": self.last_action,
        }
