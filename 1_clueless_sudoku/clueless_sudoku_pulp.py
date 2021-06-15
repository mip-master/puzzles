"""
Solution to the Clueless Sudoku.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Aster Santana (Jun 15, 2021), MipMaster.org.
"""

import pulp

# Input Data
# rows
I = [1, 2, 3, 4, 5, 6]
# columns
J = [1, 2, 3, 4, 5, 6]
# numbers
K = [1, 2, 3, 4, 5, 6]
# regions
R = {1: [(1, 1), (1, 2), (1, 3), (2, 1)], 2: [(1, 4), (1, 5), (2, 5)], 3: [(1, 6), (2, 6)],
     4: [(2, 2), (2, 3)], 5: [(2, 4), (3, 4)], 6: [(3, 1), (4, 1)], 7: [(3, 2), (3, 3), (4, 3)],
     8: [(3, 5), (3, 6), (4, 5)], 9: [(5, 1), (5, 2), (4, 2)], 10: [(4, 4), (5, 4)],
     11: [(5, 5), (5, 6), (4, 6)], 12: [(6, 1), (6, 2)], 13: [(5, 3), (6, 3)], 14: [(6, 4), (6, 5), (6, 6)]}
# decision variable keys
keys = [(i, j, k) for i in I for j in J for k in K]

# Define the model
mdl = pulp.LpProblem('clueless_sudoku', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')
z = pulp.LpVariable(cat=pulp.LpInteger, name='z')

# Add Constraints
for i in I:
    for k in K:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for j in J) == 1, name=f'row_{i}_{k}')

for j in J:
    for k in K:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I) == 1, name=f'col_{j}_{k}')

for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in K) == 1, name=f'num_{i}_{j}')

for key, r in R.items():
    mdl.addConstraint(pulp.lpSum(k * x[i, j, k] for (i, j) in r for k in K) == z, name=f'regions_{key}')

# Set the objective function
mdl.setObjective(z)

# Optimize
mdl.solve()

# Retrieve the solution
x_sol = {key: int(val.value()) for key, val in x.items() if val.value() > 0.5}
print(f'x = {x_sol}')
print(f'z = {z.value()}')
