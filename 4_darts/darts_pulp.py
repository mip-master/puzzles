"""
Solution to the Darts Puzzle.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Andrea Rujano (Aug 05 2021), MipMaster.org.
"""

import pulp

# region Input Data
# players
I = [1, 2, 3]  # {1: 'Andrea', 2: 'Antonio', 3: 'Luiz'}
# shots
J = [1, 2, 3, 4, 5, 6]
# scores
K = [1, 2, 3, 5, 10, 20, 25, 50]
# number of marks in each scoring regions
R = {1: 3, 2: 2, 3: 2, 5: 2, 10: 3, 20: 3, 25: 2, 50: 1}
# keys for decision variables x
keys = [(i, j, k) for i in I for j in J for k in K]
# endregion

# region Define the model
mdl = pulp.LpProblem('darts', sense=pulp.LpMaximize)

# Add variables
x = pulp.LpVariable.dicts(indexs=keys, cat=pulp.LpBinary, name='x')

# add constraints
# every shot hits one, and only one, scoring region
for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in K) == 1, name=f'shot_{i}_{j}')
# every player scored 71
for i in I:
    mdl.addConstraint(pulp.lpSum(k * x[i, j, k] for j in J for k in K) == 71, name=f'total_score-{i}')
# number of marks in each scoring region
for k, marks in R.items():
    mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I for j in J) == marks, name=f'score_marks_{k}')
# Andrea's first two shots scored 22 points
mdl.addConstraint(pulp.lpSum(k * x[1, j, k] for j in [1, 2] for k in K) == 22, name=f'andrea_22')
# Antonio's first shot scored 3 points
mdl.addConstraint(x[2, 1, 3] == 1, name=f'antonio_3')

# set the objective function
mdl.setObjective(pulp.lpSum(x))  # dummy objective because this is just a feasibility problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
print('Scores:')
for i in I:
    print(f'player {i}:', [sum(k*x[i, j, k].value() for k in K) for j in J])
# endregion
