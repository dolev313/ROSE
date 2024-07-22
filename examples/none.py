"""
This driver does not do any action.
"""

from rose.common import obstacles, actions  # NOQA

driver_name = "Driver"


def drive(world):
    action = find_path(world)
    return action


def find_path(world):
    x_car = world.car.x
    y_car = world.car.y
    if world.get((world.car.x, world.car.y - 1)) == obstacles.PENGUIN:
        return actions.PICKUP

    obs, pngu = extract_obs(world)
    if pngu != []:
        if x_car == pngu[0][0]:
            return actions.NONE
        elif x_car > pngu[0][0]:
            return actions.LEFT
        else:
            return actions.RIGHT
    elif obs != []:
        for i in obs:
            if world.get(i) == obstacles.CRACK:
                return actions.JUMP
            if world.get(i) == obstacles.WATER:
                return actions.BRAKE
            else:
                if x_car > i[0]:
                    return actions.RIGHT
                else:
                    return actions.LEFT
    elif obs == [] and pngu == []:
        return actions.NONE
    return actions.NONE


def extract_obs(world):
    obs = []
    pngu = []
    x, y = world.car.x, world.car.y
    start_check = max(0, x - 1)
    end_check = min(6, x + 1)

    for c in range(start_check, end_check):
        if world.get((c, y - 1)) == obstacles.PENGUIN:
            pngu.append((c, y - 1))
        elif (
            world.get((c, y - 1)) != obstacles.NONE
            and world.get((c, y - 1)) != obstacles.PENGUIN
        ):
            obs.append((c, y - 1))
    return obs, pngu
