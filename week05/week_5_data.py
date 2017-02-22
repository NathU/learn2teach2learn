'''
	
'''
import numpy
from scipy.stats import zscore


class IrisData:
# ALL attributes are numeric, continuous. Zero missing attributes.
	def __init__(self, normalize = True):
		self.filename = "../data/iris.csv"
		self.normalize = normalize
		try:
			file = open(self.filename, "r")
			self.raw_data = (file.read()).split("\n")
			self.raw_data = list(map((lambda row: row.split(",")), self.raw_data))
			self.formatted_data = []
			
			# Numericize the targets
			self.targets = list(numpy.transpose(self.raw_data))[-1]
			name_set = list(set(self.targets))
			num_targets = list(map(lambda t: name_set.index(t), self.targets))
			
			# Numericize the Features
			#self.raw_data = list(numpy.transpose(self.raw_data))[0:-1] # trim off the targets
			#self.raw_data = list(map(lambda row: list(map(float, row)), self.raw_data))
			self.feat_data = list(map(lambda row: list(map(float, row[0:-1])), self.raw_data)) # make floats!
			self.feat_data = list(numpy.transpose(self.feat_data))
			
			#for i in range(len(self.raw_data)):
				#self.raw_data[i].append(num_targets[i])
			
			for row in self.feat_data:
				temp = row
				if self.normalize:
					temp = zscore(row)
				self.formatted_data.append(temp)

			self.formatted_data.append(num_targets)
			self.formatted_data = list(numpy.transpose(self.formatted_data))
			self.formatted_data = list(map(lambda row: list(row), self.formatted_data))
			
			self.status = "data read successful"
		except:
			self.status = "error while reading data"
		finally:
			file.close()

	def get_data(self):
		#return self.raw_data
		return self.formatted_data
			
	def get_class_names(self):
		return list(["setossa", "versicolor", "virginica"])

		


class PimaData:
# ALL attributes are numeric, continuous. Missing attributes, but NO IDEA how to tell.
	def __init__(self, filename = "../data/pima.csv"):
		self.filename = filename
		try:
			file = open(filename, "r")
			self.raw_data = (file.read()).split("\n")
			self.raw_data = list(map((lambda row: row.split(",")), self.raw_data))
			self.formatted_data = []
			
			self.targets = list(numpy.transpose(self.raw_data))[-1]
			self.targets = list(map(lambda f: float(f), self.targets))
			#name_set = list(set(self.targets))
			#names = list(map(lambda t: name_set.index(t), self.targets))
			
			self.raw_data = list(numpy.transpose(self.raw_data))[0:-1] # trim off the targets
			self.raw_data = list(map(lambda row: list(map(float, row)), self.raw_data))
			
			for row in self.raw_data:
				temp = zscore(row)
				self.formatted_data.append(temp)
			self.formatted_data.append(self.targets)
			self.formatted_data = list(numpy.transpose(self.formatted_data))
			self.formatted_data = list(map(lambda row: list(row), self.formatted_data))
			
			self.status = "data read successful"
		except:
			self.status = "error while reading data"
		finally:
			file.close()

	def get_data(self):
		return self.formatted_data










	
	
