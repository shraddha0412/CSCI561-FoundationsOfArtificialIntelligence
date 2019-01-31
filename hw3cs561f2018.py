import numpy as np
from copy import deepcopy

input_f = open('input.txt', 'r')
directions = [(1,0), (0, 1), (-1, 0), (0, -1)]
priorities = {(0, -1): 1, (0, 1): 2, (1, 0): 3, (-1, 0): 4}


def move_update(x, y, move):
    pos_backup = [x,y]
    yy = y
    xx = x
    yy += move[0]
    xx += move[1]
    if xx < 0 or xx >= grid_size or yy < 0 or yy >= grid_size :
        return pos_backup
    else:
        return [xx,yy]


def turn_left(move):
    ind = directions.index(move) - 1
    if ind < 0:
        ind = 3
    return directions[ind]


def turn_right(move):
    ind = directions.index(move) + 1
    if ind > 3:
        ind = 0
    return directions[ind]


def get_best(state, seq, U, mdp):
    best = seq[0]
    best_score = -np.float64(sum(i * U[j] for (i, j) in mdp.T(state, best)))

    for x in seq:
        score = -np.float64(sum(i * U[j] for (i, j) in mdp.T(state, x)))
        if score < best_score or (score == best_score and priorities.get(best) > priorities.get(x)):
            best = x
            best_score = score
    return best


def value_iteration(mdp):
    nextU = {s: 0 for s in mdp.states}
    R = mdp.R
    T = mdp.T
    while True:
        U = nextU.copy()
        delta = 0
        for state in mdp.states:
            nextU[state] =np.float64(0.9 * max(sum(s*U[a] for (s, a) in T(state, action)) for action in mdp.get_actions(state)) + R(state))
            delta = max(delta, abs(nextU[state] - U[state]))
        if delta <= 0.1*(1 - 0.9)/0.9:
            return U


def get_best_policy(mdp, U):
    policy = [[0] * grid_size for i in range(grid_size)]
    for state in mdp.states:
        policy[state[0]][state[1]] = get_best(state, mdp.get_actions(state), U, mdp)
    return policy


class MDP:
    def __init__(self, world, terminals):
        self.terminals = terminals
        states = set()
        reward = {}
        for i in range(len(world[0])):
            for j in range(len(world)):
                if world[j][i]:
                    states.add((i, j))
                    reward[(i, j)] = world[j][i]
        self.states = states
        self.reward = reward or {s: 0 for s in self.states}
        self.actions = directions
        transitions = {}
        for state in states:
            transitions[state] = {}
            for action in self.actions:
                if action:
                    transitions[state][action] = [(0.7, self.get_move(state, action)),
                                                  (0.1, self.get_move(state, turn_right(action))),
                                                  (0.1, self.get_move(state, turn_left(action))),
                                                  (0.1, self.get_move(state, turn_left(turn_left(action))))
                                                  ]
                else:
                    transitions[state][action] = [(0.0, state)]
        self.transitions = transitions or {}

    def get_move(self, state, direction):
        new_state = state[0]+direction[0], state[1]+direction[1]
        if new_state in self.states:
            return new_state
        else:
            return state

    def get_actions(self, state):
        if state in self.terminals:
            return [None]
        else:
            return self.actions

    def R(self, state):
        return self.reward[state]

    def T(self, state, action):
        if action:
            return self.transitions[state][action]
        else:
            return [(0.0, state)]


grid_size = int(input_f.readline().strip('\n'))
num_cars = int(input_f.readline().strip('\n'))
world = [[-1] * grid_size for i in range(grid_size)]

num_obstacles = int(input_f.readline().strip('\n'))
loc_obstacles = []
for i in range(num_obstacles):
    line = input_f.readline().strip('\n')
    l_arr = line.split(",")
    y = int(l_arr[0])
    x = int(l_arr[1])
    loc_obstacles.append([x, y])
    world[x][y] = -101

world_utility = []
start_cars = []
for i in range(num_cars):
    line = input_f.readline().strip('\n')
    l_arr = line.split(",")
    y = int(l_arr[0])
    x = int(l_arr[1])
    start_cars.append([x,y])


end_cars = []
for i in range(num_cars):
    line = input_f.readline().strip('\n')
    l_arr = line.split(",")
    y = int(l_arr[0])
    x = int(l_arr[1])
    end_cars.append([x, y])
    world_cpy = deepcopy(world)
    if world_cpy[x][y] == -101:
        world_cpy[x][y] = -1
    else:
        world_cpy[x][y] = 99
    world_utility.append(world_cpy)

op = []
for i in range(num_cars):
    final_utility = 0
    ex = end_cars[i][0]
    ey = end_cars[i][1]
    if start_cars[i] == end_cars[i]:
        op.append(str(1 + world_utility[i][ex][ey]))
        continue
    mdp = MDP(world_utility[i], [(ey, ex)])
    policies = get_best_policy(mdp, value_iteration(mdp))

    for j in range(10):
        x = start_cars[i][0]
        y = start_cars[i][1]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k = 0
        utility = 0

        while [x, y] != end_cars[i]:
            swerve[k] = np.float64(swerve[k])
            move = policies[y][x]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn_right(turn_right(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)
            k += 1
            pos = move_update(x, y , move)
            x = pos[0]
            y = pos[1]
            utility += world_utility[i][x][y]
        final_utility += utility
    final_utility /= 10.0
    op.append(str(int(np.floor(final_utility))))
open('output.txt', 'w').write("\n".join(op)+"\n")
