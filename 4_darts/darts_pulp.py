"""
Solution to the Darts Puzzle.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Andrea Rujano (Aug 05 2021), MipMaster.org.
"""

import pulp

# Set of indices
players = [1, 2, 3]
shots = [1, 2, 3, 4, 5, 6]
points = [1, 2, 3, 5, 10, 20, 25, 50]
region_points = {1: 3, 2: 2, 3: 2, 5: 2, 10: 3, 20: 3, 25: 2, 50: 1}
grid_player_shots = [(i, j) for i in players for j in shots]
grid_shots_points = [(j, k) for j in shots for k in points]
keys = [(i, j, k) for i in players for j in shots for k in points]

# define the model
mdl = pulp.LpProblem('darts', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')

# Add constraints
for i in players:
    for j in shots:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in points) == 1, name=f'row_add_1_{i}_{j}')

for k, total in region_points.items():
    mdl.addConstraint(pulp.lpSum(x[i, j, k] for i, j in grid_player_shots) == total,
                      name=f'Cell-{(i, j)}-given-value-{k}')

for i in players:
    mdl.addConstraint(pulp.lpSum(k * x[i, j, k] for j, k in grid_shots_points) == 71, name=f'Cell-given-value-{i}')

mdl.addConstraint(x[1, 1, 20] == 1, name=f'first player_1')
mdl.addConstraint(x[1, 2, 2] == 1, name=f'first player_2')
# second player hits
mdl.addConstraint(x[2, 1, 3] == 1, name=f'second player')

# Set objective function
mdl.setObjective(x[3, 1, 1])

# Solve
mdl.solve()

# Retrieve the solution
x_sol = {key: val.value() for key, val in x.items() if val.value() > 0.5}
print(f'x={x_sol}')

