import pandas as pd
import numpy as np
import networkx as nx
import matplotlib as plt

# accepts models of 4 variables with variable bins

class var_set:
    def __init__(self):
        self.n_variables = 0
        self.n_states = 0
        self.n_bins = []
        self.state_list = []
        self.param = []
        self.adj = []

    def load(self, file, variable_names):
        data = pd.read_csv(file, sep=',')
        data = data.set_index(np.arange(1, len(data.index)+1))

        self.n_states = int(len(data.index))
        self.n_variables = int(len(data.columns)-3)
        self.n_bins = np.zeros(self.n_variables)

        for i in range(self.n_variables):
            self.n_bins[i] = int(len(data.iloc[:, i].unique()))

        self.state_list = data.iloc[:, 0:4].astype(str)
        self.state_list['combo'] = self.state_list[variable_names].apply(lambda x: ''.join(x), axis=1)
        self.state_list = np.asarray(self.state_list['combo'])

        self.param = data[['Odds', 'P', 'Frequency']]
        self.param = self.param.set_index(self.state_list)

    def  create_adj(self):
        adj = pd.DataFrame(np.zeros((len(self.state_list), len(self.state_list))), index=self.state_list, columns=self.state_list)
        for i in range(len(self.state_list)):
            for j in range(len(self.state_list)):
                adj.iloc[j, i] = sum ( self.state_list[i][k] != self.state_list[j][k] for k in range(self.n_variables) )
        self.adj = adj

    def trim_freq(self):
        freq = self.param.Frequency
        crit = np.std(freq)/8.0
        freq = freq[(freq > crit)]
        self.param.Frequency = freq
        # create mask for param
        self.param = self.param.dropna()
        state_list = pd.DataFrame(self.state_list)
        # state_list = state_list[state_list.isin((param.index))].dropna()
        state_list = freq.index
        # create a mask for the original
        # otherwise, messes up adj lookup
        # preserve indices
        self.state_list = state_list.mask()
        self.n_states = len(self.state_list)
        # should also update self.n_bins

    def find_joint(self, N, thresh):
        joint = pd.DataFrame(np.zeros((self.n_states*3, self.n_variables)), columns=np.arange(1, self.n_variables+1), dtype=str)
        num_joint = 0
        joint_list = pd.Series(np.zeros(self.n_states*3), dtype=str)
        adj = pd.DataFrame(self.adj)
        param = pd.DataFrame(self.param)
        state_list = self.state_list
        n_variables = self.n_variables
        n_states = self.n_states

        for i in range(n_states-1):
            for j in range(i+1, n_states):
                # if they have nth-order relationship
                if adj.iloc[j, i] == N:
                    # if they have comparable parameter values
                    if (param.Odds.iloc[j]-thresh) < param.Odds.iloc[i] < (param.Odds.iloc[j]+thresh):
                        num_joint += 2
                        print(N, (j, i))
                        print(state_list[j], state_list[i])
                        print(param.Odds.iloc[i], param.Odds.iloc[j])
                        for k in range(n_variables):
                            # if the kth variable in the states is equal
                            if state_list[i][k] == state_list[j][k]:
                                joint.iloc[num_joint-2, k] = str(state_list[i][k])
                                joint.iloc[num_joint-1, k] = str(state_list[i][k])
                            else:
                                joint.iloc[num_joint-2, k] = 'x'
                                joint.iloc[num_joint-1, k] = 'x'
                            joint_list.iloc[num_joint-2] = str(state_list[i])
                            joint_list.iloc[num_joint-1] = str(state_list[j])

        joint['joined'] = joint_list
        joint['joint'] = joint[np.arange(1, n_variables+1)].apply(lambda x: ''.join(x), axis=1)
        new_joint = joint[['joint', 'joined']]

        # trim the extra space out of the array
        for i in range(len(joint_list)):
            if joint_list.iloc[i] == 0:
                joint_list = joint_list[:i]
                new_joint = new_joint[:i]
                break

        return new_joint

fourvar = var_set()
vars = ['Ageb', 'Nrb', 'Rku', 'Rro']
fourvar.load('AgebNrbRkuRro.csv', vars)
fourvar.create_adj()
fourvar.trim_freq()
third_order_joint = fourvar.find_joint(1, (np.std(fourvar.param.Odds)/4.0))
# second_order_joint = fourvar.find_joint(2, (np.std(fourvar.param.Odds)/4.0))
# first_order_joint = fourvar.find_joint(3, (np.std(fourvar.param.Odds)/4.0))
# zero_order_joint = fourvar.find_joint(4, (np.std(fourvar.param.Odds)/4.0))

joined_items = np.unique(third_order_joint.joined)

# add in all leaves that weren't reduced
# for i in range(len(joined_items)):
#     state_list = fourvar.state_list[(fourvar.state_list != joined_items[i])]
state_list = pd.DataFrame(fourvar.state_list)
state_list = state_list[~(state_list.isin(joined_items))].dropna()

# create final state_list, aka leaves
# state_list = pd.Series(np.append(fourvar.state_list, np.unique(third_order_joint.joint)))
state_list = pd.Series(np.append(state_list, np.unique(third_order_joint.joint)))

# then find the first branching point
# aka, the variable that is constant between all lowest-order states

# maybe I should be using set operations a la np.intersect1d() or np.setdiff1d()

reduced_states = np.zeros(len(vars), dtype=object)
states = np.zeros((len(state_list), len(vars)), dtype=str)
for i in range(len(vars)):
    for j in range(len(state_list)):
        states[j, i] = state_list[j][i]
    reduced_states[i] = np.unique(states[:, i])
print(reduced_states)
