# https://github.com/vuptran/graph-representation-learning.git
import numpy as np
from scipy.sparse import csr_matrix
import pickle
import random
from collections import defaultdict
import os 

"""
ind.dataset_str.x => the feature vectors of the training instances as scipy.sparse.csr.csr_matrix object;
ind.dataset_str.tx => the feature vectors of the test instances as scipy.sparse.csr.csr_matrix object;
-ind.dataset_str.allx => the feature vectors of both labeled and unlabeled training instances
	(a superset of ind.dataset_str.x) as scipy.sparse.csr.csr_matrix object;
ind.dataset_str.y => the one-hot labels of the labeled training instances as numpy.ndarray object;
ind.dataset_str.ty => the one-hot labels of the test instances as numpy.ndarray object;
-ind.dataset_str.ally => the labels for instances in ind.dataset_str.allx as numpy.ndarray object;
ind.dataset_str.graph => a dict in the format {index: [index_of_neighbor_nodes]} as collections.defaultdict
	object;
ind.dataset_str.test.index => the indices of test instances in graph, for the inductive setting as list object.
"""

path = '../data/'
x = []
y = []
test_index = []
test_mask = []
train_labeled_mask = []

labeled_index = []
labeled_mask = []
graph = defaultdict(list)

h = 0
n = 0

with open(os.path.join(path,'users_hate_all.content')) as content_f:
	for line in content_f:
		line = line.split()
		x.append([float(i) for i in line[1:-1]])
		labeled_mask.append(line[-1] != 'other')
		if line[-1] != 'other':
			labeled_index.append(int(line[0]))
		if line[-1] != 'other' and random.random() < 0.2:
			test_index.append(len(labeled_index))
			test_mask.append(True)
			train_labeled_mask.append(False)
		# if line[-1] == 'hateful' and h < 200:
		# 	#test_index.append(int(line[0]))
		# 	test_index.append(len(labeled_index))
		# 	test_mask.append(True)
		# 	train_labeled_mask.append(False)
		# 	h += 1
		# elif line[-1] == 'normal' and n < 600:
		# 	#test_index.append(int(line[0]))
		# 	test_index.append(len(labeled_index))
		# 	test_mask.append(True)
		# 	train_labeled_mask.append(False)
		# 	n+= 1
		else:
			test_mask.append(False)
			train_labeled_mask.append(line[-1] != 'other')
		label = 1 if line[-1] == 'hateful' else 0
		#label = [1,0] if line[-1] == 'hateful' else [0,1]
		y.append(label)

with open(os.path.join(path,'users.edges')) as edges_f:
	for line in edges_f:
		s, e = line.split()
		## fully-supervised
		# if not (labeled_mask[int(s)] and labeled_mask[int(e)]):
		# 	continue
		new_s = sum(labeled_mask[:int(s)])
		new_e = sum(labeled_mask[:int(e)])
		graph[new_s].append(new_e)

x = np.array(x)
y = np.array(y)
test_index = np.array(test_index, dtype=np.int32)
test_mask = np.array(test_mask)
train_labeled_mask = np.array(train_labeled_mask)
labeled_index = np.array(labeled_index)
labeled_mask = np.array(labeled_mask)

#semi-supervised
all_x = x[~test_mask]
all_y = y[~test_mask]
#fully-supervised
# all_x = x[labeled_mask]
# all_y = y[labeled_mask]
test_x = x[test_mask]
test_y = y[test_mask]
train_x = x[train_labeled_mask]
train_y = y[train_labeled_mask]
print("size:{} {} {}".format(len(all_x), len(test_x),len(train_x)))
#assert(len(all_x) + len(test_x) == 100386)

all_x_f = open(os.path.join(path,'ind.hateful.allx'), 'w')
pickle.dump(all_x, all_x_f)
all_x_f.close()
all_y_f = open(os.path.join(path,'ind.hateful.ally'), 'w')
pickle.dump(all_y, all_y_f)
all_y_f.close()

graph_f = open(os.path.join(path,'ind.hateful.graph'), 'w')
pickle.dump(graph, graph_f)
graph_f.close()

test_index_f = open(os.path.join(path,'ind.hateful.test.index'), 'wb')
#np.savetxt("ind.hateful.test.index'", test_index, newline="\n")
test_index_f.write('\n'.join(map(str, test_index)))
#pickle.dump(test_index, test_index_f)
test_index_f.close()

test_x_f = open(os.path.join(path,'ind.hateful.tx'), 'wb')
pickle.dump(test_x, test_x_f)
test_x_f.close()
test_y_f = open(os.path.join(path,'ind.hateful.ty'), 'wb')
pickle.dump(test_y, test_y_f)
test_y_f.close()
train_x_f = open(os.path.join(path,'ind.hateful.x'), 'wb')
pickle.dump(train_x, train_x_f)
train_x_f.close()
train_y_f = open(os.path.join(path,'ind.hateful.y'), 'wb')
pickle.dump(train_y, train_y_f)
train_y_f.close()

