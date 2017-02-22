import random		
import math
import numpy		


class NeuroNet:
	# Blueprint:
	# IE, [4, 2, 3] means input layer has 4 "nodes", 
	#	hidden layer has 2, and output layer has 3
	
	# Self.Layers:
	# IE, [[0 0 0 0 -1],	- input layer
	#		[0 0 -1],		- hidden layer
	#		[0 0 0]]		- output layer
	
	# Self.Weights:
	# IE, [ [None None None None],	- weights into input layer
	#		 [1 2 3 4 5 6 7 8],   	- weights into hidden layer
	#		   [1 2 3 4 5 6]  ]		- weights into output layer

	def __init__(self, blueprint, learnRate = 0.1):
		self.blueprint = blueprint
		self.layers = []
		self.weights = []
		self.learnRate = learnRate
		self.training_accuracy = -1

		for nodes, i in zip(blueprint, range(len(blueprint))):
			tempLayer = []
			weight_values = []
			
			if i == 0:
				for w in range(nodes):
					weight_values.append(None) # just a placeholder...
			else: # generate weight values
				weight_range = math.ceil(nodes * (blueprint[i - 1] + 1) / 2) # + 1 for bias node
				weight_values = list(range(-weight_range, weight_range+1)) # ex: [-4 -3 -2 -1 0 1 2 3 4]
				weight_values.remove(0)
				weight_values = list(map(lambda w: w / (10**(math.ceil((0.1+weight_range)/10))), weight_values)) # make all weights -1 < w < 1
				random.shuffle(weight_values)
				weight_values = weight_values[0:nodes * (1 + blueprint[i - 1])] # trim off extras due to odd # of connections
			
			for n in range(nodes): 
				tempLayer.append(0)
			
			if i < (len(blueprint) - 1):
				tempLayer.append(-1) # add the bias node
			
			self.layers.append(tempLayer)		# the layer...
			self.weights.append(weight_values)	# and the weights that feed into it.

			

			
	def print_network(self, reverse = False):
		if reverse:
			self.layers.reverse()
			self.weights.reverse()
		print("--------------------------------------------------------------------------------")
		for i in range(len(self.layers)):
			print("\tW"+str(i)+" - "+str(self.weights[i]))
			print("\tL"+str(i)+" - "+str(self.layers[i]))
		print("--------------------------------------------------------------------------------")
		if reverse:
			self.layers.reverse()
			self.weights.reverse()

			
		
	
	def feed_forward(self, row):
		for layer in range(len(self.layers)):
			if layer == 0:
				self.layers[0] = row		# inputs
				self.layers[0].append(-1)	# bias
			elif layer > 0:
				temp_layer = []
				for node in range(self.blueprint[layer]):
					temp_layer.append(0)
				
				for wt, i in zip(self.weights[layer], range(len(self.weights[layer]))):
					i_dest = i % (self.blueprint[layer])
					i_input = math.floor(i / (self.blueprint[layer]))
					h = wt * (self.layers[layer-1][i_input])
					temp_layer[i_dest] += h
				temp_layer = list(map(lambda h_val: 1/(1 + numpy.exp(-h_val)), temp_layer))
				
				if layer < (len(self.blueprint)-1):
					temp_layer.append(-1)
				
				self.layers[layer] = temp_layer
		

	
	
	def predict(self, test_set):
		predictions = []
		for row in test_set:
			self.feed_forward(row)
			classification = self.layers[-1].index(max(self.layers[-1]))
			temp = row[0:-1] + [classification]
			predictions.append(temp)
		return predictions

		
		
	
	def train(self, training_set):
		# Constraint! - training_set must contain at least one instance of each class, & targets must be Numeric!
		targets = list(set(list(map(lambda row: row[-1], training_set))))
		# also, |targets| must == |output layer|
		if len(targets) != self.blueprint[-1]:
			return False
		
		correct_count = 0
		# main learning loop
		for t_row in training_set:
			self.feed_forward(t_row[0:-1])
			
			# determine accuracy
			result = self.layers[-1].index(max(self.layers[-1]))
			should_be = t_row[-1]
			if result == should_be:
				correct_count += 1

			# determine output layer's targets
			i_target_err = targets.index(should_be)
			output_targets = []
			for i in range(len(targets)):
				if i == i_target_err:
					output_targets.append(1)
				else:
					output_targets.append(0)
			
			# just to help me think...
			self.layers.reverse()
			self.weights.reverse()
			
			
			# Calc Errors
			errors = []
			for layer in range(len(self.layers)-1): # exclude input layer
				layer_err = []
				
				# errors for output layer
				if layer == 0:
					for a, t in zip(self.layers[0], output_targets):
						layer_err.append(a * (1 - a) * (a - float(t)))
					
				# errors for hidden layers
				else:
					SOPs = []
					for a in self.layers[layer]:
						SOPs.append(0)
					
					kLayer_nodeCount = len(errors[layer-1])
				
					for w, i in zip(self.weights[layer-1], range(len(self.weights[layer-1]))):
						k_err = errors[layer-1][((i+1)%kLayer_nodeCount)-1]
						i_jNode = math.floor(i/kLayer_nodeCount)
						SOPs[i_jNode] += w * k_err
				
					temp = []
					for a, sop in zip(self.layers[layer], SOPs):
						temp.append(a * (1 - a) * sop)
					
					layer_err = temp[0:-1] # exclude bias node. This is CRUCIAL.
					
				errors.append(layer_err)
			
			
			# Update Weights
			for i in range(len(self.weights)-1): # exclude input layer placeholder "weights"
				for wt, j in zip(self.weights[i], range(len(self.weights[i]))):
					i_input = math.floor(j/len(errors[i]))
					i_dest = ((j+1)%(len(errors[i]))) - 1
					input_val = self.layers[i+1][i_input]
					dest_err = errors[i][i_dest]
					new_weight = wt - (self.learnRate * dest_err * input_val)
					self.weights[i][j] = new_weight
		
			# re-orient ourselves...
			self.layers.reverse()
			self.weights.reverse()
			# errors[] falls out of scope and we start again.

		
		self.training_accuracy = correct_count / len(training_set) * 100
		return True





