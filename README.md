# Overview #
Programmed a Sudoku solver using constraint propagation and backtracking search. In this implementation, the same integer may not appear twice in any row, column, square or main diagonal. 

# Theory #
## Constraint Satisfaction Problem (CSP) ##
A constraint satisfaction problem consists of three elements:
- A set of **variables**, X = _{X1, X2, ··· Xn}_
- A set of **domains** for each variable: D = _{D1, D2, ··· Dn}_
- A set of **constraints** C that specify allowable combinations of values

A solution to a CSP is an assignment for every variable such that all constraints are satisfied. The variables are the set of squares in the 9x9 Sudoku grid. The initial domain for all squares consists of the integers 1-9. The constraints in this problem are binary. No two integers in the same unit (row, column, square or main diagonal) may share the same value.  

## Constraint Propagation (CP) ##
TBD 

## Backtracking Search (BTS) ##
TBD

# Output #
When executed, the program will write to a file called output.txt, containing the following:

	1. solved board: the solved board as a string
	
	2. solution method: AC3 (only CP was used) or BTS (both CP and BTS)
	
