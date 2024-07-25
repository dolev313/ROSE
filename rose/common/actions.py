import random

""" Driving actions """

NONE = "none"  # NOQA
RIGHT = "right"  # NOQA
LEFT = "left"  # NOQA
PICKUP = "pickup"  # NOQA
JUMP = "jump"  # NOQA
BRAKE = "brake"  # NOQA

ALL = (NONE, RIGHT, LEFT, PICKUP, JUMP, BRAKE)


def init_actions():
    return random.choices(ALL, k=4)


def update_actions(actions: list, act_taken):
    actions.remove(act_taken)
    actions.append(random.choice(ALL))
