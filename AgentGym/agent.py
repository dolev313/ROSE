from gym import Env, spaces
import numpy as np
import random



NONE = ""  # NOQA
CRACK = "crack"  # NOQA
TRASH = "trash"  # NOQA
PENGUIN = "penguin"  # NOQA
BIKE = "bike"  # NOQA
WATER = "water"  # NOQA
BARRIER = "barrier"  # NOQA


NONE = 0  # NOQA
RIGHT = 1  # NOQA
LEFT = 2  # NOQA
PICKUP = 3  # NOQA
JUMP = 4  # NOQA
BRAKE = 5  # NOQA


class BasicEnv(Env):
    def __init__(self):
        self.actions = [NONE]*36


    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self):
        pass
