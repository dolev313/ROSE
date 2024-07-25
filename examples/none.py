"""
This driver does not do any action.
"""
from rose.common import obstacles, actions  # NOQA

driver_name = "Driver"


def printsome(word):
    print(word)


def drive(world):
    # print("driving")
    # printsome("driving")
    action = find_path(world)
    return action


def find_path(world):
    x_car = world.car.x
    y_car = world.car.y
    obs, pngu = extract_obs(world)
    if pngu != []:
        if x_car == pngu[0][0] and y_car == pngu[0][1] - 1:
            print("picking up")
            return actions.PICKUP
    elif obs != []:
        for i in obs:
            if world.get(i) == obstacles.CRACK:
                return actions._JUMP
            elif world.get(i) == obstacles.WATER:
                return actions.BRAKE
            elif world.get(i) == obstacles.TRASH or world.get(i) == obstacles.BARRIER or world.get(i) == obstacles.BIKE:
                printsome("obs found")
                if x_car > i[0] or x_car == 0:
                    return actions.RIGHT
                elif x_car < i[0] or x_car == 5:
                    return actions.LEFT
                else:
                    return actions.LEFT
    return actions.NONE


def extract_obs(world):
    obs = []
    pngu = []
    x, y = world.car.x, world.car.y
    if 0 <= x <= 2:
        start_check = 0
        end_check = 3
    else:
        start_check = 3
        end_check = 6

    for c in range(start_check , end_check):
        try:
            if world.get((c, y - 1)) == obstacles.PENGUIN:
                pngu.append((c, y - 1))
            elif world.get((c, y - 1)) != obstacles.NONE and world.get((c, y - 1)) != obstacles.PENGUIN:
                obs.append((c, y - 1))
        except IndexError:
            print("error")
    print(obs)
    return obs, pngu
