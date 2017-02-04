'''
	All data formatting, missing data handling, and bining is done here.
	
	TODO: handle missing data in credit card data. Everything else should be fine.
	
'''
import numpy
from math import floor
from scipy.stats import zscore
from scipy.stats import percentileofscore

class IrisData:
# ALL attributes are numeric, continuous. Zero missing attributes.
# This is a job for Sir BinsAllot!
	def __init__(self, filename = "../data/iris.csv"):
		self.filename = filename
		try:
			file = open(filename, "r")
			self.raw_data = (file.read()).split("\n")
			self.raw_data = list(map((lambda row: row.split(",")), self.raw_data))
			self.formatted_data = []

			for row in self.raw_data:
				numbers = list(map(lambda n: float(n), row[0:-1]))
				target = str(row[-1])
				new_row = numbers + [target]
				self.formatted_data.append(new_row)
			
			self.status = "data read successful"
		except:
			self.status = "error while reading data"
		finally:
			file.close()

	def get_data(self):
		return self.formatted_data
			
	def get_feature_names(self):
		return list(["sepal_len", "sepal_wi", "petal_len", "petal_wi"])


class VotingData:
# ALL data is nominal (boolean). 
# Note on Missing Attributes below:
#	"It is important to recognize that "?" in this database does 
#         not mean that the value of the attribute is unknown.  It 
#         means simply, that the value is not "yea" or "nay" "
# https://archive.ics.uci.edu/ml/machine-learning-databases/voting-records/house-votes-84.names

	def __init__(self, filename = "../data/votes.csv"):
		self.filename = filename
		try:
			file = open(filename, "r")
			self.raw_data = (file.read()).split("\n")
			self.raw_data = list(map((lambda row: row.split(",")), self.raw_data))
			self.formatted_data = []
			# for consistency, lets put the classes in the last column
			temp = numpy.transpose(self.raw_data)
			for row in temp[1:]:
				self.formatted_data.append(row)
			self.formatted_data.append(temp[0])
			self.formatted_data = numpy.transpose(self.formatted_data)
			
			self.status = "success"
		except:
			self.status = "error"
		finally:
			file.close()

	def get_data(self):
		return self.formatted_data
			
	def get_feature_names(self):
		return list(map(lambda i: "feat." + str(i), range(1,17)))
		

class LenseData:
# ALL data is nominal. Zero missing attributes.
# I personally modified the text file. It was dumb.
	def __init__(self, filename = "../data/lenses.txt"):
		self.filename = filename
		try:
			file = open(filename, "r")
			self.raw_data = (file.read()).split("\n")
			self.raw_data = list(map((lambda row: row.split("  ")), self.raw_data))
			# ignore [0], the row number
			#self.formatted_data = list(map(lambda row: row[1:], self.raw_data)) 
			self.status = "success"
		except:
			self.status = "error"
		finally:
			file.close()

	def get_data(self):
		return self.raw_data
			
	def get_feature_names(self):
		return list(["age", "spectacle_type", "is_astigmatic", "tear_production"])
		
		
		
class Sir_BinsAllot:
	def __init__(self, data, bins = 3, features = []):
		# Expects data+targets
		self.raw_data = list(numpy.transpose(data))[0:-1] # trim off the targets
		self.raw_data = list(map(lambda row: list(map(float, row)), self.raw_data))
		self.targets = list(numpy.transpose(data))[-1]

		self.dimm = len(data[0])-1
		self.bins = int(bins)
		
		# ex: [True, True, False, False, True] means bin features 0, 1, & 4
		self.bin_these = []
		if len(features) == 0:
			for i in range(self.dimm):
				self.bin_these.append(True) # bin all the features
		else:
			self.bin_these = features # bin the features specified
	
	
	def is_numeric(self, n):
		try: 
			float(n)
			int(n)
			return True
		except ValueError:
			return False
	
	
	def bin_by_equal_width(self):
	# We only bin numeric data
		for b, i in zip(self.bin_these, range(self.dimm)):
			if b == True:
				feature = list(self.raw_data[i])
				nominal_values = list(map(lambda v: "val" + str(v), range(self.bins)))
				d = float(100/self.bins)
				
				if self.is_numeric(feature[0]):
					zscores = zscore(feature)
					temp = []
					for score in zscores:
						percentile = percentileofscore(zscores, score, kind='mean')
						if percentile >= float(100):
							percentile = float(99)
						new_val = nominal_values[floor(percentile/d)]
						temp.append(new_val)
					self.raw_data[i] = temp


	def get_binned_data(self):
		self.bin_by_equal_width()
		r = self.raw_data
		r.append(self.targets)
		return list(numpy.transpose(r))

	''' TODO:
	def merge_attributes(self):
	# For numeric features:
		# generate ratios
		
		# examine coeff of variation (stddev/mean)
		
		# The pairing with lowest variation is candidate for merging.
		#	Should there be a max variation threshold? 
		#	Just because its lowest, doesn't mean it's good...
		
		# Values of the new feature could simply be the ratios.
		#	These, along with other numeric attributs, will probably
		#	have to be binned afterwards anyways.
		
	# For nominal features:
		# generate string pairings between features, ie: "yes big"
		
		# examine relative frequency of pair-strings
		
		# A high enough frequency could justify merging.
		#	But how high is high enough? Experiment...
		
		# Nominal values for the new feature could simply be the
		#	pair-string generated earlier
		
	# If successful, the new feature should be named something meaningful.
		
	'''

















	
	
