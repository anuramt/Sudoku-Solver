#!/usr/bin/env python3

"""Backtracking algorithm to solve Sudoku puzzles.

License:
    MIT License

    Copyright (c) 2022 Anuram T

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

# Standard imports
import copy

# Third-party imports
import numpy


def solve_sudoku(arr: numpy.ndarray, index: int = 0) -> numpy.ndarray:
    """Solves a 9x9 Sudoku array.

    Parameters:
        arr: 9x9 array to be solved with Sudoku rules and backtracking.
        index: The position in the array which the function is solving
            for. Do not specify the index when calling the function!
            (default 0)

    Returns:
        A solved 9x9 Sudoku array. If unsolvable, returns the original
        arr argument.
    """

    # Deepcopies the original array in case the function needs to return
    # it (when a possible route fails to solve the array).
    orig_arr = copy.deepcopy(arr)

    # Fills elements in the array where there is only one possible
    # value. Continues to fill the array until there are only elements
    # with multiple possible values left.
    arr = fill_sudoku(arr)

    # Calculates the row and column of the element which the function is
    # finding a valid value for.
    row = index // 9
    col = index % 9

    # If the array has been solved, return the array.
    #
    # If the element does not need solving (there is already a
    # value from 1 to 9), solve the rest of the array. If the returned
    # array is solved, return the array. If not, return the original
    # array (because this solution branch has failed).
    #
    # Otherwise, get the possible values for the current element and
    # iterate through each value until you get a returned array which is
    # fully solved. If there are no values that returns a fully solved
    # array, return the original array (because this solution branch
    # has failed).
    if is_solved(arr):
        return arr
    elif arr[row][col] != 0:
        arr = solve_sudoku(arr, index + 1)

        if is_solved(arr):
            return arr
        else:
            return orig_arr
    else:
        for val in get_possible(arr, row, col):
            arr[row][col] = val

            if is_solved(arr):
                return arr
            elif index != 80:
                arr = solve_sudoku(arr, index + 1)

                if is_solved(arr):
                    return arr

        return orig_arr


def fill_sudoku(arr: numpy.ndarray) -> numpy.ndarray:
    """Fills Sudoku array elements that have only one possible value.

    Parameters:
        arr: 9x9 array to be filled using Sudoku rules.

    Returns:
        A filled 9x9 Sudoku array. If no elements can be filled, returns
        the original arr argument.
    """

    # Iterates through each element and fills elements that have only
    # one possible value. If any element has been filled (by comparing
    # it to the array before being filled), the loop iterates through
    # each element again. This continues until no more elements can be
    # filled.
    while True:
        orig_arr = copy.deepcopy(arr)

        arr = fill_rows(arr)
        arr = fill_columns(arr)
        arr = fill_subgrids(arr)

        if (arr == orig_arr).all():
            break

    return arr


def fill_rows(arr: numpy.ndarray) -> numpy.ndarray:
    """Fills Sudoku array elements that have only one possible value.

    Parameters:
        arr: 9x9 array to be filled using Sudoku row rules.

    Returns:
        A filled 9x9 Sudoku array. If no elements can be filled, returns
        the original arr argument.
    """
    
    # Iterates through each row and iterates through values 1 to 9,
    # checking if the value is only possible in one element in the row.
    # If so, sets the element in the row as that value. Continues to
    # check every row with every value and fills elements where
    # possible.
    for row in range(9):
        for val in range(1, 10):
            possible_cells = []

            for col in range(9):
                if arr[row][col] == 0:
                    if is_valid(arr, row, col, val):
                        possible_cells.append((row, col))

                if len(possible_cells) > 1:
                    break

            if len(possible_cells) == 1:
                r, c = possible_cells[0]
                arr[r][c] = val

    return arr


def fill_columns(arr: numpy.ndarray) -> numpy.ndarray:
    """Fills Sudoku array elements that have only one possible value.

    Parameters:
        arr: 9x9 array to be filled using Sudoku column rules.

    Returns:
        A filled 9x9 Sudoku array. If no elements can be filled, returns
        the original arr argument.
    """
    
    # Iterates through each column and iterates through values 1 to 9,
    # checking if the value is only possible in one element in the
    # column. If so, sets the element in the column as that value.
    # Continues to check every column with every value and fills
    # elements where possible.
    for col in range(9):
        for val in range(1, 10):
            possible_cells = []

            for row in range(9):
                if arr[row][col] == 0:
                    if is_valid(arr, row, col, val):
                        possible_cells.append((row, col))

                if len(possible_cells) > 1:
                    break

            if len(possible_cells) == 1:
                r, c = possible_cells[0]
                arr[r][c] = val

    return arr


def fill_subgrids(arr: numpy.ndarray) -> numpy.ndarray:
    """Fills Sudoku array elements that have only one possible value.

    Parameters:
        arr: 9x9 array to be filled using Sudoku subgrid rules.

    Returns:
        A filled 9x9 Sudoku array. If no elements can be filled, returns
        the original arr argument.
    """

    # Iterates through each subgrid and iterates through values 1 to 9,
    # checking if the value is only possible in one element in the
    # subgrid. If so, sets the element in the subgrid as that value.
    # Continues to check every subgrid with every value and fills
    # elements where possible.
    for row_start in [0, 3, 6]:
        for col_start in [0, 3, 6]:
            for val in range(1, 10):
                possible_cells = []

                for row in range(row_start, row_start + 3):
                    for col in range(col_start, col_start + 3):
                        if arr[row][col] == 0:
                            if is_valid(arr, row, col, val):
                                possible_cells.append((row, col))

                        if len(possible_cells) > 1:
                            break

                    if len(possible_cells) > 1:
                        break

                if len(possible_cells) == 1:
                    r, c = possible_cells[0]
                    arr[r][c] = val

    return arr


def get_possible(arr: numpy.ndarray, row: int, col: int) -> list:
    """Returns a list of the most probable values for an element.

    Parameters:
        arr: 9x9 Sudoku array to check element possibilities for.
        row: Row of element to check possibilities for. 
        col: Column of element to check possibilities for.

    Returns:
        Returns a list of the most probable values for an element,
        using Sudoku rules to reduce the number of possible values.
        Helpful for reducing the amount of backtracking.
    """

    # Gets all the possible values for the element
    possible = [val for val in range(1, 10) if is_valid(arr, row, col, val)]
    occurences = {}
    probable = []

    # Finds the rows of the subgrid the element is in. For each row the
    # element is not located in and which are not filled completely,
    # we iterate through each value in the row. If that value is a 
    # possible value for the element, we use a dictionary to store
    # the amount of occurences of the value.
    for sub_row in [get_subgrid_start(row) + i for i in range(3)]:
        if sub_row != row:
            sub_row_vals = [val for val in arr[sub_row]]

            if 0 in sub_row_vals:
                for val in sub_row_vals:
                    if val != 0 and val in possible:
                        if val in occurences.keys():
                            occurences[val] += 1
                        else:
                            occurences[val] = 1

    # Finds the columns of the subgrid the element is in. For each
    # column the element is not located in and which are not filled
    # completely, we iterate through each value in the column. If that
    # value is a possible value for the element, we use a dictionary to
    # store the amount of occurences of the value.
    for sub_col in [get_subgrid_start(col) + i for i in range(3)]:
        if sub_col != col:
            sub_col_vals = [arr[arow][sub_col] for arow in range(9)]

            if 0 in sub_col_vals:
                for val in sub_col_vals:
                    if val != 0 and val in possible:
                        if val in occurences.keys():
                            occurences[val] += 1
                        else:
                            occurences[val] = 1

    # Using the amount of occurences of each possible value, we can
    # predict which values will most likely be the right one, so we
    # append the values to a list in order of most occured to least.
    for num in range(4, 0, -1):
        if num in occurences.values():
            for key in occurences.keys():
                if num == occurences[key]:
                    probable.append(key)

    return probable


def is_solved(arr: numpy.ndarray) -> bool:
    """Checks if an array is fully solved using Sudoku rules.

    Parameters:
        arr: 9x9 Sudoku array to check if fully solved.
    
    Returns:
        True if the array is fully solved, else returns False.
    """

    # Iterates through each element in the array and checks if the 
    # value assigned to it is valid using Sudoku rules.
    for row in range(9):
        for col in range(9):
            val = arr[row][col]

            if val == 0:
                return False
            else:
                arr[row][col] = 0

                if not is_valid(arr, row, col, val):
                    return False

                arr[row][col] = val

    return True


def is_valid(arr: numpy.ndarray, row: int, col: int, val: int) -> bool:
    """Checks if a value in a certain element follows Sudoku rules.

    Assumes the element is empty (the value of the cell is 0).

    Parameters:
        arr: 9x9 Sudoku array to check value validity for.
        row: Row of element to check value validity for. 
        col: Column of element to check value validity for.
        val: The value to check validity for in a certain element.

    Returns:
        True if the value is valid in the element, else returns False.
    """

    # Values in the column of the element
    elem_col = [arr[row][col] for row in range(9)]

    # Getting the values in the subgrid of the element
    elem_subgrid = []
    row_start = get_subgrid_start(row)
    col_start = get_subgrid_start(col)

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start+3):
            elem_subgrid.append(arr[r][c])

    # Checking if the value is in the row, column, or subgrid of
    # the element
    if val not in arr[row] and val not in elem_col:
        if val not in elem_subgrid:
            return True

    return False


def get_subgrid_start(val: int) -> int:
    """Returns the first row/column index of a subgrid in a 9x9 array.

    The Sudoku subgrid is determined by the parameter val, w

    Parameters:
        val: A row or column of a 9x9 Sudoku array, which determines
            what subgrid index to return.

    Returns:
        The first row/column index of a subgrid in a 9x9 Sudoku array.
        For example, if an element's row was located in the middle
        of the array, the function would return 3.
    """

    if 0 <= val <= 2:
        subgrid_start = 0
    elif 3 <= val <= 5:
        subgrid_start = 3
    elif 6 <= val <= 8:
        subgrid_start = 6

    return subgrid_start