"""
Solution to the Continuous Line.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Eric Zettermann (Jul 11, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# rows
I = {0, 1, 2, 3, 4, 5, 6}
I2 = {1, 2, 3, 4, 5}
# columns
J = {0, 1, 2, 3, 4, 5, 6}
J2 = {1, 2, 3, 4, 5}
# digits
K = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21}
K2 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21}
K3 = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
# holes and boundaries
H = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
     (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
     (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6),
     (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6),
     (1, 1), (2, 3), (2, 4), (4, 2)]

# keys for decision variables x
keys = [(i, j, k) for i in I for j in J for k in K]
keys2 = [(i, j, k) for i in I2 for j in J2 for k in K3]
# endregion

# region Define the model
mdl = pulp.LpProblem('continuous_line', sense=pulp.LpMaximize)

# add variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')

# add constraints
# one digit per cell
for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in K) == 1, name=f'1digit_{i}_{j}')
# digits can't repeat (except 0)
    for k in K2:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I2 for j in J2) == 1, name=f'no_digit_repetition_{k}')
# holes and boundaries are 0
for holes in H:
    mdl.addConstraint((x[i, j, 0] for (i, j) in holes) == 1, name=f'blocks_{H}')
# some neighbor has to be a consecutive
for (i, j, k) in keys2:
    mdl.addConstraint((x[i, j, k] <= x[i+1, j, k] + x[i-1, j, k] + x[i, j+1, k] + x[i, j-1, k] for (i, j, k) in keys2)
                      == 1, name=f'blocks_{H}')

# set the objective function
mdl.setObjective(x[1, 2, 1])  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
x_sol = {(i, j): sum(k * x[i, j, k].value() for k in K) for i in I2 for j in J2}
print(f'x = {x_sol}')
# endregion
