"""
Solution to the Nonogram puzzle.

This version uses PuLP-CBC as a solver.

Created by Aster Santana and Éder Pinheiro (Aug, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# row strings
RS = {
  1: {1: 4, 2: 1, 3: 2},
  2: {1: 3, 2: 1},
  3: {1: 1, 2: 3, 3: 2},
  4: {1: 1, 2: 1, 3: 1, 4: 2},
  5: {1: 1, 2: 1, 3: 1, 4: 1},
  6: {1: 1, 2: 1, 3: 1, 4: 1},
  7: {1: 1, 2: 1, 3: 1, 4: 4},
  8: {1: 1, 2: 3},
  9: {1: 1, 2: 4, 3: 2},
  10: {1: 2, 2: 2}
  }
# column strings
CS = {
  1: {1: 1, 2: 1, 3: 3},
  2: {1: 1, 2: 1, 3: 1},
  3: {1: 1, 2: 1, 3: 1},
  4: {1: 1, 2: 2, 3: 1},
  5: {1: 3, 2: 3},
  6: {1: 3, 2: 2, 3: 3},
  7: {1: 3, 2: 4},
  8: {1: 1, 2: 1},
  9: {1: 1, 2: 2, 3: 1, 4: 2},
  10: {1: 6, 2: 2}
  }
# rows
I = list(RS.keys())
# columns
J = list(CS.keys())
# keys for decision variables
x_keys = [(i, j) for i in I for j in J]
y_keys = [(i, j, k) for i in I for j in J for k in RS[i]]
z_keys = [(i, j, k) for i in I for j in J for k in CS[j]]
# endregion

# region Define the model
mdl = pulp.LpProblem('nonogram')

# add variables
# although there is a more compact way to set the variable in pulp (see previous puzzles), we use the for-loop here
# to show the similarity of using different mip modeling python framework (e.g, pulp and scip).
x, y, z = dict(), dict(), dict()
for key in x_keys:
    x[key] = pulp.LpVariable(cat=pulp.LpBinary, name=f'x_{key}')
for key in y_keys:
    y[key] = pulp.LpVariable(cat=pulp.LpBinary, name=f'y_{key}')
for key in z_keys:
    z[key] = pulp.LpVariable(cat=pulp.LpBinary, name=f'z_{key}')

# add constraints
# OBS: We could have combined the loops below to gain efficiency, but we kept them separated for clarity.
# each row string begins in exactly one column
for i in I:
    for k in RS[i]:
        mdl.addConstraint(pulp.lpSum(y[i, j, k] for j in J) == 1, name=f'str_row{i}_{k}')
# each column string begins in exactly one row
for j in J:
    for k in CS[j]:
        mdl.addConstraint(pulp.lpSum(z[i, j, k] for i in I) == 1, name=f'str_col{j}_{k}')
# row strings length
for i in I:
    for j in J:
        for k in RS[i]:
            for t in range(RS[i][k]):
                mdl.addConstraint(y[i, j, k] <= x.get((i, j+t), 0), name=f'row_len_{i}_{j}_{k}_{t}')
# column strings length
for i in I:
    for j in J:
        for k in CS[j]:
            for t in range(CS[j][k]):
                mdl.addConstraint(z[i, j, k] <= x.get((i+t, j), 0), name=f'col_len_{i}_{j}_{k}_{t}')
# row strings disjunction and precedence
for i in I:
    for j in J:
        for k in RS[i]:
            for jp in range(1, j + RS[i][k]+1):  # the +1 ensures disjunction, i.e., an empty cell between strings
                mdl.addConstraint(y.get((i, jp, k+1), 0) <= 1 - y[i, j, k], name=f'row_pre_{i}_{j}_{k}_{jp}')
# column strings disjunction and precedence
for i in I:
    for j in J:
        for k in CS[j]:
            for ip in range(1, i + CS[j][k]+1):  # the +1 ensures disjunction, i.e., an empty cell between strings
                mdl.addConstraint(z.get((ip, j, k+1), 0) <= 1 - z[i, j, k], name=f'col_pre_{i}_{j}_{k}_{ip}')
# set the objective function
mdl.setObjective(pulp.lpSum(x[key] for key in x_keys))
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
for i in I:
    row = [int(x[i, j].value()) for j in J]
    print(row)
# endregion
