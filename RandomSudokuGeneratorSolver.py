import random
from enum import Enum
import copy

BOARD_SIZE = 9

class Levels(Enum):
    VERY_EASY = (1, 8)
    EASY = (9, 15)
    MEDIUM = (20, 30)
    HARD = (35, 45)
    NIGHTMARE = (65, 70)

def solveSudoku(grid, x, y, save_solution):
    """
    :type grid: List[List[int]]
    :type x: Int
    :type y: Int
    :type save_solution: List[]
    :rtype: Bool
    """
    
    if x == len(grid[0]):
        x = 0
        y += 1

    if y >= len(grid):
        if save_solution:
            return False
        for row in grid:
            new_row = []
            for val in row:
                new_row.append(val)
            save_solution.append(new_row)
        return

    if grid[y][x] != 0:
        if solveSudoku(grid, x+1, y, save_solution) == False:
            return False
        return

    for val in range(1, BOARD_SIZE+1):
        if isValid(grid, x, y, val):
            grid[y][x] = val
            if solveSudoku(grid, x+1, y, save_solution) == False:
                return False
            grid[y][x] = 0

def isValid(grid, x, y, val):
    """
    :type grid: List[List[int]]
    :type x: Int
    :type y: Int
    :type val: Int
    :rtype: Bool
    """

    block_x = (x // int(BOARD_SIZE / 3)) * int(BOARD_SIZE / 3)
    block_y = (y // int(BOARD_SIZE / 3)) * int(BOARD_SIZE / 3)

    for b_y in range(int(BOARD_SIZE / 3)):
        for b_x in range(int(BOARD_SIZE / 3)):
            if grid[b_y + block_y][b_x + block_x] == val:
                return False
            
    for col in range(0, BOARD_SIZE):
        if grid[y][col] == val:
            return False

    for row in range(0, BOARD_SIZE):
        if grid[row][x] == val:
            return False

    return True

def print_sudoku(grid):
    """
    :type grid: List[List[int]]
    :rtype: Void
    """

    horizontal_line = "+-------+-------+-------+"

    for i in range(len(grid)):
        if i % 3 == 0:
            print(horizontal_line)

        for j in range(len(grid[i])):
            if j % 3 == 0:
                print("|", end=" ")

            if grid[i][j] == 0:
                print(".", end=" ")
            else:
                print(grid[i][j], end=" ")

        print("|")
    
    print(horizontal_line)

def createGrid(level, grid):
    """
    :type grid: List[List[int]]
    :type level: Levels
    :rtype: List[List[int]]
    """

    solution = []
    solveSudoku(grid, 0, 0, solution)
    return pierceGrid(solution, level)

def pierceGrid(grid, level):
    """
    :type grid: List[List[int]]
    :type level: Levels
    :rtype: List[List[int]]
    """
    
    s, e = level.value
    numOfPierces = random.randint(s, e)
    save_grid = copy.deepcopy(grid)

    while numOfPierces > 0:
        x = random.randint(0, BOARD_SIZE-1)
        y = random.randint(0, BOARD_SIZE-1)
        while grid[y][x] == 0:
            x = random.randint(0, BOARD_SIZE-1)
            y = random.randint(0, BOARD_SIZE-1)

        grid[y][x] = 0
        solutions = []

        if solveSudoku(grid, 0, 0, solutions) == False:
            grid = copy.deepcopy(save_grid)
        else:
            save_grid[y][x] = 0
            numOfPierces -= 1

    return save_grid

if "__main__" == __name__:
    grid = [
        [random.randint(1, BOARD_SIZE), 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, random.randint(1, BOARD_SIZE), 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, random.randint(1, BOARD_SIZE), 0, 0],
        [0, random.randint(1, BOARD_SIZE), 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, random.randint(1, BOARD_SIZE), 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, random.randint(1, BOARD_SIZE), 0],
        [0, 0, random.randint(1, BOARD_SIZE), 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, random.randint(1, BOARD_SIZE), 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, random.randint(1, BOARD_SIZE)]
    ]

    sudoku = createGrid(Levels.NIGHTMARE, grid) #Create the random sudoku
    print_sudoku(sudoku)#Print the random sudoku without solving it
    solution = []
    solveSudoku(sudoku, 0, 0, solution)#Solve the sudoku with recursion
    print("\nSolution:\n")
    print_sudoku(solution)#Print the sudoku solution