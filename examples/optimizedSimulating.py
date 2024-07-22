from rose.common import obstacles, actions, config  # NOQA
import time

driver_name = "optimized run time"


class Tree:
    def __init__(self, act=actions.NONE, x=0, y=0, score=0):
        self.act = act
        self.x = x
        self.y = y
        self.score = score
        self.children = []

    def init_children(self, world, layers):
        if layers == 0:
            return
        valid_a = get_actions(world, self.x, self.y)
        for act in valid_a:
            new_x, new_y, cur_score = process(world, self.x, self.y, act, self.score)
            self.children.append(Tree(act, new_x, new_y, cur_score))

        for child in self.children:
            child.init_children(world, layers - 1)

    def append_children(self, world):
        self.y += 1
        if not self.children:
            self.init_children(world, 1)
        else:
            for child in self.children:
                child.append_children(world)

    def get_action(self):
        maxx = 0
        best_child = self

        for child in self.children:
            cur = child.get_max()
            if cur > maxx:
                maxx = cur
                best_child = child

        return best_child

    def get_max(self):
        if not self.children:
            return self.score

        maxx = 0
        for child in self.children:
            maxx = max(maxx, child.get_max())

        return maxx

    def print_tree(self, i):
        if i == 0:
            print("----- printing tree -----")
        print(self.act, self.x, self.y, self.score)
        for child in self.children:
            print("-->" * i, end="")
            child.print_tree(i + 1)


lane: int = 0
initFlag: bool = False
driving_tree = Tree()

iter_num = 0
total_time = 0


def drive(world):
    start = time.time()
    global lane, initFlag, driving_tree, iter_num, total_time
    if not initFlag:
        lane = (world.car.x // 3) * 3
        driving_tree = Tree(actions.NONE, world.car.x, world.car.y, 0)
        driving_tree.init_children(world, 6)
        initFlag = True
    else:
        driving_tree.append_children(world)

    driving_tree = driving_tree.get_action()
    end = time.time()
    total_time += end - start
    iter_num += 1
    print(f"avg reaction time: {total_time / iter_num * 1000}")
    return driving_tree.act


def get_actions(world, x, y):
    valid_a = [actions.NONE]
    if x > lane:
        valid_a.append(actions.LEFT)
    if x < lane + 2:
        valid_a.append(actions.RIGHT)
    if world.get((x, y - 1)) == obstacles.PENGUIN:
        valid_a.append(actions.PICKUP)
    if world.get((x, y - 1)) == obstacles.WATER:
        valid_a.append(actions.BRAKE)
    if world.get((x, y - 1)) == obstacles.CRACK:
        valid_a.append(actions.JUMP)
    return valid_a


def process(world, x, y, action, score):
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
