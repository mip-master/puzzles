"""
Solution to the Continuous Line.

This version uses PuLP as a modeling language and CBC as a solver.

Created by Eric Zettermann (Sep 9, 2021), MipMaster.org.
"""

import pulp

# region Input Data
# rows
I = [i for i in range(1, 6)]
# columns
J = [j for j in range(1, 6)]
# options
K = [k for k in range(1, 6)]

options = {(1, 1): '  red   ', (1, 2): '  green ', (1, 3): '  yellow', (1, 4): '  blue  ', (1, 5): '  ivory ',
           (2, 1): 'england', (2, 2): 'spain  ', (2, 3): 'ukraine', (2, 4): 'norway ', (2, 5): 'japan  ',
           (3, 1): 'coffee      ', (3, 2): 'tea         ', (3, 3): 'milk        ', (3, 4): 'orange juice',
           (3, 5): 'water       ',
           (4, 1): 'dog   ', (4, 2): 'snails', (4, 3): 'fox   ', (4, 4): 'horse ', (4, 5): 'zebra ',
           (5, 1): 'old gold     ', (5, 2): 'kools        ', (5, 3): 'chesterfields', (5, 4): 'lucky strike ',
           (5, 5): 'parliaments  '
           }
# cells
C = [(i, j) for i in I for j in J]

# kickoff restrictions. (variables that we already know is 0)
R = [
    (5, 1, 5), (1, 1, 2),  # R6
    (3, 3, 1), (3, 3, 2), (3, 3, 4), (3, 3, 5),  # R9
    (1, 2, 1), (1, 2, 2), (1, 2, 3), (1, 2, 5),  # R10
    (2, 1, 1), (2, 1, 2), (2, 1, 3), (2, 1, 5),  # R15
]

# keys for decision variables x
x_keys = [(i, j, k) for i, j in C for k in K if (i, j, k) not in R]
# endregion

# region Define the model
mdl = pulp.LpProblem('zebra', sense=pulp.LpMaximize)

# add variables
x = pulp.LpVariable.dicts(indexs=x_keys, cat=pulp.LpBinary, name='x')

# add constraints
# exactly one digit gets assigned to every cell
for i in I:
    for j in J:
        mdl.addConstraint(pulp.lpSum(x.get((i, j, k), 0) for k in K) == 1, name=f'single_digit_{i}_{j}')

# every digit must appear only once in a column
for j in J:
    for k in K:
        mdl.addConstraint(pulp.lpSum(x.get((i, j, k), 0) for i in I) == 1, name=f'once_in_column_{j}_{k}')

# R2
mdl.addConstraint(pulp.lpSum(i * x.get((i, 2, 1), 0) for i in I) == pulp.lpSum(i * x.get((i, 1, 1), 0) for i in I),
                  name=f'R2')

# R3
mdl.addConstraint(pulp.lpSum(i * x.get((i, 2, 2), 0) for i in I) == pulp.lpSum(i * x.get((i, 4, 1), 0) for i in I),
                  name=f'R3')

# R4
mdl.addConstraint(pulp.lpSum(i * x.get((i, 3, 1), 0) for i in I) == pulp.lpSum(i * x.get((i, 1, 2), 0) for i in I),
                  name=f'R4')

# R5
mdl.addConstraint(pulp.lpSum(i * x.get((i, 2, 3), 0) for i in I) == pulp.lpSum(i * x.get((i, 3, 2), 0) for i in I),
                  name=f'R5')

# R6
mdl.addConstraint(
    pulp.lpSum(i * x.get((i, 1, 2), 0) for i in I) == pulp.lpSum((i + 1) * x.get((i, 1, 5), 0) for i in I),
    name=f'R6')

# R7
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 1), 0) for i in I) == pulp.lpSum(i * x.get((i, 4, 2), 0) for i in I),
                  name=f'R7')

# R8
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 2), 0) for i in I) == pulp.lpSum(i * x.get((i, 1, 3), 0) for i in I),
                  name=f'R8')

# R11
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 3), 0) for i in I) - pulp.lpSum(i * x.get((i, 4, 3), 0) for i in I) <= 2,
                  name=f'R11_up')
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 3), 0) for i in I) - pulp.lpSum(i * x.get((i, 4, 3), 0) for i in I) >= -2,
                  name=f'R11_down')

for i in I:
    mdl.addConstraint((1 - x.get((i, 5, 3), 0)) >= x.get((i, 4, 3), 0),
                      name=f'R11_difference1_{i}')

for i in I:
    mdl.addConstraint((1 - x.get((i, 4, 3), 0)) >= x.get((i, 5, 3), 0),
                      name=f'R11_difference2_{i}')

# R12
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 2), 0) for i in I) - pulp.lpSum(i * x.get((i, 4, 4), 0) for i in I) <= 2,
                  name=f'R12_up')
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 2), 0) for i in I) - pulp.lpSum(i * x.get((i, 4, 4), 0) for i in I) >= -2,
                  name=f'R12_down')

for i in I:
    mdl.addConstraint((1 - x.get((i, 5, 2), 0)) >= x.get((i, 4, 4), 0),
                      name=f'R12_difference1_{i}')

for i in I:
    mdl.addConstraint((1 - x.get((i, 4, 4), 0)) >= x.get((i, 5, 2), 0),
                      name=f'R12_difference2_{i}')

# R13
mdl.addConstraint(pulp.lpSum(i * x.get((i, 5, 4), 0) for i in I) == pulp.lpSum(i * x.get((i, 3, 4), 0) for i in I),
                  name=f'R13')

# R14
mdl.addConstraint(pulp.lpSum(i * x.get((i, 2, 5), 0) for i in I) == pulp.lpSum(i * x.get((i, 5, 5), 0) for i in I),
                  name=f'R14')

# set the objective function
mdl.setObjective(pulp.lpSum(x[key] for key in x_keys))  # not really required for this problem
# endregion

# region Optimize and retrieve the solution
mdl.solve()

# retrieve and print out the solution
Sol = {}
Ans = {}
for i in I:
    for j in J:
        Sol[(i, j)] = sum(k * x[i, j, k].value() for k in K if (i, j, k) not in R)
        Ans[(i, j)] = options[j, Sol[(i, j)]]
print(['n', 'color ', 'country', 'drink       ', 'pet   ', 'cigar        '])
for i in I:
    sol_i = [i, Ans[(i, 1)], Ans[(i, 2)], Ans[(i, 3)], Ans[(i, 4)], Ans[(i, 5)]]
    print(sol_i)
# endregion
