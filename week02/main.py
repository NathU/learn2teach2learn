import sys
import random
from week_2_data import *
from my_Knn import *


def main(argv):
	print("-------------------")
	print(" 1 - Cars")
	print(" 2 - Iris")
	print(" 3 - Cancer")
	print("-------------------")
	
	choice = 0
	var = None
	rules = None
	normalize = False
	
	while (choice < 1 or choice > 3):
		choice = int(input("Choose your data set - "))

	if (choice == 1):
		var = CarData("../data/cars.csv")
	elif (choice == 2):
		var = IrisData("../data/iris.csv")
		normalize = True
	elif (choice == 3):
		var = CancerData("../data/cancer.csv")

	var.formatData()
	data_and_targets = var.formatted_data
	random.shuffle(data_and_targets)
	
	t = float(input("Train on what % of the dataset? - "))
	if t > 99 or t < 1:
		t = 70
	train_size = int(t / 100 * len(data_and_targets))
	print("Training size = " + str(train_size) + " of " + str(len(data_and_targets)) + " elements.\n")
	
	training_set = data_and_targets[0:train_size]
	validation_set = data_and_targets[train_size:]
	learning_set = list(map(lambda row: row[0:-1], validation_set))
	
	
	k = int(input("Calculate using How Many neighbors? - "))
	my_Knn = MyKnnClassifier(k, normalize)
	my_Knn.fit(training_set)
	predictions = my_Knn.predict(learning_set)
	
	
	choice = (str(input("Enter \'V\' for verbose output - ")))
	verbose = (choice == "V" or choice == "v")
	
	incorrect_count = 0
	for v, p in zip(validation_set, predictions):
		output_str = str(v)
		if (v[-1] != p[-1]):
			incorrect_count += 1
			output_str += "  !=  "
		else:
			output_str += "  ==  "
		output_str += str(p)
		if verbose:
			print (output_str)
			
	accuracy = 100 - float(incorrect_count / len(validation_set) * 100)
	print (str(accuracy) + "% Accurate.")
	

	
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)