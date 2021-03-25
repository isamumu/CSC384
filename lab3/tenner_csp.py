#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.  

'''
Construct and return Tenner Grid CSP models.
'''

from cspbase import *
import itertools

def tenner_csp_model_1(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner grid using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.
       
       
       The input board is specified as a pair (n_grid, last_row). 
       The first element in the pair is a list of n length-10 lists.
       Each of the n lists represents a row of the grid. 
       If a -1 is in the list it represents an empty cell. 
       Otherwise if a number between 0--9 is in the list then this represents a 
       pre-set board position. E.g., the board
    
       ---------------------  
       |6| |1|5|7| | | |3| |
       | |9|7| | |2|1| | | |
       | | | | | |0| | | |1|
       | |9| |0|7| |3|5|4| |
       |6| | |5| |0| | | | |
       ---------------------
       would be represented by the list of lists
       
       [[6, -1, 1, 5, 7, -1, -1, -1, 3, -1],
        [-1, 9, 7, -1, -1, 2, 1, -1, -1, -1],
        [-1, -1, -1, -1, -1, 0, -1, -1, -1, 1],
        [-1, 9, -1, 0, 7, -1, 3, 5, 4, -1],
        [6, -1, -1, 5, -1, 0, -1, -1, -1,-1]]
       
       
       This routine returns model_1 which consists of a variable for
       each cell of the board, with domain equal to {0-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       model_1 contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.).
       model_1 also constains n-nary constraints of sum constraints for each 
       column.
    '''
    
    #IMPLEMENT

    # what constraints do I need:
    # --> row constraints, column constraints, block constraints, sub-square constraints (All - Diff(...))
    rows = len(initial_tenner_board[0]) # variable row value
    tenner = [[0 for x in range(10)] for y in range(rows)] # board matrix

    # set up the board
    for i in range(rows):
        for j in range(10):
            pos = initial_tenner_board[0][i][j]

            # check for empty cells; if empty 
            if pos == -1:
                tenner[i][j] = Variable("V{}{}".format(i,j), list(range(10)))
            else:
                tenner[i][j] = Variable("V{}{}".format(i,j), [pos])

    # create the tenner CSP object here so we can keep adding constraints in successive functions
    # --> would like to avoid having too many moving parts, so the approach will be to sequentially check the adjacent boxes
    tenner_csp = CSP("tenner_model_1", [tenner[x][y] for x in range(rows) for y in range(10)])

    # add the constraints 
    for x in range(rows):
        for y in range(10):
            # vertical constraints 
            for z in range(y+1, 10): # check the constraints for every consecutive value down 
                con = Constraint("row", [tenner[x][y], tenner[x][z]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x][z].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

            # diagonal constraints ---> with slope of 1
            if x != (rows-1) and y != 9: # check for the out of bounds condition and off by 1 consition for the column index
                # ensure that for the negative slope, that we are considering elements that are less than 9 since we have only 10 indices which include index 0
                con = Constraint("upDiagonal", [tenner[x][y], tenner[x+1][y+1]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x+1][y+1].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

            # diagonal constraints ---> with slope of -1
            if x != (rows-1) and y != 0: # check for the out of bounds condition and off by 1 consition for the column index
                # ensure that for the negative slope, that we are considering elements that are at least greater than 1
                con = Constraint("downDiagonal", [tenner[x][y], tenner[x+1][y-1]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x+1][y-1].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

            # horizontal constraints ---> check the right adjacent cells
            if x != (rows-1): # check for the out of bounds condition
                con = Constraint("column", [tenner[x][y], tenner[x+1][y]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x+1][y].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

    # check for sum constraints 
    for col in range(10): # loop through the column indices to check for the sum constraints 
        col_domain = [tenner[x][col].cur_domain() for x in range(rows)] # obtain a list of domains for each column
        con = Constraint("sum of index " + str(col), [tenner[i][col] for i in range(rows)]) # create constraint object

        for prod in itertools.product(*col_domain): # use itertools to find every combination which satisfies the sum constraint
            if sum(prod) == initial_tenner_board[1][col]:
                con.add_satisfying_tuples([prod])
        tenner_csp.add_constraint(con)
    return tenner_csp, tenner #CHANGE THIS
##############################

def tenner_csp_model_2(initial_tenner_board):
    '''Return a CSP object representing a Tenner Grid CSP problem along 
       with an array of variables for the problem. That is return

       tenner_csp, variable_array

       where tenner_csp is a csp representing tenner using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the Tenner Grid (only including the first n rows, indexed from 
       (0,0) to (n,9)) where n can be 3 to 7.

       The input board takes the same input format (a list of n length-10 lists
       specifying the board as tenner_csp_model_1.
    
       The variables of model_2 are the same as for model_1: a variable
       for each cell of the board, with domain equal to {0-9} if the
       board has a -1 at that position, and domain equal {i} if the board
       has a fixed number i at that cell.

       However, model_2 has different constraints. In particular, instead
       of binary non-equals constaints model_2 has a combination of n-nary 
       all-different constraints: all-different constraints for the variables in
       each row, and sum constraints for each column. You may use binary 
       contstraints to encode contiguous cells (including diagonally contiguous 
       cells), however. Each -ary constraint is over more 
       than two variables (some of these variables will have
       a single value in their domain). model_2 should create these
       all-different constraints between the relevant variables.
    '''

    #IMPLEMENT
    # # NOTE DIFFERENCE: these constraints are derived from a combination of n-ary all-different constraints
    # # ie. row constraints and sum of column constraints. Also consider contiguous (diagonal) constraints too

    rows = len(initial_tenner_board[0]) # variable row value
    tenner = [[0 for x in range(10)] for y in range(rows)] # board matrix

    # set up the board
    for i in range(rows):
        for j in range(10):
            pos = initial_tenner_board[0][i][j]

            # check for empty cells; if empty 
            if pos == -1:
                tenner[i][j] = Variable("V{}{}".format(i,j), list(range(10)))
            else:
                tenner[i][j] = Variable("V{}{}".format(i,j), [pos])
    
    tenner_csp = CSP("tenner_model_2", [tenner[x][y] for x in range(rows) for y in range(10)])

    
    for x in range(rows):
        # idea is to find elements in a given row and add the ones that currently do not exist 
        # this will hopefully find the n-ary values for each row, allowing for an all diff constraint
        sat_tuples = []
        domain = list([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
        items = []

        # add the n-ary all diff constraints here
        for y in range(10):
            if tenner[x][y] == -1:
                items.append(tenner[x][y])
            else:
                if tenner[x][y] in domain:
                    tenner.remove(tenner[x][y])
        
        # find the satisfying tuples here:
        for i in itertools.permutations(domain, len(items)):
            sat_tuples.append(i)

        # all variables should have 10 variables because 10 variables per row
        con = Constraint("n-ary row: " + str(x), items)
        con.add_satisfying_tuples(sat_tuples)
        tenner_csp.add_constraint(con)

        for y in range(10):

            # diagonal constraints ---> with slope of 1
            if x != (rows-1) and y != 9: # check for the out of bounds condition and off by 1 consition for the column index
                # ensure that for the negative slope, that we are considering elements that are less than 9 since we have only 10 indices which include index 0
                con = Constraint("upDiagonal", [tenner[x][y], tenner[x+1][y+1]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x+1][y+1].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

            # diagonal constraints ---> with slope of -1
            if x != (rows-1) and y != 0: # check for the out of bounds condition and off by 1 consition for the column index
                # ensure that for the negative slope, that we are considering elements that are at least greater than 1
                con = Constraint("downDiagonal", [tenner[x][y], tenner[x+1][y-1]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x+1][y-1].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

            # horizontal constraints ---> check the right adjacent cells
            if x != (rows-1): # check for the out of bounds condition
                con = Constraint("column", [tenner[x][y], tenner[x+1][y]]) # create row constraint object
                array = []
                for i in tenner[x][y].domain():
                    for j in tenner[x+1][y].domain():
                        if i != j:
                            array.append((i,j))
                con.add_satisfying_tuples(array)
                tenner_csp.add_constraint(con)

    # check for sum of column constraints 
    for col in range(10): # loop through the column indices to check for the sum constraints 
        col_domain = [tenner[x][col].cur_domain() for x in range(rows)] # obtain a list of domains for each column
        con = Constraint("sum of index " + str(col), [tenner[i][col] for i in range(rows)]) # create constraint object

        for prod in itertools.product(*col_domain): # use itertools to find every combination which satisfies the sum constraint
            if sum(prod) == initial_tenner_board[1][col]:
                con.add_satisfying_tuples([prod])
        tenner_csp.add_constraint(con)

    return tenner_csp, tenner #CHANGE THIS
    # return None, None