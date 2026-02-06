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
