"""
Solution to the Nonogram puzzle.

This version uses SCIP as a solver.

Created by Aster Santana and Éder Pinheiro (Aug, 2021), MipMaster.org.
"""

from pyscipopt import Model, quicksum

# region Input Data
# positions
I = [1, 2, 3, 4, 5, 6, 7]  # origin
J = I  # destination
# pawns
L = ['L1', 'L2', 'L3']
R = ['R5', 'R6', 'R7']
K = L + R
# moves
T = list(range(24))
# keys for decision variables
x_keys = [(i, j, k, t) for i in I for j in J for k in L for t in T if i < j < i + 2]
x_keys += [(i, j, k, t) for i in I for j in J for k in R for t in T if i-2 < j < i]
# endregion

# region Define the model
mdl = Model('left-right')

# add variables
x = dict()
for key in x_keys:
    x[key] = mdl.addVar(vtype='B', name=f'x_{key}')

# add constraints
# initial and final position of left pawns
for k in L:
    mdl.addCons(quicksum(x.get((int(k[1]), j, k, t), 0) for j in J for t in T) == 1, name=f'init_left_{k}')
    mdl.addCons(quicksum(x.get((i, int(k[1])+4, k, t), 0) for i in I for t in T) == 1, name=f'end_left_{k}')
# initial and final position of right pawns
for k in R:
    mdl.addCons(quicksum(x.get((int(k[1]), j, k, t), 0) for j in J for t in T) == 1, name=f'init_right_{k}')
    mdl.addCons(quicksum(x.get((i, int(k[1])-4, k, t), 0) for i in I for t in T) == 1, name=f'end_right_{k}')
# flow balance
for h in I:
    for k in K:
        if h not in [int(k[1]), int(k[1])+4 if k[0] == 'L' else int(k[1])-4]:
            mdl.addCons(quicksum(x.get((i, h, k, t), 0) for i in I for t in T) ==
                        quicksum(x.get((h, j, k, t), 0) for j in J for t in T), name=f'fb_{h}_{k}')
# set the objective function
mdl.setObjective(quicksum(x[key] for key in x_keys))
# endregion

# region Optimize and retrieve the solution
mdl.optimize()

# retrieve and print out the solution
for t in T:
    for key in x_keys:
        if key[3] == t and mdl.getVal(x[key]) > 0.5:
            print(key)
# endregion
