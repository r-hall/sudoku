#import sys
import copy

# 9 x 9 sudoku board
rows = 'ABCDEFGHI'
cols = '123456789'

def cross_product(a, b):
    return [s+t for s in a for t in b]

# get list of all cells
cells = cross_product(rows, cols)
# get list of all rows (list of lists)
row_unit_list = [cross_product(r, cols) for r in rows]
# get list of all columns (list of lists)
column_unit_list = [cross_product(rows, c) for c in cols]
# get list of all squares (list of lists)
square_unit_list = [cross_product(r, c) for r in ('ABC','DEF','GHI') for c in ('123','456','789')]
# get list of both diagonals
d1 = [rows[i]+cols[i] for i in range(len(rows))]
d2 = [rows[i]+cols[len(rows)-1-i] for i in range(len(rows))]
diagonal_list = [d1, d2]
# list of a units
unit_list = row_unit_list + column_unit_list + square_unit_list + diagonal_list
all_units = dict((s, [u for u in unit_list if s in u]) for s in cells)
# get list of all peers for each cell
all_peers = dict((s, set(sum(all_units[s],[]))-set([s])) for s in cells)

def string_to_dict(input_string):
    """
    Convert grid string into dict with '123456789' value boxes
    that do not initially have an assigned value

    Input:
        Sudoku string: puzzle in string form
    
    Output:
        Sudoku dictionary with value in corresponding box 
        such as '3', or '123456789' if it is not given initially
    """
    cell_values = []
    all_nums = '123456789'
    for num in input_string:
        if num == '.':
            cell_values.append(all_nums)
        elif num in all_nums:
            cell_values.append(num)
    return dict(zip(cells, cell_values))

def eliminate(puzzle):
    """
    Go through all cells and if there is a completed cell, eliminate this value 
    from the possible values of all of its peers
    """
    completed_cells = [cell for cell in puzzle.keys() if len(puzzle[cell]) == 1]
    for cell in completed_cells:
        value = puzzle[cell]
        for peer in all_peers[cell]:
            puzzle[peer] = puzzle[peer].replace(value,'')
    return puzzle

def finalize_value(puzzle):
    """
    Go through all units and if there is a value for a particular unit that
    is only allowable in one cell, assign the value to that cell.
    """
    for unit in unit_list:
        for value in '123456789':
            cell_length = [cell for cell in unit if value in puzzle[cell]]
            if len(cell_length) == 1:
                puzzle[cell_length[0]] = value
    return puzzle

def naked_twins(puzzle):
    """
    If there are "naked twins" in a unit then remove those values as options
    from all other boxes in that unit
    Input: Sudoku in dictionary form
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    # get all cells that have two options remaining
    potential_twins = [cell for cell in puzzle.keys() if len(puzzle[cell]) == 2]
    # get all actual naked twins form potential_twins
    naked_twins = [[cell1, cell2] for cell1 in potential_twins for cell2 in all_peers[cell1] if set(puzzle[cell1])==set(puzzle[cell2]) ]

    for i in range(len(naked_twins)):
        cell1 = naked_twins[i][0]
        cell2 = naked_twins[i][1]
        peers1 = set(all_peers[cell1])
        peers2 = set(all_peers[cell2])
        # get all cells that are peers of both cell1 and cell2
        peers_intersection = peers1 & peers2
        # remove both naked twin values from all peers in peers_intersection
        for peer in peers_intersection:
            if len(puzzle[peer]) > 2:
                for naked_twin_value in puzzle[cell1]:
                    puzzle[peer] = puzzle[peer].replace(naked_twin_value,'')
    return puzzle

def reduce_puzzle(puzzle):
    """
    Reduce the values in the domain of each variable through iterative 
    constraint propagation
    """
    stalled = False
    while not stalled:
        # Get the number of completed cells
        solved_values_before = len([cell for cell in puzzle.keys() if len(puzzle[cell]) == 1])
        # Try to eliminate values in the domain for each variable
        puzzle = eliminate(puzzle)
        # Consider naked twins
        puzzle = naked_twins(puzzle)
        # Finalize values for cells if that value only appears in that cell for that unit
        puzzle = finalize_value(puzzle)
        # Get the new number of completed cells
        solved_values_after = len([cell for cell in puzzle.keys() if len(puzzle[cell]) == 1])
        # If no progress was made, stop the loop
        stalled = solved_values_before == solved_values_after
        # Return False if there is a variable with no remaining values in its domain
        if len([cell for cell in puzzle.keys() if len(puzzle[cell]) == 0]):
            return False
    return puzzle

def search(puzzle):
    """
    Use depth-first search and constraint propagation to solve the puzzle
    """
    # First, reduce the puzzle using the reduce_puzzle function
    puzzle = reduce_puzzle(puzzle)
    if puzzle is False:
        return False ## Failed earlier
    if all(len(puzzle[cell]) == 1 for cell in cells): 
        return puzzle ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    minVal = 10
    minBox = None
    for cell in puzzle:
        if len(puzzle[cell]) > 1 and len(puzzle[cell]) < minVal:
            minVal = len(puzzle[cell])
            minBox = cell
    # try each possible option available for this square
    for option in puzzle[minBox]:
        newValues = copy.deepcopy(puzzle)
        newValues[minBox] = option
        attempt = search(newValues)
        # if the puzzle was solved return the solution, otherwise move to next option
        if attempt:
            return attempt

def solve(input_string):
    """
    Try constraint propagation and, if that doesn't yield a solution, backtracking search
    """
    #input_string = str(sys.argv[1])
    puzzle = string_to_dict(input_string)
    puzzle = reduce_puzzle(puzzle)
    if all(len(puzzle[cell]) == 1 for cell in cells):
        output_values = [puzzle[cell] for cell in cells]
        with open('output.txt', 'w') as f:
            f.write(''.join(output_values) + ' AC3')
            return ''.join(output_values) + ' AC3'
    puzzle = search(puzzle)
    if all(len(puzzle[cell]) == 1 for cell in cells):
        output_values = [puzzle[cell] for cell in cells]
        with open('output.txt', 'w') as f:
            f.write(''.join(output_values) + ' BTS')
            return ''.join(output_values) + ' BTS'
        
print(solve('2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'))
    