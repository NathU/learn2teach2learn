import numpy

class MyID3:
# USE: 
#	- Initialize MyID3 with the traing set.
#
	def __init__(self, training_data, feature_names = None):
		self.training_set = list(numpy.transpose(training_data))
		if feature_names == None:
			names = []
			feat_count = len(training_data[0]) - 1
			for i in range(feat_count):
				names.append("Feature " + str(i))
			self.feature_names = names
		else:
			self.feature_names = feature_names
		self.tree = self.build_tree(self.training_set, self.feature_names)
		
	
	def predict(self, data):
		feat_name = list(self.tree.keys())[0]
		predictions = []
		for row in data:
			feat_value = row[self.feature_names.index(feat_name)]
			subtree = self.tree[feat_name][feat_value]
			classification = self.find_leaf(row, subtree)
			temp = list(row)
			temp.append(classification)
			predictions.append(temp)
		
		return predictions

		
	def find_leaf(self, data, subtree):
		r = "Hi"
		if (isinstance(subtree, dict)):
			feat_name = list(subtree.keys())[0]
			feat_value = data[self.feature_names.index(feat_name)]
			r = self.find_leaf(data, subtree[feat_name][feat_value])
		else:
			r = subtree
		return r
	
	def print_tree(self, tree = None, tabs = 0):
		if tree == None:
			tree = self.tree
		for key in tree.keys():
			if not isinstance(tree[key], dict):
				print ('\t' * tabs + str(key) + " - " + str(tree[key]))
			else:
				print ('\t' * tabs + str(key))
				self.print_tree(tree[key], tabs + 1)

		
		
	def most_common_class(self, t_set):
		tallies = [1]
		counter = 0
		targets = t_set[-1]
		targets.sort()
		for i in range(1,len(targets)):
			if targets[i] != targets[i - 1]:
				tallies.append(0)
				counter += 1
			tallies[counter] += 1
		i_max = tallies.index(max(tallies))
		return list(set(targets))[i_max]


	#T_Set should be transposed
	def get_entropies(self, t_set):
		targets = {}
		entropies = []
		
		# EX: { c1 : 0, c2 : 0, c3 : 0 }
		for t in set(t_set[-1]):
			targets[t] = 0
		
		for row in t_set[0:-1]:
			feature_values = set(row)
			if None not in feature_values:
				counts = {}
				
				# EX: { Yes   : { c1 : 0, c2 : 0, c3 : 0 }, 
				#		No    : { c1 : 0, c2 : 0, c3 : 0 }, 
				#		Maybe : { c1 : 0, c2 : 0, c3 : 0 } }
				for val in feature_values:
					counts[val] = targets
				
				# tabulate classes for each value in this feature
				# EX:   No    : { c1 : 7, c2 : 4, c3 : 18 }
				for f,i in zip(row, range(len(row))):
					(counts[val])[t_set[-1][i]] += 1
				
				# collect class frequencies for each value in the feature,
				feature_entropies = []
				for val in counts:
					target_counts = []
					for t in counts[val]:
						target_counts.append((counts[val])[t])
					# calculate the weighted entropy of each value in the feature,
					total = sum(target_counts)
					feature_entropies.append(self.calc_entropy(target_counts, total))
				# collect the entropy of this feature
				entropies.append(sum(feature_entropies))
			
			# if this feature has already been used higher in the decision tree assign
			#	it a dummy entropy value of 2.
			else:
				entropies.append(2)
		
		return entropies
		
		
	def calc_entropy(self, value_list, total = 1):
		e = float(0)
		d = float(sum(value_list))
		for v in value_list:
			x = float(v)/d
			e -= x * numpy.log2(x)
		return float(e/total)
		

	def build_tree (self, t_set, name_list):

		# If all remaining features have just one class,
		if len(set(t_set[-1])) == 1:
			return list(set(t_set[-1]))[0] # a leaf
			
		# If all out of features, return most common class
		elif list(set(name_list))[0] == None:
			return self.most_common_class(t_set) # a leaf
			
		# else, build the tree
		else:
			# calc collective entropies of all features
			feature_entropies = self.get_entropies(t_set)
			
			# select the feature with the min entropy
			i_feature = feature_entropies.index(min(feature_entropies))
			
			# branch the data by values of the selected feature
			new_name_list = (name_list[0:i_feature] + [None] + name_list[i_feature+1 : ])
			new_data = {}
			feature_values = set(t_set[i_feature])
			for val in feature_values:
				new_data[val] = []
			for row in list(numpy.transpose(t_set)):
				part1 = list(row[0:i_feature])
				part2 = [None]
				part3 = list(row[i_feature+1 : ])
				new_row = part1 + part2 + part3
				(new_data[row[i_feature]]).append(new_row)
			
			# create a subtree, recure, and return
			feature_name = name_list[i_feature]
			subtree = {feature_name : {}}
			for key in new_data:
				temp = list(numpy.transpose(new_data[key]))
				(subtree[feature_name])[key] = self.build_tree(temp, new_name_list)
			
			return subtree
			
		
		
		
		
		
		
		
		
		
