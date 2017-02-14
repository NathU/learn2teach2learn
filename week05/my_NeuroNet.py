import random		
import math
import numpy		



class NeuroNet:
	# Layers:
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

	def __init__(self, layers, learnRate = None):
		self.blueprint = layers
		self.layers = []
		self.weights = []
		self.learnRate = 0.1 if learnRate is None else learnRate

		for nodes, i in zip(layers, range(len(layers))):
			tempLayer = []
			weight_values = []
			
			if i == 0:
				for w in range(nodes):
					weight_values.append(None)
			else: # generate weight values
				weight_range = math.ceil(nodes * (layers[i - 1] + 1) / 2) # + 1 for bias node
				weight_values = list(range(-weight_range, weight_range+1)) # ex: [-4 -3 -2 -1 0 1 2 3 4]
				weight_values.remove(0)
				weight_values = list(map(lambda w: w / (10**(math.ceil((0.1+weight_range)/10))), weight_values)) # make all weights -1 < w < 1
				random.shuffle(weight_values)
				weight_values = weight_values[0:nodes * (1 + layers[i - 1])] # trim off extras due to odd # of connections
			
			for n in range(nodes): 
				tempLayer.append(0)
			
			if i < (len(layers) - 1):
				tempLayer.append(-1) # add the bias node
			
			self.layers.append(tempLayer)		# the layer...
			self.weights.append(weight_values)	# and the weights that feed into it.


	def print_network(self):
		print("n---------------------------------")
		for layer, weights in zip(self.layers, self.weights):
			print(weights)
			print(layer)
		print("---------------------------------\n")


	def feed_forward(self, row):
		for layer in range(len(self.layers)):
			if layer == 0:
				self.layers[0] = row
				self.layers[0].append(-1)
			elif layer > 0:
				for node in range(self.blueprint[layer]):
					h = 0
					for i in range(len(self.layers[layer-1])):
						input = self.layers[layer-1][i]
						weight = self.weights[layer][i*(node+1)]
						h += input * weight
					self.layers[layer][node] = 1/(1 + numpy.exp(-h))
		self.print_network()


	def predict(self, test_set):
		predictions = []
		for row in test_set:
			print("Testing Row: " + str(row))
			self.feed_forward(row)
			classification = self.layers[-1].index(max(self.layers[-1]))
			temp = row[0:-1] + [classification]
			#row.append(classification)
			predictions.append(temp)
		return predictions










