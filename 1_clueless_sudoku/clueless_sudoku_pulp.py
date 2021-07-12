"""
Solution to the Clueless Sudoku.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Aster Santana (Jun 15, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# rows
I = {1, 2, 3, 4, 5, 6}
# columns
J = {1, 2, 3, 4, 5, 6}
# digits
K = {1, 2, 3, 4, 5, 6}
# blocks
B = {1: [(1, 1), (1, 2), (1, 3), (2, 1)], 2: [(1, 4), (1, 5), (2, 5)], 3: [(1, 6), (2, 6)],
     4: [(2, 2), (2, 3)], 5: [(2, 4), (3, 4)], 6: [(3, 1), (4, 1)], 7: [(3, 2), (3, 3), (4, 3)],
     8: [(3, 5), (3, 6), (4, 5)], 9: [(5, 1), (5, 2), (4, 2)], 10: [(4, 4), (5, 4)],
     11: [(5, 5), (5, 6), (4, 6)], 12: [(6, 1), (6, 2)], 13: [(5, 3), (6, 3)], 14: [(6, 4), (6, 5), (6, 6)]}
# keys for decision variables x
keys = [(i, j, k) for i in I for j in J for k in K]
# endregion

# region Define the model
mdl = pulp.LpProblem('clueless_sudoku', sense=pulp.LpMaximize)

# add variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')
z = pulp.LpVariable(cat=pulp.LpContinuous, name='z')  # sum of digits in every block

# add constraints
# digits can't repeat in any row
for i in I:
    for k in K:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for j in J) == 1, name=f'row_{i}_{k}')
# digits can't repeat in any column
for j in J:
    for k in K:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I) == 1, name=f'col_{j}_{k}')
# exactly one digit is assigned to each cell
for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in K) == 1, name=f'digit_{i}_{j}')
# sum of digits in every block must be z
for key, block in B.items():
    mdl.addConstraint(pulp.lpSum(k * x[i, j, k] for (i, j) in block for k in K) == z, name=f'blocks_{key}')

# set the objective function
mdl.setObjective(z)  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
x_sol = {key: int(val.value()) for key, val in x.items() if val.value() > 0.5}
print(f'sum = {z.value()}')
for i in I:
    print([int(sum(k * x[i, j, k].value() for k in K)) for j in J])
# endregion
