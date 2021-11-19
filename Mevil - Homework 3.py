# Mevil Crasta
# CISC 681 - HW 3
# Nov 13, 2021

import numpy as np
import random
import heapq

random.seed(1)
class Agent:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    @property
    def loc(self):
        return (self.i, self.j)

    def vertical_move(self, dir):
        dir = 1 if dir > 0 else -1
        return Agent(self.i + dir, self.j)

    def horizontal_move(self, dir):
        dir = 1 if dir > 0 else -1
        return Agent(self.i, self.j + dir)
    
    def __repr__(self):
        return str(self.loc)

class QLearning:
    def __init__(self, num_states, num_actions, lr=0.3, discount_factor = 0.1):
        self.q = np.zeros((num_states, num_actions))
        self.a = lr
        self.g = discount_factor

    def update(self, curr_state, action_to_take, reward, next_action_to_take):
        q = self.q 
        a = self.a
        g = self.g
        q[curr_state, action_to_take] = (1 - a)*q[curr_state, action_to_take] + a * (reward + g * np.max(q[next_action_to_take]))


class Maze:
    def __init__(self):
        self.env = np.zeros((4, 4))
        self.track_agent = Agent(3,1)

    def in_bounds(self, i , j):
        ROWS, COLUMNS = 4, 4
        if i >= 0 and i < ROWS and j >= 0 and j < COLUMNS: return True

    @property
    def all_actions(self):
        a = self.track_agent
        return [a.vertical_move(1),  a.vertical_move(-1), a.horizontal_move(1), a.horizontal_move(-1)]

    def compute_possible_moves(self):
        moves = self.all_actions
        return [(m, ii) for ii, m in enumerate(moves) if self.check_valid_new_agent(m)]

    def check_valid_new_agent(self, a):
        return self.agent_in_bounds(a) and self.agent_at_wall(a)

    def agent_in_bounds(self, a):
        return self.in_bounds(a.i, a.j)
    
    def agent_at_wall(self, a): # returns True if agent is not at wall state
        return not self.env[a.i, a.j] == -1

    def get_agent_idx(self, a):
        COLUMNS = 4
        return a.i * COLUMNS + a.j

    def get_reward(self, a):
        if self.check_valid_new_agent(a):
            self.track_agent = a
            if self.has_won(): return 100
            elif self.is_forbidden(): return -100
            else: return -0.1
        return -0.1

    def has_won(self):
        a = self.track_agent
        return self.env[a.i, a.j] == 1

    def is_forbidden(self):
        a = self.track_agent
        return self.env[a.i, a.j] == 2


    def visualize(self):
        if self.agent_in_bounds(self.track_agent):
            e = self.env.copy()
            m = self.track_agent
            e[m.i, m.j] = 6
            print(e)


# This makes the maze with the states
def make_test_maze(goal_state1, goal_state2, forbid_state, wall_state):
    m = Maze()
    e = m.env
    i, j = 0, 0

    for k in (goal_state1, goal_state2, forbid_state, wall_state):
        if k >= 1 and k < 5: i, j = 3, k - 1
        elif k >= 5 and k < 9: i, j = 2, k - 5
        elif k >= 9 and k < 13: i, j = 1, k - 9
        elif k >= 13 and k < 16: i, j = 0, k - 13

        if k == goal_state1 or k == goal_state2: e[i, j] = 1
        elif k == forbid_state: e[i, j] = 2
        if k == wall_state: e[i, j] = -1

    return m


def find_second_max(avoid_index, q, s):
    # get the second largest max q value
    max_q_2 = heapq.nlargest(2, q.q[s])[-1]
    
    for index, q_val in enumerate(q.q[s]):
        if q_val == max_q_2:
            if index != avoid_index:
                max_q_2_index = index
                break
    return max_q_2_index # returns second max q value index


def find_third_max(avoid_index_1, avoid_index_2, q, s):
    max_q_3 = heapq.nlargest(3, q.q[s])[-1]
    # get the third largest max q value action

    for index, q_val in enumerate(q.q[s]):
        if q_val == max_q_3:
            if index != avoid_index_1 and index != avoid_index_2:
                max_q_3_index = index
                break
    return max_q_3_index

def get_adjusted_state(state_to_adjust):
    if state_to_adjust >= 13 and state_to_adjust < 17: state_to_adjust -= 13
    elif state_to_adjust >= 9 and state_to_adjust < 13: state_to_adjust -= 5
    elif state_to_adjust >= 5 and state_to_adjust < 9: state_to_adjust += 3
    elif state_to_adjust >= 1 and state_to_adjust < 5: state_to_adjust += 11
    return state_to_adjust

def main():
  
    get_maze = input()
    maze_states = get_maze.split(" ")
    goal_state1, goal_state2 = int(maze_states[0]), int(maze_states[1])
    forbid_state = int(maze_states[2])
    wall_state = int(maze_states[3])
    
    q = QLearning(16, 4)
    
    for i in range(1000):
        
        m = make_test_maze(goal_state1, goal_state2, forbid_state, wall_state)
        
        #goal_stateA, goal_stateB, forbid_stateA = goal_state1, goal_state2, forbid_state

        goal_stateA = get_adjusted_state(goal_state1)
        goal_stateB = get_adjusted_state(goal_state2)
        forbid_stateA = get_adjusted_state(forbid_state)
        
        # keeping going until you are at a forbidden state or any of the goal states
        while (m.get_agent_idx(m.track_agent) != forbid_stateA) and ( m.get_agent_idx(m.track_agent) != goal_stateA and m.get_agent_idx(m.track_agent) != goal_stateB):
            
            r = random.random()
            if r < 0.5:
                moves = m.compute_possible_moves()
                random.shuffle(moves)
                move, move_idx = moves[0]
                curr_state = m.get_agent_idx(m.track_agent)
                

            else:
                moves = m.all_actions 
                curr_state = m.get_agent_idx(m.track_agent)
                
                # counts the occurences of each element in np array
                unique, counts = np.unique(q.q[curr_state], return_counts=True)

                # Case 1: All q table values are 0 -> check if chosen move is valid. If not, move to next 0.
                if len(unique) == 1 and unique[0] == 0:
                    for i in range(4):
                        move = moves[i]
                        if m.in_bounds(move.i, move.j):
                            move_idx = i
                            break

                # Case 2: Not all q values are 0
                else:
                    # get the first maximum q value and its index
                    max_q = np.max(q.q[curr_state])
                    max_q_index = np.argmax(q.q[curr_state])
                    move = moves[max_q_index]

                    #check if chosen q value move is valid
                    if m.in_bounds(moves[max_q_index].i, moves[max_q_index].j):
                        move_idx = max_q_index

                    #If not valid, keep looking for the next maximum
                    else:
                        max_q_index_2 = find_second_max(max_q_index, q, curr_state)
                        move = moves[max_q_index_2]
                        # check if the next maximum provides a valid action
                        if m.in_bounds(moves[max_q_index_2].i, moves[max_q_index_2].j):
                            move_idx = max_q_index_2

                        # If not valid, keee looking for another maximum 
                        else:
                            max_q_index_3 = find_third_max(max_q_index_2, max_q_index, q, curr_state)
                            move = moves[max_q_index_3]
                            if m.in_bounds(moves[max_q_index_3].i, moves[max_q_index_3].j):
                                move_idx = max_q_index_3

                            else:
                                move_idx = 6 - sum(q.q[curr_state])

                    move = moves[move_idx]

            action_to_take = move_idx
            st = m.get_agent_idx(m.track_agent)
            score = m.get_reward(move)

            reward = score

            next_action_to_take = m.get_agent_idx(move)
            q.update(curr_state, action_to_take, reward, next_action_to_take)
  

    q.q = np.round(q.q, 5)
    print(q.q)

  # Prints best action at each state
    if maze_states[4] == "p":
        actions = {0: "down", 1: "up", 2: "right", 3: "left"}
        seq = {1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "",10 : "",11: "",12: "",13: "",14: "",15: "", 16: ""}

        for i in range(16):
        
            uni, num = np.unique(q.q[i], return_counts=True)
            
            if len(uni) == 1 and uni[0] == 0:
                max_idx = 1
                
            else:
                max_idx1 = np.argmax(q.q[i])
                max_idx2 = -100
                max_idx = max_idx1
                ctr = 0

                while (q.q[i][max_idx] == 0):
                    if ctr >= 1:
                        max_idx = find_third_max(max_idx1, max_idx2, q, i)
                    else:
                        ctr += 1
                        max_idx2 = find_second_max(max_idx1, q, i)
                        max_idx = max_idx2

            for j in range(4):
            # if j = 1 go "up" =1
            # if j = 2 go "right" =2
            # if j = 0 go "down" =3
            # if j = 3 go "left" =4

                if (q.q[i][j] == q.q[i][max_idx]) and (j != max_idx):
                    if ((max_idx == 0) and (j == 1 or j == 2)):
                        max_idx = j
                    elif (max_idx == 2) and (j == 1):
                        max_idx = j
                    elif (max_idx == 3):
                        max_idx = j

            if i >= 12 and i < 16:
                if i - 11 in (goal_state1, goal_state2):
                    seq[i - 11] = "goal"
                elif i - 11 == forbid_state: 
                    seq[i - 11] = "forbid"
                elif i - 11 == wall_state:
                    seq[i - 11] = "wall-square"
                else:
                    seq[i - 11] = actions[max_idx]

            elif i >= 8 and i < 12:
                if i - 3 in (goal_state1, goal_state2):
                    seq[i - 3] = "goal"
                elif i - 3 == forbid_state: 
                    seq[i - 3] = "forbid"
                elif i - 3 == wall_state:
                    seq[i - 3] = "wall-square"
                else:
                    seq[i - 3] = actions[max_idx]

            elif i >= 4 and i < 8:
                if i + 5 in (goal_state1, goal_state2):
                    seq[i + 5] = "goal"
                elif i + 5 == forbid_state: 
                    seq[i + 5] = "forbid"
                elif i + 5 == wall_state:
                    seq[i + 5] = "wall-square"
                else:
                    seq[i + 5] = actions[max_idx]
        
            elif i >= 0 and i < 4:
                if i + 13 in (goal_state1, goal_state2):
                    seq[i + 13] = "goal"
                elif i + 13 == forbid_state: 
                    seq[i + 13] = "forbid"
                elif i + 13 == wall_state:
                    seq[i + 13] = "wall-square"
                else:
                    seq[i + 13] = actions[max_idx]


        for k in seq: print(k, seq[k])

    # Prints q value for each action at given row
    elif maze_states[4] == "q":
        row = int(maze_states[5])
        if row >= 13 and row < 17: row -= 13
        elif row >= 9 and row < 13: row -= 5
        elif row >= 5 and row < 9: row += 3
        elif row >= 1 and row < 5: row += 11
  
        act = {"up" : q.q[row][1], "right" : q.q[row][2], "down" : q.q[row][0], "left" : q.q[row][3]}
        for i in act: print(i, act[i])

  
if __name__ == '__main__':
  main()