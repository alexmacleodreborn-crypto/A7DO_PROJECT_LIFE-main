# nervous_system.py

from central_nervous_system.central import CentralNervousSystem
from peripheral_nervous_system.peripheral import PeripheralNervousSystem
from autonomic_nervous_system.autonomic import AutonomicNervousSystem


class NervousSystem:
    """
    Central + peripheral + autonomic wiring.
    """

    def __init__(self):
        self.cns = CentralNervousSystem()
        self.pns = PeripheralNervousSystem()
        self.ans = AutonomicNervousSystem()

    def mature(self, rate: float):
        self.cns.grow(rate)
        self.pns.grow(rate)
        self.ans.grow(rate)

    def is_motor_ready(self) -> bool:
        return self.cns.functional and self.pns.motor_ready
