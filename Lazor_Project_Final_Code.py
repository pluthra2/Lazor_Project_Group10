'''
***** Lazor Project 2019 - Software Carpentry *****
Contributors - Charan S. Pasupuleti. , Prabhjot K. Luthra, Wayne D. Moneteiro
Objective:- The code so written should generate solution for placing the blocks
in a given board, thus solving the lazor board so given and making lazors
intersect all holes.
Method or Idea :- Lazors or holes are always on the middle point of the edges
of the blocks, thus we designed a grid for a given board, so each block in the
board is a middle point on the block in a grid (like a block surrounded by x's)
x x x
x o x
x x x - this is one block of the grid portraying one block of the board
So now it's easy to mathematically have a coordinate system for the grid with
  ----- > x
 |
 |
 |
 V
 y
 x,y- As the directions for the coordinate system.
 And just like solving a maze, here we increment each of the lazors one step
 at a time, and as it intersects the holes we remove that hole from the list
 For Placement of Blocks in the grid at the right ( or even wrong) position
 We first found all the permutations of o's , A's, B's, C's ( movable blocks)
 and then generated or created grids and checked each of them with the lazor
 solver that checks if in that case for that placement of blocks, if the lazors
 hit all the sinks/ holes or not. As soon as it comes across the right grid,
 the simulation stops and it prnts out the correct grid or
 the Solution for the lazor game.
 Lastly as an additional challenge we generated a GUI image for the solution
 with light grey blocks/ background as - non movable blocks (x)
 dark grey blocks as - empty positions (o's)
 white blocks as - reflect blocks (A's)
 black blocks as - absorb blocks (B's)
 cyan blocks as - refract blocks (C's)
'''


import time
import copy
from sympy.utilities.iterables import multiset_permutations
from PIL import Image, ImageDraw


x = 0  # Positions not allowed to place the block
o = 1  # Positions open to place the block
A = 2  # Reflect Block
B = 3  # Absorb Block
C = 4  # Refract Block
# Colors for the Board and Solution Board Image
COLORS = {
    'x': (160, 160, 160),
    'A': (255, 255, 255),
    'B': (0, 0, 0),
    'C': (172, 215, 218),
    'o': (100, 100, 100),
}


def set_color(img, x0, y0, dim, color):
    '''
    This function sets a colour for the pixels in that block
    of the board
    *** Parameters ***
    img : CLass Object - Image class object
    x0 : Integer - starting x coordinate
    y0 : Integer -starting y coordinate
    dim : Integer - dimension of the block
    color : String - Color to set the block to
    *** Returns ***
    An image with all the pixels assigned with specific colour.
    '''
    for x in range(dim):
        for y in range(dim):
            img.putpixel(
                (dim * x0 + x, dim * y0 + y), color)


def GUI_board(original_board, solution_board, filename,
              lazors_ori, holes, stack_lazors, blockSize=100):
    '''
    This function is to generate the given and solution board as an image
    Once you run this code the images are saved as
    "file_name_originalboard.png" and "file_name_solution.png"
    The idea of the code is extracted from the maze generation challenge
    given in the software carpentry class.
    *** Parameters ***
    original_board : List of Lists - That hold the board given in .bff file
    solution_board : List of Lists - Solution board so generated
    filename: String - .bff filename
    lazors_ori : List of tuples - Consisting of all origins and directions
                                  of the lazors
    holes : List - consisiting of the hole points
    stack_lazors - List of Lists - consisting of the lazor path
                                   for each lazor
    blocksize - Integer - Size of the block of the board
    *** Returns ***
    Nothing as it saves the boards as images
    '''
    name = filename.split('.')
    file_name = name[0]
    w_blocks = len(solution_board[0])
    h_blocks = len(solution_board)
    SIZE = (w_blocks * blockSize, h_blocks * blockSize)
#    Creates a new image with all blocks filled with black.
    img = Image.new("RGB", SIZE, color=COLORS['x'])

    for y, row in enumerate(original_board):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])
#   Calls Imagedraw function from PIL to draw shapes on the image.

    draw = ImageDraw.Draw(img)
#   The below code is to generate the image for the original board.
    # For Horizontal Boundaries
    for x in range(100, SIZE[0] + 100, 100):
        x1 = x
        x2 = x
        y1 = 0
        y2 = SIZE[1]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Vertical Boundaries
    for y in range(100, SIZE[1] + 100, 100):
        y1 = y
        y2 = y
        x1 = 0
        x2 = SIZE[0]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Holes
    for i in holes:
        x1 = i[0]
        y1 = i[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 10, b - 10, a + 10, b + 10], fill=255)
    # For Lazor Origin
    for j in lazors_ori:
        ori = j[0]
        x1 = ori[0]
        y1 = ori[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(153, 0, 0))
        draw.ellipse([a - 8, b - 8, a + 8, b + 8], outline=0, width=2)
    # Saving it as an original board
    img.save("%s_original_board.png" % (file_name))

#   The below code is for generating the solved grid image.

    for y, row in enumerate(solution_board):
        for x, block_ID in enumerate(row):
            set_color(img, x, y, blockSize, COLORS[block_ID])
    # For Horizontal Boundaries
    draw = ImageDraw.Draw(img)
    for x in range(100, SIZE[0] + 100, 100):
        x1 = x
        x2 = x
        y1 = 0
        y2 = SIZE[1]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Vertical Boundaries
    for y in range(100, SIZE[1] + 100, 100):
        y1 = y
        y2 = y
        x1 = 0
        x2 = SIZE[0]
        draw.line([x1, y1, x2, y2], fill=(255, 255, 255))
    # For Holes
    for i in holes:
        x1 = i[0]
        y1 = i[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 10, b - 10, a + 10, b + 10], fill=255)
    # For Lazor Origins
    for j in lazors_ori:
        ori = j[0]
        x1 = ori[0]
        y1 = ori[1]
        a = x1 * 50
        b = y1 * 50
        draw.ellipse([a - 5, b - 5, a + 5, b + 5], fill=(153, 0, 0))
        draw.ellipse([a - 8, b - 8, a + 8, b + 8], outline=0, width=2)
    # For Lazor Path
    final_points = []
    for i in range(len(stack_lazors)):
        final_points.append([])
        for j in range(len(stack_lazors[i])):
            if stack_lazors[i][j][0] != stack_lazors[i][j - 1][0]:
                stack_lazors[i][j][0] = [element * 50 for element in stack_lazors[i][j][0]]
                final_points[i].append(tuple(stack_lazors[i][j][0]))
    for i in final_points:
        draw.line(i, fill=255, width=2)
    # Saving the solution boards
    img.save("%s_solution.png" % (file_name))


class Grid():
    '''
    This Class creates objects which represent the board
    With different placement of the blocks there are different
    boards generated and each board is an object of this class
    '''

    def __init__(self, board, A_blocks, B_blocks, C_blocks, lazors, hole):
        '''
        Initialises the object of the Class Grid
        *** Parameters ***
        self - variable that holds all the data regarding the class object
        board - n*m matrix consisting of some or all of o, x, A, B and C
        A_blocks - number of reflect blocks in the board
        B_blocks - number of absorb blocks in the board
        C_blocks -  number of refract blocks in the board
        lazors - list of lists of all lazors consisting of orgins and direction
        eg. [[(1,3),(-1,-1)],[(2,4), (1,-1)]] - 2 lazors
        L1 - origin (1,3), direction (-1,-1)
        L2 - origin (2,4), direction (1, -1)
        hole- list of hole points that the lazor has to intersect
        *** Returns ***
        Nothing!
        '''
        self.board = board
        self.A = A_blocks
        self.B = B_blocks
        self.C = C_blocks
        self.L = lazors
        self.H = hole
        length = 2 * len(self.board) + 1
        width = 2 * len(self.board[0]) + 1
        grid = []
        for i in range(length):
            grid.append([])
            for j in range(width):
                grid[i].append('x')
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                grid[2 * i + 1][2 * j + 1] = self.board[i][j]
        self.grid = grid

    def blocks(self, filename):
        '''
        Depensing upon the data read from the bff file
        Board, Number of A, B, C blocks, Lazor List, Holes
        This block generates all the possible boards by permuting the list
        of all movable blocks like o's, A's, B's, and C's
        Each board so generated is first converted into a grid and then checked
        with lazor solver function if the generated board is the solution for
        the board so given, The maximum iterations possible and iterations so
        performed are printed.
        ** Parameters **
        self - consists of all data (board, A_blocks, B_blocks, C_blocks .. )
        ** Returns **
        Nothing!
        '''
        movable_blocks = []
        for x in self.board:
            for y in x:
                if y == 'o':
                    movable_blocks.append(y)

        for i in range(self.A):
            movable_blocks[i] = 'A'
        for i in range(self.A, (self.A + self.B)):
            movable_blocks[i] = 'B'
        for i in range((self.A + self.B), (self.A + self.B + self.C)):
            movable_blocks[i] = 'C'
        ITER_B = 0
        print("Generating possible Boards.......", end="\r")
        t1 = time.time()
        permutations = list(multiset_permutations(movable_blocks))
        t2 = time.time()
        print("Maximum possible iteration possible : ", len(permutations))
        print("Time for generating possible Boards: ", t2 - t1)
        x = 0
        print("Solving...", end="\r")
        t1 = time.time()
        for permut in permutations:
            sinks = copy.deepcopy(self.H)
            actual_board = copy.deepcopy(self.grid)
            possible_grid = create_grid(actual_board, permut)
            ITER_B += 1
            Result, stack_lazors = lazor_path(possible_grid, self.L, sinks)
            if Result:
                print("Congratulations!! Board Solved")
                final_board = []
                length = int((len(possible_grid) - 1) / 2)
                width = int((len(possible_grid[0]) - 1) / 2)
                for i in range(length):
                    final_board.append([])
                    for j in range(width):
                        final_board[i].append(
                            possible_grid[2 * i + 1][2 * j + 1])
                        print(possible_grid[2 * i + 1][2 * j + 1], end=' ')
                    print()
                print("This is the solution grid!")
                print("OR just check the text file or image so created!")
                GUI_board(self.board, final_board,
                          filename, self.L, self.H, stack_lazors)
                fname1 = filename.split(".bff")[0]
                fname = fname1 + "_solution_textfile.txt"
                f = open(fname, "w+")
                f.write("The solution to your board is: \n")
                for i in range(length):
                    for j in range(width):
                        f.write(possible_grid[2 * i + 1][2 * j + 1])
                        f.write(" ")
                    f.write("\n")
                f.write("A is the reflect block, B is the absorb ")
                f.write("block and  C is the reflect block.\nThe o should ")
                f.write("be empty. Try not to cheat next time :)")
                f.close()
                break
            t2 = time.time()
            if t2 - t1 >= 5:
                t1 = time.time()
                b = "Solving" + "..." * x
                print(b, end="\r")
                if x == 3:
                    x = 0
                x += 1
        print("Iteration took to solve: ", ITER_B)


def read_bff(filename):
    '''
    This function is to read a 'bff' file so given
    This file consists all the given information for solving the board
    It consists of the board, number of blocks of type A, B, and C,
    lazors ( with their origin and direction), hole points
    *** Parameters ***
    filename - the name of the bff file
    *** Returns ***
    updated_board - list of lists :board given in the bff file
    A_blocks - integer : Number of blocks of Type A
    B_blocks - integer : Number of blocks of Type B
    C_blocks - integer : Number of blocks of Type C
    lazors - list of lists : List of all lazors with their origin and direction
    hole - list : List of all the hole points
    '''
    split_name = [char for char in filename]
    if split_name[-4:] != [".", "b", "f", "f"]:
        raise Exception("File type is not .bff")
    board = []
    A_blocks = 0
    B_blocks = 0
    C_blocks = 0
    lazor_ori = []
    hole = []
    '''
    If no such file exists with this filename
    '''
    try:
        bff_read = open(filename, "r").read()
    except UnboundLocalError:
        print("There is no such file")
    file_content = bff_read.strip().split("\n")
    start_found = 0
    stop_found = 0
    for i in range(len(file_content)):
        if file_content[i] == "":
            continue
#        Read in the grid, if no START or STOP raise an error
        if file_content[i] == "GRID START":
            a = i + 1
            start_found = 1
            while file_content[a] != "GRID STOP":
                board.append(file_content[a])
                a = a + 1
                if file_content[a + 1] == "GRID STOP":
                    stop_found = 1
        if file_content[i][0] == "A" and (
                file_content[i][2] != "x") and file_content[i][2] != "o":
            A_temp = []
            if len(file_content[i]) > 3:
                for j in range(2, len(file_content[i])):
                    A_temp.append(file_content[i][j])
                num_str_A = "".join(A_temp)
                A_blocks = int(num_str_A)
#                print("A",A_blocks)
            else:
                A_blocks = int(file_content[i][2])
        if file_content[i][0] == "B" and (
                file_content[i][2]) != "x" and file_content[i][2] != "o":
            B_temp = []
            if len(file_content[i]) > 3:
                for j in range(2, len(file_content[i])):
                    B_temp.append(file_content[i][j])
                num_str_B = "".join(B_temp)
                B_blocks = int(num_str_B)
            else:
                B_blocks = int(file_content[i][2])
        if file_content[i][0] == "C" and (
                file_content[i][2]) != "x" and file_content[i][2] != "o":
            C_temp = []
            if len(file_content[i]) > 3:
                for j in range(2, len(file_content[i])):
                    C_temp.append(file_content[i][j])
                num_str_C = "".join(C_temp)
                C_blocks = int(num_str_C)
#                print("C",C_blocks)
            else:
                C_blocks = int(file_content[i][2])
        if len(file_content[i]) != 0 and file_content[i][0] == "L":
            strip_lazor = file_content[i].split(" ")
            '''
            If wrong lazor input format
            '''
            if len(strip_lazor) != 5:
                raise Exception("Not correct number of lazor origin arguments")
            if strip_lazor[-2:] not in [["-1", "-1"], ["1", "1"], ["-1", "1"], ["1", "-1"]]:
                raise Exception("Your direction for a lazor is not right")

            for j in range(1, len(strip_lazor), 2):
                lazor_ori.append(
                    (int(strip_lazor[j]), int(strip_lazor[j + 1])))

        if len(file_content[i]) != 0 and file_content[i][0] == "P":
            hole.append([int(file_content[i][2]), int(file_content[i][4])])
    updated_board = []
    lazors = []

    for i in range(int(len(lazor_ori) / 2)):
        lazors.append([lazor_ori[2 * i], lazor_ori[2 * i + 1]])
    for x in board:
        lists = x.split()
        updated_board.append(lists)
    '''
    If no board present in the .bff file
    '''
    if len(updated_board) == 0:
        raise Exception("There is no board in your file")
    ocount = 0
    for i in range(len(updated_board)):
        for j in range(len(updated_board[0])):
            if updated_board[i][j] == 'o':
                ocount = ocount + 1

            '''
            If random characters other than the ones mentioned
            '''
            if updated_board[i][j].lower() not in ['x', 'o', 'a', 'c', 'b']:
                raise Exception("Board has characters other than x and o")
    # If more blocks than movable spaces
    if (A_blocks + B_blocks + C_blocks) > (ocount):
        raise Exception("There are more blocks than there are movable spaces")
    # If no blocks to place
    if A_blocks == 0 and B_blocks == 0 and C_blocks == 0:
        raise Exception("Your file has no blocks in it to place")
    # If lazor or hole out of bounds
    for i in range(len(lazors)):
        if lazors[i][0][0] > 2 * len(updated_board[0]) or lazors[i][0][0] < 0:
            raise Exception("A lazor is out of the bounds of the boards")
    for i in range(len(lazors)):
        if lazors[i][0][1] > 2 * len(updated_board) or lazors[i][0][0] < 0:
            raise Exception("A lazor is out of the bounds of the boards")
    for i in range(len(hole)):
        if hole[i][0] > 2 * len(updated_board[0]) or hole[i][0] < 0:
            raise Exception("A hole is out of the bounds of the boards")
    for i in range(len(hole)):
        if hole[i][1] > 2 * len(updated_board) or hole[i][0] < 0:
            raise Exception("A hole is out of the bounds of the boards")
    # If not enough lazors or holes
    if len(lazors) < 1:
        raise Exception("No lasers found")
    if len(hole) < 1:
        raise Exception("No holes found")
    if start_found == 0:
        raise Exception("Start not found")
    if stop_found == 0:
        raise Exception("Stop not found")
    return(updated_board, A_blocks, B_blocks, C_blocks, lazors, hole)


def create_grid(grid, permut):
    '''
        Creates a grid as explained in the top section for the given board
        for eg. if board is 2 x 2 matrix
        Board - o A
                B o
        Grid so generated - x x x x x
                            x o x A x
                            x x x x x
                            x B x o x
                            x x x x x
        *** Parameters ***
        self - consists of all data (board, A_blocks, B_blocks, C_blocks .. )
        *** Returns ***
        a (2n + 1) x (2m +1) matrix (grid) if board size is n x m
    '''
    value = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'o':
                grid[i][j] = permut[value]
                value += 1
    return grid


def next_step(grid, pos, direc):
    '''
    This function is to calculate the next step the lazor will take
    depending on the type of the block it intersects, and its position
    *** Parameters ***
    grid - List of lists : consisting of the board on which the lazor moves
    pos - array : current position of the lazor
    direc - array : current direction of the lazor
    *** Returns ***
    new_dir = new direction the lazor is taking depending on the type
    of the block it interacts with and its orginal direction
    (-1, -1)             (1, -1)
                 *
    (-1, 1)               (1, 1)
    * - is the current location of the lazor
    and the 4 coordinates are it are the 4 directions possible
    for the movement of lazor
    '''
    x = pos[0]
    y = pos[1]
    if y % 2 == 0:
        '''
        If y is even then block lies above or below
        '''
        if grid[y + direc[1]][x].lower() == 'o' or (
                grid[y + direc[1]][x].lower() == 'x'):
            new_dir = direc
        elif grid[y + direc[1]][x].lower() == 'a':
            new_dir = [direc[0], -1 * direc[1]]
        elif grid[y + direc[1]][x].lower() == 'b':
            new_dir = []
        elif grid[y + direc[1]][x].lower() == 'c':
            direc1 = direc
            direc2 = [direc[0], -1 * direc[1]]
            new_dir = [direc1[0], direc1[1], direc2[0], direc2[1]]
    else:
        '''
        If y is odd the block is left or right
        '''
        if grid[y][x + direc[0]].lower() == 'o' or (
                grid[y][x + direc[0]].lower() == 'x'):
            new_dir = direc
        elif grid[y][x + direc[0]].lower() == 'a':
            new_dir = [-1 * direc[0], direc[1]]
        elif grid[y][x + direc[0]].lower() == 'b':
            new_dir = []
        elif grid[y][x + direc[0]].lower() == 'c':
            direc1 = direc
            direc2 = [-1 * direc[0], direc[1]]
            new_dir = [direc1[0], direc1[1], direc2[0], direc2[1]]
    return new_dir


def boundary_check(grid, pos, direc):
    '''
    This function just checks if the current lazor position and the next
    possible position is within the boundary of the grid or not
    If it is then we can continue with the lazor or else the lazor is dead
    as it crosses the boundary of the board/grid
    ** Parameters **
    grid - List of Lists : consisting of the board on which the lazor moves
    pos - Array : Current position of the lazor
    direc - Array : Current direction of the lazor
    ** Returns **
    True or False - depending upon if the point is in or out of the boundary
    '''
    x = pos[0]
    y = pos[1]
    y_max = len(grid) - 1
    x_max = len(grid[0]) - 1
    if x < 0 or x > x_max or y < 0 or y > y_max or (x + direc[0]) < 0 or (
        x + direc[0]) > x_max or (y + direc[1]) < 0 or (
            y + direc[1]) > y_max:
        return True
    else:
        return False


def lazor_path(grid, lazors, sinks):
    '''
    This function is the main lazor solver for the given/ generated
    board. The stack of lazors consists of the lazor path for all lazors
    available. It is appending after each step all the lazors take.
    If in their path they intersect the hole, that point is then removed
    from the hole list. As soon as the whole list is empty, the while loop
    breaks and it returns True i.e Solved; else the loop goes on till Maximum
    Iterations are reached.
    *** Parameters ***
    grid - List of lists: consisting of the board on which the lazor moves
    lazaors - Array: Consisting of origin and direction of each lazor
    sinks - Array : consists of all the hole/sinks points
    ***Returns***
    Stack_lazors - list of lists: having coordinates the lazor took to
    reach the hole
    '''

    # list of all lazors and and each lazor list has its path
    stack_lazors = []
    for i in range(len(lazors)):
        stack_lazors.append([lazors[i]])
    ITER = 0
    MAX_ITER = 100
    while len(sinks) != 0 and ITER <= MAX_ITER:
        ITER += 1
        for i in range(len(stack_lazors)):
            lazor_pos = list(stack_lazors[i][-1][0])
            direc = list(stack_lazors[i][-1][1])
            if boundary_check(grid, lazor_pos, direc):
                continue
            else:
                new_dir = next_step(grid, lazor_pos, direc)
                if len(new_dir) == 0:
                    stack_lazors[i].append([lazor_pos, direc])
                elif len(new_dir) == 2:
                    direc = new_dir
                    lazor_pos = [lazor_pos[0] +
                                 direc[0], lazor_pos[1] + direc[1]]
                    stack_lazors[i].append([lazor_pos, direc])
                else:
                    direc = new_dir
                    lazor_pos1 = [lazor_pos[0] +
                                  direc[0], lazor_pos[1] + direc[1]]
                    lazor_pos2 = [lazor_pos[0] +
                                  direc[2], lazor_pos[1] + direc[3]]
                    stack_lazors.append([[lazor_pos1, [direc[0], direc[1]]]])
                    stack_lazors[i].append([lazor_pos2, [direc[2], direc[3]]])
                    lazor_pos = lazor_pos2
            if lazor_pos in sinks:
                    sinks.remove(lazor_pos)
    if len(sinks) == 0:
        return (True, stack_lazors)
    else:
        return (False, stack_lazors)


def unit_test():
    # Dark_1.bff
    grid = [['x', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'x']]
    A_blocks = 0
    B_blocks = 3
    C_blocks = 0
    lazors = [[(3, 0), (-1, 1)], [(1, 6), (1, -1)],
              [(3, 6), (-1, -1)], [(4, 3), (1, -1)]]
    hole = [[0, 3], [6, 1]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'B', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'B', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("dark_1.bff") == (grid, A_blocks,
                                      B_blocks, C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Mad_1.bff
    grid = [['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
    A_blocks = 2
    B_blocks = 0
    C_blocks = 1
    lazors = [[(2, 7), (1, -1)]]
    hole = [[3, 0], [4, 3], [2, 5], [4, 7]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'c', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("mad_1.bff") == (grid, A_blocks,
                                     B_blocks, C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Mad_4.bff
    grid = [['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o']]
    A_blocks = 5
    B_blocks = 0
    C_blocks = 0
    lazors = [[(7, 2), (-1, 1)]]
    hole = [[3, 4], [7, 4], [5, 8]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'A', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("mad_4.bff") == (grid, A_blocks, B_blocks,
                                     C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Mad_7.bff
    grid = [['o', 'o', 'o', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'x'], ['o', 'o', 'o', 'o', 'o'],
            ['o', 'o', 'o', 'o', 'o']]
    A_blocks = 6
    B_blocks = 0
    C_blocks = 0
    lazors = [[(2, 1), (1, 1)], [(9, 4), (-1, 1)]]
    hole = [[6, 3], [6, 5], [6, 7], [2, 9], [9, 6]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'A', 'x', 'o', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("mad_7.bff") == (grid, A_blocks, B_blocks,
                                     C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Numbered_6.bff
    grid = [['o', 'o', 'o'], ['o', 'x', 'x'], ['o', 'o', 'o'],
            ['o', 'x', 'o'], ['o', 'o', 'o']]
    A_blocks = 3
    B_blocks = 3
    C_blocks = 0
    lazors = [[(4, 9), (-1, -1)], [(6, 9), (-1, -1)]]
    hole = [[2, 5], [5, 0]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'x', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'o', 'x']]
    assert read_bff("numbered_6.bff") == (grid, A_blocks, B_blocks,
                                          C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Showstopper_4.bff
    grid = [['B', 'o', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']]
    A_blocks = 3
    B_blocks = 3
    C_blocks = 0
    lazors = [[(3, 6), (-1, -1)]]
    hole = [[2, 3]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'A', 'x', 'B', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'B', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("showstopper_4.bff") == (grid, A_blocks, B_blocks,
                                             C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Tiny_5.bff
    grid = [['o', 'B', 'o'], ['o', 'o', 'o'], ['o', 'o', 'o']]
    A_blocks = 3
    B_blocks = 0
    C_blocks = 1
    lazors = [[(4, 5), (-1, -1)]]
    hole = [[1, 2], [6, 3]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'B', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'C', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("tiny_5.bff") == (grid, A_blocks, B_blocks,
                                      C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True
    # Yarn_5.bff
    grid = [['o', 'B', 'x', 'o', 'o'], ['o', 'o', 'o', 'o', 'o'],
            ['o', 'x', 'o', 'o', 'o'], ['o', 'x', 'o', 'o', 'x'],
            ['o', 'o', 'x', 'x', 'o'], ['B', 'o', 'x', 'o', 'o']]
    A_blocks = 8
    B_blocks = 0
    C_blocks = 0
    lazors = [[(4, 1), (1, 1)]]
    hole = [[6, 9], [9, 2]]
    solved_grid = [['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'B', 'x', 'x', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'A', 'x', 'o', 'x', 'o', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'x', 'x', 'o', 'x', 'o', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'o', 'x', 'x', 'x', 'A', 'x', 'o', 'x', 'x', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'A', 'x', 'o', 'x', 'x', 'x', 'x', 'x', 'A', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                   ['x', 'B', 'x', 'A', 'x', 'x', 'x', 'A', 'x', 'o', 'x'],
                   ['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x']]
    assert read_bff("yarn_5.bff") == (grid, A_blocks, B_blocks,
                                      C_blocks, lazors, hole)
    assert lazor_path(solved_grid, lazors, hole)[0] == True


if __name__ == "__main__":
    filename = "dark_1.bff"
    (board_given, A_blocks, B_blocks,
        C_blocks, lazors, hole) = read_bff(filename)
    print("**** Welcome to the CPW Lazor Solver ****")
    print("Given Board :- ")
    for y in board_given:
        for x in y:
            print(x, end=' ')
        print()
    print("Type of Blocks given A(reflective) : %d " % (A_blocks) +
          "B(opaque) : %d, C(Refractive) : %d " % (B_blocks, C_blocks))
    unit_test()
    time_start = time.time()
    Board = Grid(board_given, A_blocks, B_blocks, C_blocks, lazors, hole)
    Board.blocks(filename)
    time_end = time.time()
    print('Run time: %f seconds' % (time_end - time_start))