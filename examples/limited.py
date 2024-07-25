import copy

from rose.common import obstacles, actions, config  # NOQA
import time

driver_name = "limited"


class Tree:
    def __init__(self, act, x, y, score):
        self.act = act
        self.x = x
        self.y = y
        self.score = score
        self.children = []

    def get_children(self, world, layers, action_list):
        if layers == 0:
            return
        for act in action_list:
            new_x, new_y, cur_score = process(world, self.x, self.y, act, self.score)
            self.children.append(Tree(act, new_x, new_y, cur_score))

        for child in self.children:
            new_list = copy.copy(action_list)
            new_list.remove(child.act)
            child.get_children(world, layers - 1, new_list)

    def get_action(self):
        self.update_scores()
        maxx = 0
        act = actions.NONE

        for child in self.children:
            if child.score > maxx:
                maxx = child.score
                act = child.act

        return act

    def update_scores(self):
        if not self.children:
            return self.score

        maxx = 0
        for child in self.children:
            maxx = max(maxx, child.update_scores())

        self.score = maxx
        return maxx

    # def print_tree(self, i):
    #     print(self.act, self.x, self.y, self.score)
    #     for child in self.children:
    #         print("-->" * i, end="")
    #         child.print_tree(i + 1)
    #         print()


lane: int = 0
laneFlag: bool = False

iter_num = 0
total_time = 0


def drive(world, action_list):
    # start = time.time()
    global lane, laneFlag, iter_num, total_time
    if not laneFlag:
        lane = (world.car.x // 3) * 3
        print("lane: ", lane)
        laneFlag = True

    x, y = world.car.x, world.car.y
    # iter_num = (iter_num + 1) % (config.game_duration)
    driving_tree = Tree(actions.NONE, x, y, 0)
    driving_tree.get_children(world, min(y, config.game_duration - iter_num), action_list)

    # end = time.time()
    # total_time += end - start
    # print(f"avg reaction time: {total_time / (iter_num + 1)* 1000}")
    print(f'action list: {action_list} - played: {driving_tree.get_action()}')
    return driving_tree.get_action()


# def get_actions(x, action_list):
#     if (x == 0 and ):
#         action = actions.NONE
#     if (self.world.car.x == 5 and action == actions.RIGHT):
#         action = actions.NONE
#     return valid_a


def process(world, x, y, action, score):
    if x == 0 and action == actions.LEFT:
        action = actions.NONE
    if x == 5 and action == actions.RIGHT:
        action = actions.NONE
    y -= 1
    if action == actions.LEFT:
        x -= 1
    elif action == actions.RIGHT:
        x += 1

    obstacle = world.get((x, y))

    if obstacle == obstacles.NONE:
        score += config.score_move_forward

    elif obstacle in (obstacles.TRASH, obstacles.BIKE, obstacles.BARRIER):
        score += config.score_move_backward

    elif obstacle == obstacles.CRACK:
        if action == actions.JUMP:
            score += config.score_move_forward + config.score_jump
        else:
            score += config.score_move_backward

    elif obstacle == obstacles.WATER:
        if action == actions.BRAKE:
            score += config.score_move_forward + config.score_brake
        else:
            score += config.score_move_backward

    elif obstacle == obstacles.PENGUIN:
        if action == actions.PICKUP:
            score += config.score_move_forward + config.score_pickup
        else:
            score += config.score_move_forward

    return x, y, score
