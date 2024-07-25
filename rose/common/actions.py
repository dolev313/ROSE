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
    """
    initializing the action list with 4 random actions
    """
    return random.choices(ALL, k=4)


def update_actions(actions: list, act_taken):
    """
    removing the used action from the list and replacing with a new random action
    """
    if act_taken in actions:
        actions.remove(act_taken)
        actions.append(random.choice(ALL))

