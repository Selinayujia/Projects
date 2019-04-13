#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 21:05:34 2019
@author: selina
"""
#READ ME
#This is a program for solving 8 puzzle problem using A* search.
#It take an input file from the current directory, format is initial state(num from 0-9), 
#blank line and goal statenum from (0-9). 0 represents blank space in puzzle
#Example: (upper is initial state and lower is goal state)
#2 0 7
#3 4 5
#1 6 8

#1 2 3
#4 5 6
#7 8 0
#This program takes the input file and generates an output file in the current directory 
#with the name user provided
# Line 8 is a blank line
# Line 9 is the depth level d of the goal node in your search tree (assume the root node is at level 0)
# Line 10 is the total number of nodes N generated in your search tree (including the root node.) 
# Line 11 contains the solution that you have found. The solution is a sequence of actions (from root node
#to goal node) represented by the A’s in line 11. Each A in line 11 is a character from the set {L,
#R, U, D}, where L, R, U and D represent the left, right, up and down movements of the blank
#position. 
#Line 12 contains the f(n) values of the nodes along the solution path, from root node to the goal node. 
#There should be d number of A values in line 11 and d+1 number of f values in line 12.
# (Instruction provided by my instructor, Edward Wong)

import os
import copy
class puzzle:
    def __init__(self, config, blank_pos, depth, parent, action = None,cost = 0):
        self.config = config       # an 2d array that represents the puzzle
        self.blank_pos = blank_pos # the location of zero
        self.depth = depth         # the puzzle's depth 
        self.parent = parent       # the puzzle's parent, used for trace back when find goal
        self.action = action       # the action that generate the next puzzle
        self.cost = cost           # f(n), which is  h(n) + g(n)
        
def input_file(filename):          
# Read the input file, if error occurs, leave error mesaages
    file_path = filename           
    initial_state = [0]*3          # three rows, each elem of list will be a list of three numbers from each colume
    goal = []
    blank_pos = (0,0)
    try:
        open(file_path)
    except:
        print("Cannot open file " + filename) 
        return       
    try:
        with open(file_path) as fp:  
           cnt = 0
           while cnt < 3:             #first three rows are initial state
               initial_state_row = fp.readline().strip('\n').split(" ")
               for i in range(len(initial_state_row)):  
                                      #find the position of the blank in the form (x,y)
                   if initial_state_row[i] == '0':
                       blank_pos = (cnt, i)              
               initial_state[cnt] = initial_state_row
               cnt += 1
           fp.readline()              # blank line in between initial and goal
           cnt += 1
           while cnt < 7:             #the rest lines are goal state
               goal.append(fp.readline().strip('\n').split(" "))
               cnt += 1
           fp.close() 
    except:
        print("Please arrange your input file in the correct format.") 
        return  
    return (initial_state, blank_pos, goal)

def A_star_search(curr_node,goal_config,heuristic_func):
# A* search algorithm 
    frontier = []
    explored_set = []
    num_total_nodes = 1                 # initial state node
    while  curr_node.config != goal_config:
        expanded_nodes = expand(curr_node)
        new_node_list = []
        for node in expanded_nodes:
           # choose one of the heuristic functions
           if heuristic_func == "1":
               h_n = h_F_M_dis(node.config, goal_config)
           else:
               h_n = h_F_M_dis_Lconf(node.config, goal_config)
           node.cost = node.depth + h_n  #f(n) = g(n) + h(n)
           # if the generated node in explored set, do not generate
           in_explored_set = False
           for i in range (len(explored_set)): 
               if(node.config == explored_set[i].config):
                   in_explored_set = True
                   break
           if not in_explored_set:  
               new_node_list.append(node)
        explored_set.append(curr_node)
        num_total_nodes += len(new_node_list)
        frontier = descending_sort_frontier(frontier,new_node_list) 
        # find the least cost node, the frontier is sorted from large to small
        if len(frontier) == 0:
            return "failure"
        else:
            curr_node = frontier.pop() # poped node has the smallest cost
    return trace_back(curr_node, num_total_nodes)

def expand(curr_node):  
# expand the current node by making one move of the blank space
    result = []
    x = curr_node.blank_pos[0]  #colume
    y = curr_node.blank_pos[1]  #row
    depth = curr_node.depth + 1
    if (x - 1) >= 0:     # if move upward is valid
        new_node_config = copy.deepcopy(curr_node.config)
        new_node_config[x][y] = new_node_config[x-1][y]
        new_node_config[x-1][y] = '0'
        new_blank_pos = (x-1,y)
        action = "U"
        new_puzzle = puzzle(new_node_config, new_blank_pos, depth, curr_node, action)
        result.append(new_puzzle)
        
    if (x + 1) <= 2:     # if move downward is valid
        new_node_config = copy.deepcopy(curr_node.config)
        new_node_config[x][y] = new_node_config[x+1][y]
        new_node_config[x+1][y] = '0'
        new_blank_pos = (x+1,y)
        action = "D"
        new_puzzle = puzzle(new_node_config, new_blank_pos, depth, curr_node, action)
        result.append(new_puzzle)
    
    if (y - 1) >= 0:     # if move left is valid
        new_node_config = copy.deepcopy(curr_node.config)
        new_node_config[x][y] = new_node_config[x][y-1]
        new_node_config[x][y-1] = '0'
        new_blank_pos = (x,y-1)
        action = "L"
        new_puzzle = puzzle(new_node_config, new_blank_pos, depth, curr_node, action)
        result.append(new_puzzle)
        
    if (y + 1) <= 2:    # if move right is valid
        new_node_config = copy.deepcopy(curr_node.config)
        new_node_config[x][y] = new_node_config[x][y+1]
        new_node_config[x][y+1] = '0'
        new_blank_pos = (x,y+1)
        action = "R"
        new_puzzle = puzzle(new_node_config, new_blank_pos, depth, curr_node, action)
        result.append(new_puzzle)
    return result

def h_F_M_dis(curr_node_config, goal_config, linear_conf = 0):  
# calculate h(n) using manhattan distance
    curr_pos_lst = [0] * 9
    goal_pos_lst = [0] * 9
    manhattan_dis = 0
    # this double loop is used to put each number's position under the corresponding list's index
    # for example, in the current puzzle, the location of "7" will be put in index 7 of curr_pos_lst
    for i in range (len(curr_node_config)):
        for j in range(len(curr_node_config[i])):
            curr_pos_lst[int(curr_node_config[i][j])] = (i,j)  #col = i and row = j
            goal_pos_lst[int(goal_config[i][j])] = (i,j)   
    for i in range(1,9): # do not count the change of blank space
        manhattan_dis += abs(goal_pos_lst[i][0]-curr_pos_lst[i][0]) 
        #plus the horizontal absolute distance between goal and current node
        manhattan_dis += abs(goal_pos_lst[i][1]-curr_pos_lst[i][1]) #
        #plus the vertical absolute distance between goal and current node
    if(linear_conf == 1):
        return (curr_pos_lst, goal_pos_lst, manhattan_dis)
    return manhattan_dis
    
def h_F_M_dis_Lconf(curr_node_config, goal):
# calculate h(n) using manhattan distance + 2 * linear conflicts   
# the methodology is, from the two position lists(explained in the above func),
# if it find the same number in the same row/col, it put the relative distance 
# into relative linear conflict list (linear_conf_x/linear_conf_y) 
# Each element represents that under ith column, there is a position shiftment (positive or negative) between the num in current node and goal node 
# if there is no linear conflict, that means either the same number from current list and goal list not in the same row/col
# or it means they both shift in the same direction (the absolute value of their distance sum will not be zero)
# However, if there is linear conflict, there are three cases
# 1 linear conflict, there are +1 and -1 position shiftments in a row/col
# 2 linear conflicts, there are +1, +1, -2 or -1, -1, +2 position shiftments in a row/col
# 3 linear conflicts, there are +2 and -2 position shiftments in a row/col
    
    result = h_F_M_dis(curr_node_config, goal,1)
    curr_pos_lst = result[0] 
    goal_pos_lst = result[1]
    linear_conf_x = [[],[],[]]
    linear_conf_y = [[],[],[]]
    manhattan_dis = result[2]
    linear_conf = 0

    for i in range(1,9):
        if goal_pos_lst[i] == curr_pos_lst[i]:
            pass
        elif goal_pos_lst[i][0] == curr_pos_lst[i][0]:
            col = goal_pos_lst[i][0]
            dis = goal_pos_lst[i][1]-curr_pos_lst[i][1]
            linear_conf_y[col].append(dis)
        elif goal_pos_lst[i][1] == curr_pos_lst[i][1]:
            row = goal_pos_lst[i][1]
            dis = goal_pos_lst[i][0]-curr_pos_lst[i][0]
            linear_conf_x[row].append(dis)
            
    for i in range (len(linear_conf_x)):
        if sum(linear_conf_x[i]) == 0 and len(linear_conf_x[i])!= 0:
            if len(linear_conf_x[i]) == 3:
                linear_conf += 2 * 2
            elif abs(linear_conf_x[i][0]) == 1:
                linear_conf += 1 * 2
            
            else: #abs(linear_conf_x[i][0]) == 2:
                linear_conf += 3 * 2
                
    for i in range (len(linear_conf_y)):
        if sum(linear_conf_y[i]) == 0 and len(linear_conf_y[i])!= 0:
            if len(linear_conf_y[i]) == 3:
                linear_conf += 2 * 2
            elif abs(linear_conf_y[i][0]) == 1:
                linear_conf += 1 * 2
            
            else:   # abs(linear_conf_y[i][0]) == 2:
                linear_conf += 3 * 2

                
    return manhattan_dis + linear_conf
     

def descending_sort_frontier(frontier,generated_nodes):
# A piority stack sorted by the path cost from high to low.
# If two nodes have the same cost, the child will be poped out before uncle
# This will generate less nodes
    count = len(generated_nodes)
 # bubble sort the generated node list first  
    while count >= 0:
        for i in range (count-1):
            if generated_nodes[i].cost < generated_nodes[i+1].cost:
                temp = generated_nodes[i+1]
                generated_nodes[i+1] = generated_nodes[i]
                generated_nodes[i] = temp
        count -= 1
    if len(frontier) == 0:
        return generated_nodes
# if frontier not empty, it should be in descending order allready,
# A merge sort of frontier(sorted) and generated node list(sorted)
    else:
        return_list = []
        i = 0
        j = 0
        while i < len(frontier):
            if j < len(generated_nodes):
                if frontier[i].cost >= generated_nodes[j].cost: 
# >= makes the child moved to end before uncle if cost is the same. 
# If >, then this is a piority queue, but that will generate more nodes
                    return_list.append(frontier[i])
                    i += 1
                else:
                    return_list.append(generated_nodes[j])
                    j += 1
            else:   # generated_nodes list is first completely merged already
                for k in range(i, len(frontier)):
                    return_list.append(frontier[k])
                break
        if j!= len(generated_nodes):  #the frontier is first completely merged
            for k in range(j, len(generated_nodes)):
                    return_list.append(generated_nodes[k])
        return return_list
def trace_back(curr_node,num_total_nodes):
#trace back from goal state to initial state to see the action and cost list along the solution path
    action_list =[]
    cost_list = []
    solution_depth = 0 # the initial_state level
    
    while curr_node.parent!= None:
        action_list.append(curr_node.action)
        cost_list.append(str(curr_node.cost))
        solution_depth += 1
        curr_node = curr_node.parent
        
# currently the cost list and action list are in reversed order from goal to initial state
# need to reverse it back
    (low, high) = (0, solution_depth-1)
    while low <= high:  
        (action_list[low],action_list[high]) = (action_list[high],action_list[low])
        (cost_list[low], cost_list[high]) = (cost_list[high], cost_list[low])
        low += 1
        high -= 1
        
    cost_list.append(str(solution_depth))  #when the curr_node is goal node, 
    #h(n) is zero and f(n) is g(n), which is path cost == solution depth
        
    return [solution_depth, num_total_nodes, action_list,cost_list]

def output_file(input_name,output_name,cwd,result):
    cnt = 0
    with open(os.path.join(cwd, output_name), 'w') as output_f:
        with open(input_name) as input_f:  # copy the input file to the output file
            while cnt < 7:
                line = input_f.readline()
                output_f.write(line) 
                cnt += 1
            input_f.close() 
        output_f.write('\n\n')
        if isinstance(result, list):       # if result is a string, that means a failure message
            output_f.write(str(result[0])+'\n')      # the depth of solution
            output_f.write(str(result[1])+'\n')      # the nodes generated
            output_f.write(" ".join(result[2])+'\n') # the action list converted to string
            output_f.write(" ".join(result[3])+'\n') # the cost list converted to string 
        else:         
            output_f.write("There is no possible way from initial state to goal state.")
    
    output_f.close()
    return output_f
   
def main():                       
    input_file_name = input("Please enter your input file name (The input file need to be in your current directory):")
    output_file_name = input("Please enter your intended output file name (The output file will be generated in your current directory):")
    heuristic_func = input("Please choose one heuristic function: enter 1 is h(n) = manhattan distance and enter 2 is h(n) = mahattan distance + 2 * linear conflicts: ")
    result = input_file(input_file_name)        # read input file
    if result != None:                          # success in opening file
        config = result[0]
        blank_pos = result[1]
        initial_state = puzzle(config,blank_pos, 0, None)# first is config, second is depth,third is parent
        goal_config = result[2]
        result = A_star_search(initial_state, goal_config, heuristic_func)
        print("Output generated.File name is "+ output_file_name)
        cwd = os.getcwd()                       # get the path of current directory
        if result == "failure":
            return output_file(input_file_name,output_file_name, cwd,result) 
        return output_file(input_file_name,output_file_name, cwd,result)


if __name__ == "__main__":
    main()