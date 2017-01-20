import numpy # for transpose
from scipy.stats import zscore


class MyKnnClassifier:
	def __init__(self, K = 3, useZscore = False):
		self.normalize = useZscore
		if self.normalize:
			self.z_set = []
		self.K = K if (K % 2 != 0) else (K + 1) #just keeping it odd...
		
		
	def fit(self, training_set):
		self.t_set = training_set
		self.target_max = int(max((numpy.transpose(self.t_set))[-1]))
		if self.normalize:
			self.z_set = list(map(zscore, (numpy.transpose(self.t_set))[0:-1]))
			self.z_set = list(numpy.transpose(self.z_set))
			
	
	
	
	def predict(self, learning_set):
		self.predictions = []
		
		for row in learning_set:
			temp = row if self.normalize is False else self.get_Z_scores(row)
			diffs = {}
			for i in range(len(self.t_set)):
				diffs[self.calc_dist(temp, i)] = i
			
			nearest_classes = list([0] * (self.target_max + 1))
			for i, key in zip(range(self.K), sorted(diffs)):
				classification = (self.t_set[diffs[key]])[-1]
				nearest_classes[classification] += 1
			
			c = nearest_classes.index(max(nearest_classes))
			row.append(c)
			
			self.t_set.append(row)
			self.predictions.append(row)
		return self.predictions

		
		
	
	def get_Z_scores(self, learning_row):
		temp_tset = list(map(lambda row: row[0:-1], self.t_set))
		temp_tset.append(learning_row)
		'''
		#For static Z_set
		temp_zset = list(map(zscore, (numpy.transpose(temp_tset))))
		temp_zset = list(numpy.transpose(temp_zset))
		L_row_zscores = temp_zset[-1]
		self.z_set.append(L_row_zscores)
		'''
		#For Dynamic Z_set... possibly a bad idea, I'm not sure.
		self.z_set = list(map(zscore, (numpy.transpose(temp_tset))))
		self.z_set = list(numpy.transpose(self.z_set))
		L_row_zscores = self.z_set[-1]		
		
		return L_row_zscores
	
	
	
	
	def calc_dist(self, L_row, T_row_index):
		T_row = []
		if self.normalize:		
			T_row = self.z_set[T_row_index]
		else:
			T_row = (self.t_set[T_row_index])[0:-1]
		dimm = len(L_row)
		dist = 0
		for L, T in zip(L_row, T_row):
			if (L == -1 or T == -1):
				dimm -= 1
			else:
				dist += ((L - T)**2)
		# My solution for missing data is to weight the distance by 
		#   the number of dimmensions accounted for.
		return float(dist / dimm)
	
	
	
	
	
	
	
	