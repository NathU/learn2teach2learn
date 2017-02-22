import sys
from my_NeuroNet import *
from week_5_data import *



def log_accuracies(acc_hist, valid_hist):
	try:
		f = open('./accuracy_log.csv', 'w')
		for a, v in zip(acc_hist[1:], valid_hist[1:]):
			f.write(str(a)+","+str(v)+"\n")
		f.close()
	except:
		print("...error writing accuracy log file...")
	
		


def main(argv):
	
	# Acquire Data:
	print("-------------------")
	print(" 1 - Iris")
	print(" 2 - Pima Indian Diabetes")
	print("-------------------")
	choice = 0
	var = None
	while (choice < 1 or choice > 2):
		choice = int(input("\nChoose your data set - "))
	if (choice == 1):
		norm = (str(input("Normalize Iris dataset?(y/n) - ")))
		if (norm == "Y" or norm == "y"):
			var = IrisData(True)
		else:
			var = IrisData(False)
	elif (choice == 2):
		var = PimaData()
	data_and_targets = var.get_data()
	
	random.shuffle(data_and_targets)
	shuffles = 1

	# Partition & Prepare data for training & testing	
	t = float(input("\nTrain on what % of the dataset? - "))
	v = float(input("Validate with what % of the training set? - "))
	
	v = int(t * (v/100))
	t -= v
	
	train_size = int(t / 100 * len(data_and_targets))
	validation_size = int(v / 100 * len(data_and_targets))
	print("Training with " + str(train_size) + " of " + str(len(data_and_targets)) + " elements.")
	print("Validating with " + str(validation_size) + " of " + str(len(data_and_targets)) + " elements.")
	training_set = data_and_targets[0:train_size]
	
	# Training set must contain all targets
	all_classes = list(set(list(map(lambda row: row[-1], data_and_targets))))
	training_classes = list(set(list(map(lambda row: row[-1], training_set))))
	while (training_classes != all_classes):
		random.shuffle(data_and_targets)
		training_set = data_and_targets[0:train_size]
		training_classes = list(set(list(map(lambda row: row[-1], training_set))))
		shuffles += 1
	print("  (required "+str(shuffles)+" shuffle(s))")
	
	validation_verification_set = data_and_targets[train_size:train_size+validation_size]
	validation_set = list(map(lambda row: row[0:-1], validation_verification_set))
	
	verification_set = data_and_targets[validation_size+train_size:]
	test_set = list(map(lambda row: row[0:-1], verification_set))


	# Let user choose network config & batch/seq updating 
	nonInput_layers = int(input("\nUse How many Layers? - "))
	targets = len(list(set(list(map(lambda row: row[-1], data_and_targets)))))
	inputs = len(test_set[0])
	bluePrint = [inputs]
	for i in range(nonInput_layers-1):
		bluePrint.append(int(input("How many Nodes for Hidden Layer #" + str(i+1) + "? - ")))
	bluePrint.append(targets)

	
	# Construct the Network. Weights are now assigned.
	myNet = NeuroNet(bluePrint)
	print("\nNewly Initialized Network:")
	print("  (\'W0\' is a placeholder, \'L0\' will hold our Inputs.)")
	myNet.print_network()
	
	
	# Stopping Criteria: train for n epochs. Once done, revert to best state.
	epochs = int(input("\nTrain for How Many Epochs? - "))
	training_history = [0]
	validation_history = [0]
	bestState_layers = []
	bestState_weights = []
	i_peak = 0
	for e in range(epochs):
		myNet.train(training_set)
		if myNet.training_accuracy > max(training_history):
			bestState_layers = myNet.layers
			bestState_weights = myNet.weights
			i_peak = len(training_history)
		training_history.append(myNet.training_accuracy)
		validation_history.append(get_accuracy(validation_verification_set, myNet.predict(validation_set)))
	print ("\nAchieved "+str(training_history[i_peak])+"% TRAINING accuracy at Epoch #"+str(i_peak))
	
	
	# log learning trends for graphing later
	log_accuracies(training_history, validation_history)	
	
	# Restore best state
	myNet.layers = bestState_layers
	myNet.weights = bestState_weights
	
	# Proceed with Testing
	predictions = myNet.predict(test_set)

	accuracy = get_accuracy(verification_set, predictions)
	print ("\nTESTING accuracy: "+str(accuracy) + "%")
	
	
	
	
def get_accuracy(verification_set, predictions):
	
	# Determine & report Training accuracy
	incorrect_count = 0
	for v, p in zip(verification_set, predictions):
		if (v[-1] != p[-1]):
			incorrect_count += 1
			
	accuracy = 100 - float(incorrect_count / len(verification_set) * 100)
	
	return accuracy
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)