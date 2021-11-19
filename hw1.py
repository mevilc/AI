#############################################
# Mevil Crasta
# CISC 681 - Homework 1
# Due Date: Sept. 28, 2021
# Dr. Beheshtmi
#############################################


# -----------------------------------------------------------------------------------
# Main Part - 1 (Part 2 at bottom)
# -----------------------------------------------------------------------------------

# ask user input - #C#C#C#C-X
user_input = input("Enter the pancake arrangement: \n")
start_node = user_input[:8] # splicing string to take initial pancake arrangement
search_method = user_input[-1] # splicing string to take search approach
goal = "1w2w3w4w"

# -----------------------------------------------------------------------------------
# In this function, a node is flipped at the 1st, 2nd, 3rd, and 4th 
# place. For the first pancake flip, the first two characters
# are flipped and the rest of the unchanged string is added to
# together  - from 1w2b3w4b to 1b + 2b3w4b for 1st flip and so on.
# -----------------------------------------------------------------------------------

def make_children(node_to_add): 
    '''(str) -> list
    Returns a list of all the children that is added to a node'''

    child1, child2, child3, child4 = "", "", "", "" # Initialize children
    seg1, seg2, seg3, seg4 = "", "", "", "" # Initialize segments

    listOfChildren = [] # function returns this list

    #---------------SEGMENTS----------------
    for i in range (0, 2):
        seg4 = seg4 + node_to_add[i]

    for i in range (0, 4):
        seg1 = seg1 + node_to_add[i]
    
    for i in range (0, 6):
        seg2 = seg2 + node_to_add[i]
        
    for i in range (0, 8):
        seg3 = seg3 + node_to_add[i]
    #------------------------------

    # these lengths helps traverse through the node, only looking for #s
    length1 = int(len(seg1)/2)
    length2 = int(len(seg2)/2)
    length3 = int(len(seg3)/2)

    # add the penultimate number to newstr
    child4 = child4 + seg4[0]
    # changes the w/b side after flipping a pancake
    if (seg4[1] == 'b'):
        child4 = child4 + 'w'
    elif (seg4[1] == 'w'):
        child4 = child4 + 'b'
    child4 = child4 + node_to_add[2:] # adds unchanged string to flipped
    listOfChildren.append(child4)

    for i in range(length1):
        # add the penultimate number to newstr
        child1 = child1 + seg1[-2]
        # flip the last character of newstr
        if (seg1[-1] == 'b'):
            child1 = child1 + 'w'
        elif (seg1[-1] == 'w'):
            child1 = child1 + 'b'
        seg1 = seg1[:-2]
    child1 = child1 + node_to_add[4:]
    listOfChildren.append(child1)

    for i in range(length2):
        # add the penultimate number to newstr
        child2 = child2 + seg2[-2]
        # flip the last character of newstr
        if (seg2[-1] == 'b'):
            child2 = child2 + 'w'
        elif (seg2[-1] == 'w'):
            child2 = child2 + 'b'
        seg2 = seg2[:-2]
    child2 = child2 + node_to_add[6:]
    listOfChildren.append(child2)

    for i in range(length3):
        # add the penultimate number to newstr
        child3 = child3 + seg3[-2]
        # flip the last character of newstr
        if (seg3[-1] == 'b'):
            child3 = child3 + 'w'
        elif (seg3[-1] == 'w'):
            child3 = child3 + 'b'
        seg3 = seg3[:-2]
    listOfChildren.append(child3)

    return listOfChildren


# -----------------------------------------------------------------------------------
# In this function, a tree is intialized and a root is given to add to tree.
# Tree is a dictionary.
# -----------------------------------------------------------------------------------

def build_tree(root, goal):
    '''(str, str) -> dict
    Returns a complete tree, which is represented as a dictionary,
    starting from root node and terminates after reaching goal. '''
    
    # 1) Make a tree dictionary
    tree = dict()

    # 2) Check if root is equal to goal. If so, stop building tree
    if (root == goal):
        tree = {root:[]}
        return tree
        
    # 3) If not, expand root and populate tree with first set of children
    # make children() returns a list of chldren from the initial root node.
    root_children = make_children(root)
    tree = {root:[]}
    tree[root] = root_children # adding those initial children to tree

    # using this list to add the intial set of children. Will use this
    # to make these children as nodes, and keep adding their children until
    # each children becomes a new node, until the above if condition is satisfied.
    # this will change throughout the course of the loop.
    list_of_keys = [root_children] 

    for child_list in list_of_keys:
        for child in child_list:
            if (child == goal):
                tree[child] = []
                return tree
            grandchildren = make_children(child) # making 2nd, 3rd, 4th, etc.. n-th level of children
            tree[child] = grandchildren
            list_of_keys.append(grandchildren)
    
    return tree


# -----------------------------------------------------------------------------------
# BFS Implementation
# -----------------------------------------------------------------------------------


'''
Implements the Breadth-first search algorithm

Arguments: 
Map as a graph dictionary, G_dict
Start location, start_node
Goal location, goal_node

Returns:
bfs_route, which is a list of nodes [start_node, ..., goal_node]
'''
bfs_route = [] # keeps track of nodes visited to state goal by bfs
visited_2 = set() # keeps track of all nodes visited in order to find goal

# This approach uses a queue to keep track of the breadth-wise paths and a set to track the visited nodes
def bfs(mapDict, start, end):
    '''(dict, str, str) -> list
    Returns the path from start to end (goal) using BFS algorithm. '''
    
    queue = [[start]]
    while queue:
        route = queue.pop(0)
        node = route[-1] # Get the last node in the route
        if node == end:
            return route
        elif node not in visited_2:
            # create a new path by visiting adjacent nodes and appending to the queue
            for neighbour in mapDict.get(node, []):
                newRoute = list(route)
                newRoute.append(neighbour)
                queue.append(newRoute)
            visited_2.add(node) #after looking through breadth-wise add it as visited



# -----------------------------------------------------------------------------------
# Following Functions relate to A star implementation
# -----------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------
# Function returns heuristic of a node by getting the largest ID out of place.
# -----------------------------------------------------------------------------------

def assign_h_val(neighbour):
    '''(str) -> list
    Returns the maximum ID out of place (heuristic). '''
    
    return_h_max = [] # keep track of all ID's out of place
    if int(neighbour[0]) != 1: # if index is not equal to element, then its out of place
        return_h_max.append(neighbour[0])
    if int(neighbour[2]) != 2:
        return_h_max.append(neighbour[2])
    if int(neighbour[4]) != 3:
        return_h_max.append(neighbour[4])
    if int(neighbour[6]) != 4:
        return_h_max.append(neighbour[6])

    if len(return_h_max) != 0:
        return int(max(return_h_max)) # max of all the out-of-place ID = heuristic
    else:
        return 0
  
# -----------------------------------------------------------------------------------
# Function returns actual cost. Index 0 -> flipped 1, index 1 -> flipped twice, etc..
# -----------------------------------------------------------------------------------

def assign_g_val(child, parent):
    '''(str, dict, str) -> int
    Returns actual cost of flipping. '''

    if parent[2:] == child[2:]:
        g = 1
    elif parent[4:] == child[4:]:
        g = 2
    elif parent[6:] == child[6:]:
        g = 3
    else:
        g = 4
    return g
    


# -----------------------------------------------------------------------------------
# Function returns the highest node in case of a tie with all same costs
# -----------------------------------------------------------------------------------

def tie_break(tie_break_list):
    '''(list) -> str
    Returns the largest node from a list of nodes
    with equal total cost. '''

    for each_node in tie_break_list:
        each_node = int(each_node.replace("w", "1").replace("b", '0'))
    return max(tie_break_list)



# -----------------------------------------------------------------------------------
# A* Implementation
#   - Expand a node and generate g,h values for it
#   - add to fringe and visited sets
#   - find node with lowest total cost from fringe for each level of children
#   - check if lowest cost node is already visited. If so, check if it has a smaller cost.
#   - and replace it with it. If not, ignore that node and dont expand.
#   - Expand the cheapest node and add its children to fringe.
#   - Repeat same process for each node until goal node is reached.
# -----------------------------------------------------------------------------------

def Astar(tree, start, goal):
    '''(dict, str, str) -> list
    Returns the path taken by A* search in a
    given tree, from start to goal. '''

    visited = set() # closed set
    fringe = set() # open set
    #current = start
    a_star_path = [] # {route : [g, h]} -> keeps track of node travelled in 
    g_initial, h_initial = 0

    while fringe: # as long as not reached the goal, keep playing with tree
        for parent in tree: # if children are already in tree, remove them.
            # for each node (in the list of values corresponding to a node key)
            if (parent not in fringe) and (parent not in visited):
                fringe.add(parent)
                a_star_path.append(parent)

            for child in tree[parent]:
                #g_value = assign_g_val(child, parent) # get the actual cost
                #h_value = assign_h_val(child) # get the heuristic function
                #total_cost = g_value + h_value # get total cost

                # add total cost to fringe in both representations (for convince)
                if child != goal:
                    fringe.add(child)
                else:
                    a_star_path.add(child)
                    return a_star_path

            if parent in fringe:
                fringe.remove(parent)
                visited.add(parent)

            cost_tracker = {}
            for node_in_fringe in fringe:
                g_value = assign_g_val(parent, node_in_fringe)
                h_value = assign_h_val(node_in_fringe)
                cost_tracker[node_in_fringe] = g_value + h_value
                # get the min total cost among all nodes to in fringe
            min_cost = min(list(cost_tracker.values()))

        # check if there is only one node in fringe that has the lowest cost
        if list(cost_tracker.values()).count(min_cost) == 1:
            # knowing the min cost, find the node that is the lowest cost
            for min_cost_check in cost_tracker:
                if cost_tracker[min_cost_check] == min_cost:
                    next_node = min_cost_check # this is the node with the lowest cost.
            
            # Before expanding cheapest node, check if it already exists in visited nodes
            #if next_node in visited:
                # If it exists, check if the total cost is greater/equal to cost required in the visited set
                # If the cost is more, ignore that node -> dont expand
                #if cost_tracker[next_node] >= min_cost:
                    #fringe.pop(next_node)
                # If the node is cheaper than whats in the visited set, then replace this lower cost node 
                # with the existing similar one.
                #elif fringe[next_node] < min_cost:
                    # expand that cheaper node, add to visited, and remove from fringe
                    #visited[next_node] = min_cost
                    #fringe.pop(next_node)
            

            # If cheapest node is not in visited set, add it.
            if next_node not in visited:
                # expand that node, add to visited, and remove from fringe
                visited.add(next_node)
                # remove the node from fringe.
                fringe.remove(next_node)
                #cost_tracker.pop(next_node)

            else:
                fringe.remove(next_node)
                #cost_tracker

        # If more than one node share the same total cost, use tiebreak to pick winner
        elif list(cost_tracker.values()).count(min_cost) > 1:
            perform_tie_break = [] 
            # finds all nodes in fringe that have same cost and add to above list
            for min_cost_check in cost_tracker:
                if cost_tracker[min_cost_check] == min_cost:
                    perform_tie_break.append(min_cost_check)
            next_node = tie_break(perform_tie_break) # call tie-break function
            
            
             # If cheapest node is not in visited set, add it.
            if next_node not in visited:
                # expand that node, add to visited, and remove from fringe
                visited.add(next_node)
                # remove the node from fringe.
                fringe.remove(next_node)
                #cost_tracker.pop(next_node)

            else:
                fringe.remove(next_node)
                #cost_tracker

    #return 0 # Returning 0 because this function does not return any list due to a few unresolved issues.


# -----------------------------------------------------------------------------------
# Main Part - 2
# -----------------------------------------------------------------------------------

# 1) First step is to build a tree
build_tree_return = build_tree(start_node, goal) # returs a built tree
for i in build_tree_return:
    print(i, ":", build_tree_return[i])


#print("star node: ", type(start_node))
# 2) Perform BFS if chose
if search_method == "b":
    bfs_route = bfs(build_tree_return, start_node, goal) # calls bfs function
    print()
    #print("bfs route: ", bfs_route)
    # prints each node in bfs path
    for bfs_index in range(len(bfs_route) - 1):
        if bfs_route[bfs_index + 1][2:] == bfs_route[bfs_index][2:]:
                print(bfs_route[bfs_index][:2] + "|" + bfs_route[bfs_index][2:])
        elif bfs_route[bfs_index + 1][4:] == bfs_route[bfs_index][4:]:
                print(bfs_route[bfs_index][:4] + "|" + bfs_route[bfs_index][4:])
        elif bfs_route[bfs_index + 1][6:] == bfs_route[bfs_index][6:]:
                print(bfs_route[bfs_index][:6] + "|" + bfs_route[bfs_index][6:])
        elif bfs_route[bfs_index + 1] == bfs_route[bfs_index]:
                print(bfs_route[bfs_index] + "|" + bfs_route[bfs_index])
        else:
            print(bfs_route[bfs_index] + "|")

    print(bfs_route[-1])




# 3) Perform A star if chosen
elif search_method == "a":
    A_star_return = Astar(build_tree_return, start_node, goal) # calls A star function
    print(A_star_return)
    #print()
    # prints each node in A* path
    #for A_star_route_node in A_star_return:
        #print(A_star_route_node)
