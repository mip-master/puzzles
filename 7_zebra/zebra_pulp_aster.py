"""
Solution to the Zebra puzzle.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Éder Pinheiro and Eric Zettermann  (Sep 9, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# house positions
I = [1, 2, 3, 4, 5]
# attributes
J = ['flag', 'color', 'pet', 'beverage', 'hobby']
# options
K = {'flag': ['Brazil', 'Venezuela', 'India', 'Tunisia', 'Mexico'],
     'color': ['red', 'green', 'ivory', 'yellow', 'blue'],
     'pet': ['dog', 'cat', 'turtle', 'hamster', 'rabbit'],
     'beverage': ['coffee', 'tea', 'milk', 'orange juice', 'water'],
     'hobby': ['chess', 'volleyball', 'sudoku', 'karaoke', 'fishing']}

# keys for decision variables x
x_keys = [(i, j, k) for i in I for j in J for k in K[j]]
# endregion

# region Define the model
mdl = pulp.LpProblem('zebra', sense=pulp.LpMaximize)

# add variables
x = pulp.LpVariable.dicts(indexs=x_keys, cat=pulp.LpBinary, name='x')

# add constraints
# exactly one option for each house-attribute pair
for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in K[j]) == 1, name=f'single_option_{i}_{j}')
# exactly one house for each attribute-option pair
for j in J:
    for k in K[j]:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I) == 1, name=f'single_house_{j}_{k}')
# R2
for i in I:
    mdl.addConstraint(x[i, 'flag', 'Brazil'] == x[i, 'color', 'red'], name=f'R2_{i}')
# R3
for i in I:
    mdl.addConstraint(x[i, 'flag', 'Venezuela'] == x[i, 'pet', 'dog'], name=f'R3_{i}')
# R4
for i in I:
    mdl.addConstraint(x[i, 'color', 'green'] == x[i, 'beverage', 'coffee'], name=f'R4_{i}')
# R5
for i in I:
    mdl.addConstraint(x[i, 'flag', 'India'] == x[i, 'beverage', 'tea'], name=f'R5_{i}')
# R6
for i in I:  # using the get function because x[i-1, '*', '*'] is not defined for i=1
    mdl.addConstraint(x[i, 'color', 'green'] <= x.get((i-1, 'color', 'ivory'), 0), name=f'R6_{i}')
# R7
for i in I:
    mdl.addConstraint(x[i, 'pet', 'cat'] == x[i, 'hobby', 'chess'], name=f'R7_{i}')
# R8
for i in I:
    mdl.addConstraint(x[i, 'color', 'yellow'] == x[i, 'hobby', 'volleyball'], name=f'R8_{i}')
# R9
mdl.addConstraint(x[3, 'beverage', 'milk'] == 1, name='R9')
# R10
mdl.addConstraint(x[1, 'flag', 'Mexico'] == 1, name='R10')
# R11
for i in I:
    mdl.addConstraint(x[i, 'hobby', 'sudoku'] <= x.get((i-1, 'pet', 'turtle'), 0) + x.get((i+1, 'pet', 'turtle'), 0),
                      name=f'R11_{i}')
# R12
for i in I:
    mdl.addConstraint(x[i, 'hobby', 'volleyball'] <= x.get((i-1, 'pet', 'hamster'), 0) +
                      x.get((i+1, 'pet', 'hamster'), 0), name=f'R12_{i}')
# R13
for i in I:
    mdl.addConstraint(x[i, 'beverage', 'orange juice'] == x[i, 'hobby', 'karaoke'], name=f'R13_{i}')
# R14
for i in I:
    mdl.addConstraint(x[i, 'flag', 'Tunisia'] == x[i, 'hobby', 'fishing'], name=f'R14_{i}')
# R15
for i in I:
    mdl.addConstraint(x[i, 'flag', 'Mexico'] <= x.get((i-1, 'color', 'blue'), 0) + x.get((i+1, 'color', 'blue'), 0),
                      name=f'R15_{i}')

# set the objective function
mdl.setObjective(pulp.lpSum(x[key] for key in x_keys))  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
sol = {(i, j, k): x[i, j, k].value() for i, j, k in x_keys if x[i, j, k].value() >= 0.5}

print('position'.ljust(12), [j.ljust(12) for j in J])
for i in I:
    a = [k.ljust(12) for j in J for k in K[j] if (i, j, k) in sol]
    print(str(i).ljust(12), a)
# endregion
