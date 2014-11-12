# -*- coding: utf-8 -*-
"""
@author: Hayden (Yuxi) Liu   yuxi.liu.ece@gmail.com


Insight Data Engineering Fellows Program - Coding Challenge

Input a CSV file consisting of an unsolved Sudoku with 0's 
representing blanks, and output a CSV file with the solved Sudoku.
"""

import csv
import time

#%% Global constant
 
VAL = '123456789'    # values from 1 to 9
ROW = '123456789'    # row index from 1 to 9
COL = '123456789'    # column index from 1 to 9

CELL = [row + col for row in ROW for col in COL]     # cell index from '11', '12' ... '19' to '91', '92' ...  '99'

def find_con_cell(cell):
    """Find all the constraint cells of the input cell, e.g., constraint cells of '11' are '13', '12', '15', '21',
    '22', '16', '19', '18', '31', '23', '51', '41', '61', '17', '71', '32', '91', '81', '33' and '14'."""
    same_row = [cell[0] + i for i in COL]
    same_col = [i + cell[1] for i in ROW]
    same_sqr = [ str(i) + str(j) for i in range( ( int(cell[0]) -1)/3*3+1,((int(cell[0])-1)/3 + 1)*3 +1 )  \
               for j in  range( ( int(cell[1]) -1)/3*3+1,((int(cell[1])-1)/3 + 1)*3 +1 ) ]
    return  list( ( set(same_row) | set(same_col) | set(same_sqr) ) - set([cell])) 

ConCELL = dict ( [(cell , find_con_cell(cell))  for cell in CELL ] )  # dict(cell : corresponding constraint cells )

#%%
        
def read_sudoku(filename):
    "Read the sudoku puzzle from a CSV file."
    sudoku = {}
    with open(filename, 'rb' ) as csvfile:
        lines = csv.reader(csvfile, delimiter=',' )
        k = 0
        for row in lines:
            sudoku.update ( dict( zip( CELL[ k*9: (k+1)*9 ] , row  )  ) )
            k += 1
    return sudoku

def fill_sudoku(sudoku):
    "Fill in the unsolved sudoku puzzle, replace '0' with possible values"
    for cell in sudoku:
        if sudoku[cell] == '0':
            sudoku[cell] = possible_guess(sudoku, cell)
    return sudoku
    
def possible_guess(sudoku, cell):
    "Get possible values for an unknown cell, under the rules of the game"
    con_cell = ConCELL[cell]
    val_con_cell = [sudoku[a] for a in con_cell]
    return ''.join(set(VAL) - set(val_con_cell))

def solve_sudoku(sudoku):
    "Main step, solve the input sudoku"
    if not sudoku :
        print 'Unsolvable sudoku puzzle'
        raise

    guess_min = 9     # minimum number of possible values
    for cell in CELL:
        l = len(sudoku[cell])
        if l < guess_min and l >1:
            cell_min = cell
            guess_min = l
    if guess_min == 9:    # if each cell only has one value
        return sudoku

    # copy the current sudoku, so that any update will not be interactional
    sudoku_possible = find_possible_solution(  [ solve_sudoku ( assign_guess(sudoku.copy(), cell_min, a) ) 
                        for a in possible_guess(sudoku, cell_min) ] )
    return sudoku_possible   # return a possible solution
      
def assign_guess(sudoku, cell, guess):
    "Assign the guess to the specific cell in a sudoku puzzle"
    sudoku[cell] = guess
    return sudoku
    
def check(sudoku):
    "Check whether the input sudoku is solved"
    for cell in CELL:
        for con_cell in ConCELL[cell]:
            if sudoku[cell] == sudoku[con_cell] and len(sudoku[con_cell]) == 1:
                return False
    return True      
    
def find_possible_solution(sudokus):
    "Input none or several possible solutions, return one may work"
    for sudoku in sudokus:
        if sudoku and check(sudoku):
            return sudoku
    return False
    
def print_sudoku(sudoku):
    "Print out the sudoku puzzle."
    for i in ROW:
        if int(i) % 3 == 1:
            print '-'*19  
        print  ''.join( ( '|' if int(j) % 3 == 1 else ' ') + sudoku[i+j]   for j in COL ) +'|'
    print '-'*19 

def validate(sudoku):
    "Verify the sudoku puzzle"
    try:
        assert check(sudoku)     
    except AssertionError :
        print 'Input sudoku puzzle is not validate'
        raise 
        
def write_sudoku(filename,sudoku):
    "Write the solved sudoku puzzle to a CSV file."
    with open(filename, 'wb' ) as csvfile:
        sudokuwriter = csv.writer(csvfile, delimiter=',',quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for i in ROW: 
            sudokuwriter.writerow( [sudoku[i+j] for j in COL])
#%%
    
if __name__=='__main__':
    in_csv = 'test1.csv'
    out_csv = in_csv.split('.csv')[0] +'_solved.csv'
    print 'Sudoku puzzle to be solved from %s:' %in_csv
    sudoku = read_sudoku(in_csv)
    print_sudoku(sudoku)
    sudoku = fill_sudoku(sudoku)
    validate(sudoku)
    startTime = time.time()
    sudoku = solve_sudoku(sudoku)
    endTime = time.time()
    print '\nSudoku puzzle is solved, and saved to %s:' %out_csv
    write_sudoku(out_csv,sudoku)
    print_sudoku(sudoku)
    print "Time spent: " + "%.4f" % (endTime-startTime) + " seconds"

 
    