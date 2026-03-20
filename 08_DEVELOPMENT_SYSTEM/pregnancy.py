# pregnancy.py

GROWTH_RATES = {
    "cellular": 0.01,
    "organ_buds": 0.03,
    "functional": 0.05,
    "integration": 0.02,
}


def pregnancy_tick(body, nervous_system, stage: str):
    """
    Progress limb + nervous system maturation during pregnancy.
    """
    growth_rate = GROWTH_RATES[stage]

    nervous_system.mature(growth_rate)

    for limb in body.limbs:
        limb.grow(growth_rate)
        limb.update(nervous_system.is_motor_ready())


def birth_activation(body):
    """
    Switch on survival-critical systems at birth.
    """
    body.nervous_system.pns.sensory_ready = True
    body.nervous_system.ans.functional = True

    for limb in body.limbs:
        limb.motor_control = True
