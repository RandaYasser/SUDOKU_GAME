from numpy import zeros
import random

"""board=[[2, 0, 8, 7, 3, 0, 0, 6, 0],
    [0, 7, 0, 6, 9, 2, 0, 0, 0],
    [6, 0, 0, 0, 5, 8, 0, 0, 9],
    [0, 5, 0, 0, 2, 3, 4, 1, 0],
    [0, 2, 9, 1, 6, 4, 8, 0, 5],
    [0, 0, 0, 5, 8, 0, 0, 0, 0],
    [9, 8, 2, 3, 0, 6, 7, 0, 0],
    [3, 1, 0, 0, 0, 5, 0, 2, 0],
    [0, 0, 7, 0, 0, 9, 3, 4, 0]]"""
# TODO generate boards with diffrent sizes
def generator():
    
    board=[[0 for _ in range(9)] for _ in range(9)]
    board[0][0]=random.randint(1,9)
    solve(board)
    for x in range(50):
        
        i=random.randint(0,8)
        j=random.randint(0,8)
        board[i][j]=0

     
    return board

def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("-------------------------------")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            
            if j != len(bo[0])-1:
                print(bo[i][j]," ", end="")
            else:
                print(bo[i][j])
        

def find_empty(bo):
    # returns the first empty cell 
    for i in range(len(bo)):
        for j in range(len(bo)):
            if bo[i][j] == 0:
                return (i, j)
    return (-1, -1)


def is_valid(bo, num, pos ):
    # checks if the number is valid in a row , a col, or a box

    # check row
    for j in range(len(bo[0])):
        if bo[pos[0]][j] == num and j != pos[1]:
            return False

    # check col 
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and i != pos[0]:
            return False

    # check box
    box_i = pos[0] // 3
    box_j = pos[1] // 3
    # iterate in the box that have "pos"
    for i in range(box_i * 3, box_i * 3 + 3):    
        for j in range(box_j * 3, box_j * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    
    return True

def solve(bo):
    #solves the sudoku using backtracking
    pos = find_empty(bo)
    if pos==(-1,-1):
        return True
    else:
        i, j = pos
     
    for x in range(1, len(bo) + 1):
        if is_valid(bo, x , pos):
            bo[i][j] = x

            if solve(bo):
                return True

            bo[i][j] = 0

    return False        



