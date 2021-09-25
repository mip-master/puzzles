"""
Solution to the Zebra

This version uses PuLP as a modeling language and CBC as a solver.

Created by Éder Pinheiro and Eric Zettermann  (Sep 9, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# House position
I = [1, 2, 3, 4, 5]
# Characteristics
J = ['country', 'color', 'pet', 'beverage', 'hobby']
# options
K = {'country': ['Brazil', 'Venezuela', 'India', 'Tunisia', 'Mexico'],
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
# exactly one digit gets assigned to every cell
for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for k in K[j]) == 1, name=f'single_digit_{i}_{j}')

# every digit must appear only once in a column
for j in J:
    for k in K[j]:
        mdl.addConstraint(pulp.lpSum(x[i, j, k] for i in I) == 1, name=f'once_in_column_{j}_{k}')

# R2
mdl.addConstraint(pulp.lpSum(i * x[i, 'country', 'Brazil'] for i in I) == pulp.lpSum(i * x[i, 'color', 'red']
                                                                                     for i in I), name=f'R2')

# R3
mdl.addConstraint(pulp.lpSum(i * x[i, 'country', 'Venezuela'] for i in I) == pulp.lpSum(i * x[i, 'pet', 'dog']
                                                                                        for i in I), name=f'R3')

# R4
mdl.addConstraint(pulp.lpSum(i * x[i, 'color', 'green'] for i in I) == pulp.lpSum(i * x[i, 'beverage', 'coffee']
                                                                                  for i in I), name=f'R4')
# R5
mdl.addConstraint(pulp.lpSum(i * x[i, 'country', 'India'] for i in I) == pulp.lpSum(i * x[i, 'beverage', 'tea']
                                                                                    for i in I), name=f'R5')

# R6
for i in I[1:4]:
    mdl.addConstraint(x[i, 'color', 'green'] <= x[i - 1, 'color', 'ivory'], name=f'R6_{i}')
mdl.addConstraint(x[1, 'color', 'green'] == 0, name=f'R6_{1}')
# R7
mdl.addConstraint(pulp.lpSum(i * x[i, 'pet', 'cat'] for i in I) == pulp.lpSum(i * x[i, 'hobby', 'chess']
                                                                              for i in I), name=f'R7')

# R8
mdl.addConstraint(pulp.lpSum(i * x[i, 'color', 'yellow'] for i in I) == pulp.lpSum(i * x[i, 'hobby', 'volleyball']
                                                                                   for i in I), name=f'R8')
# R9
mdl.addConstraint(x[3, 'beverage', 'milk'] == 1, name=f'R9')

# R10
mdl.addConstraint(x[1, 'country', 'Mexico'] == 1, name=f'R10')

# R11
for i in I[1:3]:
    mdl.addConstraint(x[i, 'hobby', 'sudoku'] <= x[i - 1, 'pet', 'turtle'] + x[i + 1, 'pet', 'turtle'],
                      name=f'R11_{i}')

mdl.addConstraint(x[1, 'hobby', 'sudoku'] <= x[2, 'pet', 'turtle'], name=f'R11_1')

mdl.addConstraint(x[5, 'hobby', 'sudoku'] <= x[4, 'pet', 'turtle'], name=f'R11_5')

# R12
for i in I[1:3]:
    mdl.addConstraint(x[i, 'hobby', 'volleyball'] <= x[i - 1, 'pet', 'hamster'] + x[i + 1, 'pet', 'hamster'],
                      name=f'R12_{i}')

mdl.addConstraint(x[1, 'hobby', 'volleyball'] <= x[2, 'pet', 'hamster'], name=f'R12_1')

mdl.addConstraint(x[5, 'hobby', 'volleyball'] <= x[4, 'pet', 'hamster'], name=f'R12_5')

# R13
mdl.addConstraint(pulp.lpSum(i * x[i, 'beverage', 'orange juice'] for i in I) == pulp.lpSum(i * x[i, 'hobby', 'karaoke']
                                                                                            for i in I), name=f'R13')

# R14
mdl.addConstraint(pulp.lpSum(i * x[i, 'country', 'Tunisia'] for i in I) == pulp.lpSum(i * x[i, 'hobby', 'fishing']
                                                                                      for i in I), name=f'R14')

# R15
for i in I[1:3]:
    mdl.addConstraint(x[i, 'country', 'Mexico'] <= x[i - 1, 'color', 'blue'] + x[i + 1, 'color', 'blue'],
                      name=f'R15_{i}')

mdl.addConstraint(x[1, 'country', 'Mexico'] <= x[2, 'color', 'blue'], name=f'R15_1')

mdl.addConstraint(x[5, 'country', 'Mexico'] <= x[4, 'color', 'blue'], name=f'R15_5')

# set the objective function
mdl.setObjective(pulp.lpSum(x[key] for key in x_keys))  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
sol = {(i, j, k): x[i, j, k].value() for i, j, k in x_keys if x[i, j, k].value() == 1}

print('position'.ljust(12), [j.ljust(12) for j in J])
for i in I:
    a = [k.ljust(12) for j in J for k in K[j] if (i, j, k) in sol]
    print(str(i).ljust(12), a)
# endregion
