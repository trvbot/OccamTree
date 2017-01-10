import pandas as pd
import numpy as np
import networkx as nx
import matplotlib as plt

## this code takes in five variables of variable bins

# file = raw_input('Date File Name:\n')
file = 'PijPyeCnr.csv'

data = pd.read_csv(file, sep=',')
data = data.set_index(np.arange(1, len(data.index)+1))
variable_names = ['Pij', 'Pye', 'Cnr']

n_total_states = len(data.index)
n_total_variables = 3

state_list = data.iloc[:, 0:3].astype(str)
state_list['combo'] = state_list[variable_names].apply(lambda x: ''.join(x), axis=1)
state_list = np.asarray(state_list['combo'])

param = data[['Odds', 'P']]
param = param.set_index(state_list)

adj = pd.read_csv('3variable_adjacency.csv', sep=',', names=state_list)
adj = adj.set_index(state_list)

# class Var:
#     def __init__(self, name):
#         name = name
#         n_states = 0
#         states = []
#
#     def set_states(self, state_list):
#         states = list(state_list)

# joint = pd.DataFrame(np.zeros((1, 3)))
joint = pd.DataFrame(np.zeros((n_total_states*2, 3)), columns=[['1', '2', '3']], dtype=str)
num_joint = 0
joint_list = pd.Series(np.zeros(n_total_states*2), dtype=str)

# to find second-order relationships
for i in range(n_total_states-1):
    for j in range(i+1, n_total_states):
        # if they have nth-order relationship
        if adj.iloc[j, i] == 1:
            # if they have comparable parameter values
            if param.Odds.iloc[i] == param.Odds.iloc[j]:
                num_joint += 2
                print('1 :', (j, i))
                print(state_list[j], state_list[i])
                for k in range(n_total_variables):
                    # if the kth variable in the states is equal
                    if state_list[i][k] == state_list[j][k]:
                        joint.iloc[num_joint-2, k] = str(state_list[i][k])
                        joint.iloc[num_joint-1, k] = str(state_list[i][k])
                    else:
                        joint.iloc[num_joint-2, k] = 'x'
                        joint.iloc[num_joint-1, k] = 'x'
                    joint_list.iloc[num_joint-2] = str(state_list[i])
                    joint_list.iloc[num_joint-1] = str(state_list[j])
                print('yey')

# create joint set
joint['joined'] = joint_list
joint['joint'] = joint[['1', '2', '3']].apply(lambda x: ''.join(x), axis=1)
second_order_joint = joint[['joint', 'joined']]

# trim the extra space out of the array
for i in range(len(joint_list)):
    if joint_list.iloc[i] == 0:
        joint_list = joint_list[:i]
        second_order_joint = second_order_joint[:i]
        break


# to find first-order relationships
for i in range(n_total_states-1):
    for j in range(i+1, n_total_states):
        if adj.iloc[j, i] == 2:
            if param.Odds.iloc[i] == param.Odds.iloc[j]:
                print('2 :', (j, i))
                print(state_list[j], state_list[i])

# to find zeroth-order relationships
for i in range(n_total_states-1):
    for j in range(i+1, n_total_states):
        if adj.iloc[j, i] == 3:
            if param.Odds.iloc[i] == param.Odds.iloc[j]:
                print('3 :', (j, i))
                print(state_list[j], state_list[i])

print('\n')
print(param)
print('\n')
print(adj)


# to find the first branching point
# aka, the variable that is constant between all lowest-order states

# maybe I should be using set operations a la np.intersect1d() or np.setdiff1d()

# find unique joined states
# again, check for overlap, choose min __

# do I have to find which ones are duplicates first?
# both can't be added to the full state list probably
# make decision first and then create final state_list?

# second_order_joint will be trimmed when the decision is made
# then this step occurs
joined_items = np.unique(second_order_joint.joined)

for i in range(len(joined_items)):
    state_list = state_list[(state_list != joined_items[i])]

# create final state_list, aka leaves
state_list = np.append(state_list, np.unique(second_order_joint.joint))

