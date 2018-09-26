#!/usr/bin/env python
# coding:utf-8

"""
Usage:
$ python3 driver.py <81-digit-board>
$ python3 driver.py   => this assumes a 'sudokus_start.txt'

Saves output to output.txt
"""

import sys
import time

ROW = "ABCDEFGHI"
COL = "123456789"
TIME_LIMIT = 1.  # max seconds per board
out_filename = 'output.txt'
src_filename = 'sudokus_start.txt'


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def string_to_board(s):
    """
        Helper function to convert a string to board dictionary.
        Scans board L to R, Up to Down.
    """
    return {ROW[r] + COL[c]: int(s[9 * r + c])
            for r in range(9) for c in range(9)}


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def write_solved(board, f_name=out_filename, mode='w+'):
    """
        Solve board and write to desired file, overwriting by default.
        Specify mode='a+' to append.
    """
    backtracking(board)
    #print(result)  # TODO: Comment out prints when timing runs.
    #print()

    # Write board to file
    outfile = open(f_name, mode)
    outfile.write(result)
    outfile.write('\n')
    outfile.close()

    return result


def backtracking(board):
    """Takes a board and returns solved board."""
    global result
    solved_board=board
    #print(board)
    empties=get_empties(board) #we just need to know who is empty
    if len(empties) == 0:
        #print_board(board)
        result = board_to_string(board)
        return 1
        #return board_to_string(solved_board)
    remaining=get_remaining(board)
    #print(remaining)
    mrv=[]
    for square in empties:
        mrv.append(len(remaining[square]))
    mrv_index = mrv.index(min(mrv))
    square = empties[mrv_index]
    #print(square)
    domain = remaining[square]
    while len(domain) != 0:
        value = domain[0]
        domain.remove(value)
        if forward_check(remaining, value, square[0], square[1]):
            board[square] = value
            if backtracking(board):
                result = board_to_string(board)
                return 1
            else:
                board[square]=0
    return 0

def forward_check(remaining, value, row, col):
    """Conducts the forward check"""
    rowint = ROW.find(row)
    for c in COL:
        if c == col:
            continue
        x = remaining[row+c]
        if len(x)==1:
            if x[0]==value:
                return 0
    for r in ROW:
        if r == row:
            continue
        x = remaining[r+col]
        if len(x) ==1:
            if x[0] == value:
                return 0
    startrow = rowint//3
    startcol = (int(col)-1)//3
    for i in range(3):
        for j in range(3):
            rowindex=ROW[startrow*3+i]
            colindex=COL[startcol*3+j]
            if (rowindex==row and colindex==col):
                continue
            x = remaining[rowindex+colindex]
            if len(x) == 1:
                if x[0]==value:
                    return 0
    return 1



def get_empties(board):
    """Provide empty squares"""
    empties=[]
    for key, val in board.items():
        if val==0:
            empties.append(key)
    return empties

def get_remaining(board):
    remaining={}
    #initialize
    for r in ROW:
        for c in COL:
            remaining[r+c]=[i for i in range(1,10)]
    #print(remaining)
    for r in ROW:
        for c in COL:
            if board[r+c]!=0:
                value = board[r+c]
                remaining=remove_value(r,c,value,remaining)
    return remaining

def remove_value(r, c, value, remaining):
    """Remove a value from domains"""
    remaining[r+c]=[0] #placeholder for taken square
    
    
    #lets check same row
    for col in COL:
        domainvalues=remaining[r+col]
        try:
            domainvalues.remove(value)
        except ValueError:
            pass
    

    #lets check same column
    for row in ROW:
        domainvalues = remaining[row+c]
        try:
            domainvalues.remove(value)
        except ValueError:
            pass

    #lets check same large square
    startrow = ROW.find(r)//3
    #print(startrow)
    startcol = (int(c)-1)//3
    #print(startcol)
    for i in range(3):
        for j in range(3):
            rowindex=ROW[startrow*3+i]
            colindex=COL[startcol*3+j]
            domainvalues =remaining[rowindex+colindex]
            try:
                domainvalues.remove(value)
            except ValueError:
                pass
    #print(remaining)
    return remaining


if __name__ == '__main__':
    startime=time.time()
    if len(sys.argv) > 1:  # Run a single board, as done during grading
        board = string_to_board(sys.argv[1])
        write_solved(board)

    else:
        print("Running all from sudokus_start")

        #  Read boards from source.
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):
            

            if len(line) < 9:
                continue

            # Parse boards to dict representation
            board = string_to_board(line)
            #print_board(board)  # TODO: Comment this out when timing runs.

            # Append solved board to output.txt
            write_solved(board, mode='a+')

        print("Finished all boards in file.")