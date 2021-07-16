"""
Solution to the Digits Tracking puzzle.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Eric Zettermann (July, 2021), MipMaster.org.
"""

import pulp

# region Input Data

# columns
I = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}
# digits
K = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

# keys for decision variables x
keys = [(i, k) for i in I for k in K]
# endregion

# region Define the model
mdl = pulp.LpProblem('digits_tracking', sense=pulp.LpMaximize)

# add variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')

# add constraints
# exactly one digit is assigned to each cell
for i in I:
    mdl.addConstraint(pulp.lpSum(x[(i, k)] for k in K) == 1, name=f'One-digit-per-cell-{i}')

# If the digit k is assigned to cell i, then i must appear k times in the grid.
for i in I:
    mdl.addConstraint(pulp.lpSum(k * x[(i, k)] for k in K) == pulp.lpSum(x[(k, i)] for k in K),
                      name=f'rep-condition-{i}')

# set the objective function
mdl.setObjective(x[1, 1])  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
x_sol = {i: sum(k * x[i, k].value() for k in K) for i in I}
print(f'x = {x_sol}')
# endregion
