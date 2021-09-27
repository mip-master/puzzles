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
H = [(1, 3), (2, 5), (4, 3), (4, 4), (5, 1), (5, 4), (5, 6), (6, 1), (6, 6)]

num_digits = num_rows*num_cols-len(H)
# rows
I = [i for i in range(1, num_rows+1)]
# columns
J = [j for j in range(1, num_cols+1)]

# cells
C = [(i, j) for i in I for j in J if (i, j) not in H]

# keys for decision variables x
x_keys = list()
for i, j in C:
    if j > 1:
        if (i, j-1) not in H:
            x_keys.append(((i, j), (i, j-1)))
    if j < num_cols:
        if (i, j+1) not in H:
            x_keys.append(((i, j), (i, j+1)))
    if i > 1:
        if (i-1, j) not in H:
            x_keys.append(((i, j), (i-1, j)))
    if i < num_rows:
        if (i+1, j) not in H:
            x_keys.append(((i, j), (i+1, j)))
dummy = (0, 0)
x_keys = [(dummy, (i, j)) for i, j in C] + x_keys
x_keys = x_keys + [((i, j), dummy) for i, j in C]
C.append(dummy)
# endregion

# region Define the model
mdl = Model('continuous_line')

# add variables
x = dict()
for key in x_keys:
    x[key] = mdl.addVar(vtype='B', name=f'x_{key}')
u = dict()
for i in C:
    u[i] = mdl.addVar(vtype='I', ub=27, name=f'u_{i}')
# add constraints
# exactly one origin
for i in C:
    mdl.addCons(quicksum(x[i, j] for i_, j in x_keys if i_ == i) == 1, name=f'single_origin_{i}')
# exactly one destination
for j in C:
    mdl.addCons(quicksum(x[i, j] for i, j_ in x_keys if j_ == j) == 1, name=f'single_dest_{j}')
# sequence
for i, j in x_keys:
    if i != dummy and j != dummy:
        mdl.addCons(u[i] - u[j] + 1 <= (num_digits+1) * (1 - x[i, j]), name=f'seq_{i}_{j}')
# set the objective function
mdl.setObjective(quicksum(x[i, j] for i, j in x_keys))  # not required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
u_sol = {(i, j): int(round(mdl.getVal(u[i, j]))) for (i, j) in C if (i, j) != dummy}
for i in I:
    row = [u_sol[i, j] if (i, j) in u_sol else 'X' for j in J]
    print(row)
# endregion

