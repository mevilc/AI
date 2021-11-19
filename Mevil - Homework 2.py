# Mevil Crasta
# CISC 681 Homework 2
# Dr. Rahmat Beheshti
# Due Date: Oct 15, 2021


import math # to use +ve and -ve infinity

def alphabeta(alpha, beta, curr_depth, root_type, terminal_node, visited, index):
  '''
    (int, int, bool, list, int, int) -> list

    Parameters:
    :curr_depth: - The depth at each level. Root -> 0, terminal nodes -> 3
    :index: - the index of the leaf node as found in the terminal_nodes list
    :root_type: if MAX node -> True, if MIN node -> False
    :terminal_nodes: list of leaf nodes
    :alpha: alpha of each node
    :beta: beta of each node

    Returns the list of pruned indices given a list of terimnal nodes from user.
    '''
  
  # if depth == 3, then found the leaf node.
  if curr_depth == 3:
    visited.append(index) # add to visited node
    return terminal_node[index] # return value of leaf node

  # if at root node, then need to check 3 children
  if curr_depth == 0:
    num_child = 3
  # if at depth 1 or 2, then need to check only 2 children
  elif curr_depth > 0:
    num_child = 2

  # if node type is MAX
  if root_type == "MAX NODE":
    max_value = MIN # tracks the best value. For MAX node, the default best value is -ve infinity

    # loops through children using a recursive call, each time increasing the depth + 1
    for child_branch in range(0, num_child):

      # recursive function calls itself until depth == 3.
      # From there, the leaf nodde is returned and the best valuet ill that node is computed.
      # The maximum of the best and default of alpha -> new alpha
      max_value = max(max_value, alphabeta(alpha, beta, curr_depth + 1, "MIN NODE", terminal_node, visited, index * 2 + child_branch))
      alpha = max(alpha, max_value)

      if beta <= alpha:
        break
    return max_value

  # if node is MIN
  elif root_type == "MIN NODE":
    min_value = MAX # the default best value for MIN node is positive infinity
    for child_branch in range(0, num_child):
      min_value = min(min_value, alphabeta(alpha, beta, curr_depth + 1, "MAX NODE", terminal_node, visited, index * 2 + child_branch))
      beta = min(beta, min_value)

      if beta <= alpha:
        break  
    return min_value


# ask user the input
nodes = input("Enter terminal nodes: \n")
terminal_nodes = [int(i) for i in nodes.split() if i.isdigit()] # convert string input to a list of numbers

# set for initial function call. Initially, alpha = min and beta = max
MAX = math.inf
MIN = -math.inf
visited = [] # list of all visited terminal nodes
alphabeta(MIN, MAX, 0, "MAX NODE", terminal_nodes, visited, 0) # function call

# prints the lead node indices not present in visited list
for i in range(0,12):
  if i not in visited:
    print(i, end = ' ')







    



    
    
            




