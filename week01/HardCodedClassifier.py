import sys
import random
from sklearn import datasets
iris = datasets.load_iris()

# This HardCodedClassifier class can be initialized with a 
#	classifying function. Otherwise a naive, default function
#	is assigned.
# The classifying function must accept an input vector as a 
#	list and return that input vector paired with it's 
#	predicted class.
#
# INPUT: [x1, x2, ... xn]
# OUTPUT: {'data' : [x1, x2, ... xn], 'class' : y }
class HardCodedClassifier:
	def __init__(self, class_func = None):
		default_func = (lambda input_vector: {"data" : input_vector, "class" : 0})
		self.classify = default_func if class_func is None else class_func 
		
	# ***Not used in this assignment***
	def fit(self, training_set):
		None
	
	def predict(self, dataset):
		return list(map(self.classify, dataset))

		
		
# MAIN pairs, then shuffles the data rows. Then uses the
#	HardCodedClassifier to classify the Iris data. Then
#	displays prediction accuracy data.
#
# INPUT: 'V' or 'v' will yield verbose accuracy data.
def main(argv):
	
	# before randomizing, pair all data with given targets
	data_and_targets = []
	for i in range(len(iris.data)):
		t = {"data" : iris.data[i], "target" : iris.target[i]}
		data_and_targets.append(t)
	
	# randomize data rows. This yields different accuracies each execution.
	random.shuffle(data_and_targets)
	
	# ***Not used in this assignment***
	names = iris.target_names
	
	# ***Not used in this assignment***
	training_set = data_and_targets[0:(len(data_and_targets) // 3)]
	
	learning_set = data_and_targets[(len(data_and_targets) // 3):]
	DataOnly_learning_set = list(map((lambda x: x["data"]), learning_set))
	
	hc = HardCodedClassifier()
	predictions = hc.predict(DataOnly_learning_set)
	
	# Determine accuracy of our HardCodedClassifier
	incorrect_count = 0
	user_input = (str(input("Enter \'V\' for verbose output - ")))
	verbose = (user_input == "V" or user_input == "v")
	for i in range(len(learning_set)):
		output_str = str(learning_set[i])
		if ((learning_set[i])["target"] != (predictions[i])["class"]):
			incorrect_count += 1
			output_str += "  !=  "
		else:
			output_str += "  ==  "
		output_str += str(predictions[i])
		if verbose:
			print (output_str)
			
	print (str(incorrect_count / len(learning_set) * 100) + "% Accurate.")
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)