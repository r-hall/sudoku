# Overview #
Programmed a Sudoku solver using constraint propagation and backtracking search. In this implementation, the same integer may not appear twice in any row, column, square or main diagonal. 

# Theory #
## Constraint Satisfaction Problem ##
A constraint satisfaction problem consists of three elements:
- A set of **variables**, X = _{X1, X2, ··· Xn}_
- A set of **domains** for each variable: D = _{D1, D2, ··· Dn}_
- A set of **constraints** that specify allowable combinations of values

A solution to a constraint satisfaction problem is an assignment for every variable such that all constraints are satisfied. The variables are the set of cells in the 9x9 Sudoku grid. The domain for all cells consists of the integers 1-9. The constraints in this problem are binary. No two variables in the same unit (row, column, square or main diagonal) may share the same value.  

## Constraint Propagation ##
We can say that X → Y is arc-consistent, where X and Y are variables, if and only if every value x in X is consistent with at least one value y in Y. We can use these binary constraints to iteratively remove values from the set of possible values for each variable based upon the assigned value of other variables from the same unit. For example, if we are given that the top left corner, 'A1', has a value of 1, then we can remove 1 from the set of possible values for all cells in the top left square, the first column, the first row and the major diagonal. Through this process, if we discover that a variable only has one possible remaining value or a particular value in a unit is only possible in a single cell, then we can formally assign the value to that variable and repeat this process.

## Backtracking Search ##
Often when proceeding through a constraint propagation algorithm we will reach a point where no further eliminations can be made to the set of possible values of any variable and the problem remains unsolved. In this case we must pick a variable and try each of its remaining possible values. When selecting the variable we should select the one with the fewest possible remaining values. This will result in a search tree with a smaller branching factor. 

After each assignment in the search we will again execute the constraint propagation algorithm and if at any point we discover that a variable has zero remaining possible values the search function will return false and backtrack to the most recent working set of assignments. 

# Output #
When executed, the program will write to a file called output.txt, containing the following:

	1. solved board: the solved board as a string
	
	2. solution method: AC3 (only CP was used) or BTS (both CP and BTS)
	
