"""
Solution to the Continuous Line.

This version uses SCIP as a solver.

Created by Aster (Aug, 2021), MipMaster.org.
"""

from pyscipopt import Model, quicksum

# region Input Data
num_rows = 6
num_cols = 6
# holes
H = [(0, 2), (1, 4), (3, 2), (3, 3), (4, 0), (4, 3), (4, 5), (5, 0), (5, 5)]

num_digits = num_rows*num_cols-len(H)
# rows
I = [i for i in range(num_rows)]
# columns
J = [j for j in range(num_cols)]
# digits
K = [k for k in range(num_digits)]

# cells
C = [(i, j) for i in I for j in J if (i, j) not in H]

# keys for decision variables x
x_keys = [(i, j, k) for i, j in C for k in K]
# endregion

# region Define the model
mdl = Model('continuous_line')

# add variables
x = dict()
for key in x_keys:
    x[key] = mdl.addVar(vtype='B', name=f'x_{key}')

# add constraints
# exactly one digit gets assigned to every cell
for i, j in C:
    mdl.addCons(quicksum(x[i, j, k] for k in K) == 1, name=f'single_digit_{i}_{j}')
# every digit must be used exactly once
for k in K:
    mdl.addCons(quicksum(x[i, j, k] for i, j in C) == 1, name=f'all_digits{k}')
# every digit must have its consecutive in an adjacent cell
for i, j in C:
    for k in K[:num_digits-1]:  # skip the last digits
        mdl.addCons((x[i, j, k] <=
                     x.get((i+1, j, k+1), 0) + x.get((i-1, j, k+1), 0) +
                     x.get((i, j+1, k+1), 0) + x.get((i, j-1, k+1), 0)),
                    name=f'neighboring_{i}_{j}_{k}')

# set the objective function
mdl.setObjective(quicksum(x[key] for key in x_keys))  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
for i in I:
    row = [int(sum(k * mdl.getVal(x[i, j, k]) for k in K)) if (i, j) in C else 'X' for j in J]
    print(row)
# endregion

