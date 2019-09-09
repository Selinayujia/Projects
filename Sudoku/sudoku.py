#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 17:37:13 2019
@author: Selina Zhang

AI project: Sudoku
Implemented by using forward checking, backtrack search and maximum constrained variable with degree heuristic
"""
import os
def input_file(filename):          
# Read the input file, if error occurs, leave error mesaages
    file_path = filename           
    input = ""
    result = []
    try:
        open(file_path)
    except:
        print("Cannot open file " + filename) 
        return       
    try:
        with open(file_path) as fp:   
            for i in range(9): 
                row = fp.readline()
                input += row
            fp.close();
        for i in range(len(input)):
            if input[i].isdigit() and int(input[i])>=0 and int(input[i]) < 10: #make sure the input file has correct input for sudoku (num from 1-9)
                result.append(int(input[i]))
        if len(result) != 81:
            print("Please give a valid sudoku input.") 
            return  
    except:
        print("Please arrange your input file in the correct format.") 
        return  
    return result

def forward_checking(lst):
    result = []
    for i in range(len(lst)):                     # iterating through all the variable      
        if type(lst[i]) == int and lst[i]!= 0:    # if the variable has already has a chosen value, just append the value to the result
            result.append(lst[i])
        else:
            check_lst = [None,0,0,0,0,0,0,0,0,0]   # this is a methodology that each index represents a domain value's availablity. If after update the value from row col and grid the  number under index is still 0, that means it is a valid domain value
            domain_lst = []
            constrained_vals = row_col_grid_vals(i, lst)
            for i in range (len(constrained_vals)):
                ind = constrained_vals[i]
                check_lst[ind] = check_lst[ind]+ 1
            for i in range (len(check_lst)):
                if check_lst[i] == 0:
                    domain_lst.append(i)       # because it is lopping through the check list that has index 1-9, the possible domain value of the current variable will be ordered from small to large
            if len(domain_lst) == 0:           # early failure if the variable has no possible value to choose
                return "failure"
            elif len(domain_lst) == 1:         # after forward checking if only one variable is remained, we should use that value to further rule out the value of its neighbour
                result.append(domain_lst[0])
            else:                             # if variable has a lot of values possible, replace the value "0" or older possible value to new list of its possible value
                result.append(domain_lst)
        
    return result

def backtrack_search(lst):
    mcv_index = find_mcv_w_degree(lst)       # find the maximum constrained variable's index in the list
    if mcv_index == None:                    # return none if all the variable in the list only has one integer value, that means successfully assigned
        return lst
    else:
        mcv = lst[mcv_index]                
        for i in range(len(mcv)):           # loop through the possible value of a variable
            if mcv[i] not in row_col_grid_vals(mcv_index, lst):  #if the current value is not conflicting with row col and grid values
                lst[mcv_index] = mcv[i]             # update the current lst value
                result = forward_checking(lst)      # do a forward checking based on that (inference)
                if (result != "failure"):   
                    result = backtrack_search(result)  # if forward checking is okay then do another backtrack search based on that
                    if(result == "failure" and i!= len(mcv)):   # if the backtrack search on this current value failed and the current variable still has other possible values
                        continue                             # continue on the loop
                    else:                       # the backtrack search successed at some point
                        return result         
        return "failure"
                 
def find_mcv_w_degree(lst):             # find the varible has minimum remaining values, for tie breaking, take the variable that has most neighbours unassigned yet
    min_domain = 9                      # set min_domain the largest possible one at first
    degree = 0                
    mcv_i = 0
    complete = True                     # if non of the variable's type is list, that means conplete
    for i in range(len(lst)):
        if type(lst[i]) == list:
            complete = False
            if len(lst[i]) < min_domain:    
                min_domain = len(lst[i])
                degree = row_col_grid_vals(i, lst, True)  # using three parameter to get the degree
                mcv_i = i
            if len(lst[i]) == min_domain:    # for breaking the tie of minimum constraint variable, we need to use the degree heuristic
                curr_d = row_col_grid_vals(i, lst, True)
                if curr_d > degree:
                    degree = curr_d
                    mcv_i = i
    if complete:
        return None
    return mcv_i           # return the index of the mcv
        
    
    
def row_col_grid_vals(index, lst, mcv = False):   
    # if mcv = true, that means return the degree(how many variables at the same row, col and grid haven't has an assigned value)
    # if mcv = false, simplely return the varaibe's possible value domain
    result_lst = []
    if mcv:
        counter_of_unassigned_n = 0;
    
    row = index // 9                            # check the row of current variable
    for i in range (9 * row, 9 * (row + 1)):
        if(type(lst[i])!=list and lst[i]!= 0):
            result_lst.append(lst[i])
        if(mcv and type(lst[i])==list):
            counter_of_unassigned_n += 1
            
    col = index % 9                             # check the col of current variable
    for i in range (9):
        if(type(lst[col + 9 * i])!= list and lst[col + 9 * i] != 0):
            result_lst.append(lst[col + 9 * i])
        if(mcv and type(lst[col + 9 * i]) == list):
            counter_of_unassigned_n += 1
    
    row_s = (row // 3) * 3                     # check the grid of current variable
    col_s = (col // 3) * 3
    for i in range (row_s, row_s+3): 
        for j in range (col_s, col_s+3):
            if(type(lst[9 * i + j])!= list and lst[9 * i + j] != 0):
                result_lst.append(lst[9 * i + j])
            if(mcv and type(lst[9 * i + j])== list):
                counter_of_unassigned_n += 1
      
    if mcv: 
        return counter_of_unassigned_n - 3  #count self 3 times, need to delete it 

    return result_lst

def output_file(input_name,output_name,cwd,result):
    with open(os.path.join(cwd, output_name), 'w') as output_f:
        if isinstance(result, list):       # if result is a string, that means a failure message
            cnt = 0
            line = ""
            for i in range(len(result)):
                line += str(result[i])
                cnt += 1
                if cnt <= 8:
                    line += " "        # in between variable
                else:
                    line += "\n"       # in between line
                    output_f.write(line)
                    line = ""
                    cnt = 0
        else:         
            output_f.write("There is no possible way to form a correct sudoku.")
        output_f.close()
    return output_f
   
def main():                       
    input_file_name = input("Please enter your input file name (The input file need to be in your current directory):")
    output_file_name = input("Please enter your intended output file name (The output file will be generated in your current directory):")
    cwd = os.getcwd()   
    result = input_file(input_file_name)        # read input file
    if result != None:                          # success in opening file
        result = forward_checking(result)       
        if result != "failure":                 # detect early failure by forward  checking
            result = backtrack_search(result)   
    print("Output generated.File name is "+ output_file_name)
    return output_file(input_file_name,output_file_name, cwd,result)

if __name__ == "__main__":
    main()
