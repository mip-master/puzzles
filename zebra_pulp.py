"""

This version uses PuLP as a modeling language and CBC as a solver.

"""

import pulp

# region Input Data
K = [1, 2, 3, 4, 5]  # house position
I = ['country', 'house_color', 'pet', 'beverage', 'cigarette_brand']
J = {'country': ['England', 'Spanish', 'Ukrainian', 'Japan', 'Norwege'],
     'house_color': ['Red', 'Green', 'Ivory', 'Yellow', 'Blue'],
     'pet': ['Dog', 'Snails', 'Fox', 'Horse', 'Zebra'],
     'beverage': ['Coffee', 'Tea', 'Milk', 'Orange juice', 'Water'],
     'cigarette_brand': ['Old gold', 'Kools', 'Chesterfields', 'Lucky strike', 'Parliaments']}

# region Define the model
mdl = pulp.LpProblem('zebra')

x_indexes = [(k, i, j) for k in K for i in I for j in J[i]]
x = pulp.LpVariable.dicts(indexs=x_indexes, cat=pulp.LpBinary, name='x')

# add constraints

for i in I:
    for j in J[i]:
        mdl.add(sum(x[k, i, j] for k in K) == 1, name=f'elements {i} fields {j}')

for k in K:
    for i in I:
        mdl.add(sum(x[k, i, j] for j in J[i]) == 1, name=f'position {k} elements {i}')

# R2
mdl.addConstraint(sum(k * x[k, 'country', 'England'] for k in K) == sum(k * x[k, 'house_color', 'Red'] for k in K))

# R3
mdl.addConstraint(sum(k * x[k, 'country', 'Spanish'] for k in K) == sum(k * x[k, 'pet', 'Dog'] for k in K))

# R4
mdl.addConstraint(sum(k * x[k, 'house_color', 'Green'] for k in K) == sum(k * x[k, 'beverage', 'Coffee'] for k in K))

# R5
mdl.addConstraint(sum(k * x[k, 'country', 'Ukrainian'] for k in K) == sum(k * x[k, 'beverage', 'Tea'] for k in K))

# R6
for k in K:
    if k - 1 in K:
        mdl.addConstraint(x[k - 1, 'house_color', 'Ivory'] == x[k, 'house_color', 'Green'])

# R7
mdl.addConstraint(sum(k * x[k, 'pet', 'Snails'] for k in K) == sum(k * x[k, 'cigarette_brand', 'Old gold'] for k in K))

# R8
mdl.addConstraint(sum(x[k, 'house_color', 'Yellow'] for k in K) == sum(x[k, 'cigarette_brand', 'Kools'] for k in K))

# R9
mdl.addConstraint(x[3, 'beverage', 'Milk'] == 1)

# R10
mdl.addConstraint(x[1, 'country', 'Norwege'] == 1)

# R11
mdl.addConstraint(
    sum(k * x[k, 'cigarette_brand', 'Chesterfields'] for k in K) - sum(k * x[k, 'pet', 'Fox'] for k in K) <= 2)
mdl.addConstraint(
    sum(k * x[k, 'cigarette_brand', 'Chesterfields'] for k in K) - sum(k * x[k, 'pet', 'Fox'] for k in K) >= -2)

# R12
mdl.addConstraint(sum(k * x[k, 'cigarette_brand', 'Kools'] for k in K) - sum(k * x[k, 'pet', 'Horse'] for k in K) <= 2)
mdl.addConstraint(sum(k * x[k, 'cigarette_brand', 'Kools'] for k in K) - sum(k * x[k, 'pet', 'Horse'] for k in K) >= -2)

# R13
mdl.addConstraint(
    sum(k * x[k, 'beverage', 'Orange juice'] for k in K) == sum(k * x[k, 'cigarette_brand', 'Lucky strike'] for k in K))

# R14
mdl.addConstraint(
    sum(k * x[k, 'country', 'Japan'] for k in K) == sum(k * x[k, 'cigarette_brand', 'Parliaments'] for k in K))

# R15
mdl.addConstraint(sum(k * x[k, 'country', 'Norwege'] for k in K) - sum(k * x[k, 'house_color', 'Blue'] for k in K) <= 2)
mdl.addConstraint(
    sum(k * x[k, 'country', 'Norwege'] for k in K) - sum(k * x[k, 'house_color', 'Blue'] for k in K) >= -2)

#
# # set the objective function
mdl.setObjective(sum(x[k, i, j] for k, i, j in x_indexes))

# # endregion
#
# # region Optimize and retrieve the solution
mdl.solve()

#

# # retrieve and print out the solution
sol = {(k, i, j): x[k, i, j].value() for k, i, j in x_indexes if x[k, i, j].value() == 1}

print('position', [i for i in I])
for k in K:
    a = [j for i in I for j in J[i] if (k, i, j) in sol]
    print(k, a)

# endregion
