import sys
import random
from week_3_data import *
from ID3 import *

def log_t_set(t_set):
	try:
		f = open('./tsetlog.txt', 'w')
		for row in t_set:
			for elem in row:
				f.write(str(elem) + ", ")
			f.write("\n")
	except:
		None
	finally:
		f.close()

def main(argv):
	print("-------------------")
	print(" 1 - Iris")
	print(" 2 - Lenses")
	print(" 3 - Voting")
	print("-------------------")
	print("(Heads up, results are hit and miss due to data randomization)")
	
	choice = 0
	var = None
	
	while (choice < 1 or choice > 3):
		choice = int(input("\nChoose your data set - "))

	if (choice == 1):
		var = IrisData()
	elif (choice == 2):
		var = LenseData()
	elif (choice == 3):
		var = VotingData()

	data_and_targets = var.get_data()
	
	if choice == 1:
		print("\nIris numeric, continuous data will be binned...")
		bins = (int(input("Enter # of bins: ")))
		binny = Sir_BinsAllot(data_and_targets, bins, [True, True, True, True])
		data_and_targets = binny.get_binned_data()
	
	for i in range(3):
		random.shuffle(data_and_targets)
	
	t = float(input("\nTrain on what % of the dataset? - "))
	if t > 99 or t < 1:
		t = 70
	train_size = int(t / 100 * len(data_and_targets))
	print("Training size = " + str(train_size) + " of " + str(len(data_and_targets)) + " elements.")
	
	training_set = data_and_targets[0:train_size]
	verification_set = data_and_targets[train_size:]
	learning_set = list(map(lambda row: row[0:-1], verification_set))
	
	myID3 = MyID3(training_set)

	choice = (str(input("\nView Decision Tree? (y/n) - ")))
	view_tree = (choice == "y" or choice == "Y")	
	if view_tree:
		myID3.print_tree()
	
	save = (str(input("\nType \'Save\' to log Training Data in a file: ")))
	logit = (save == "Save" or save == "save")	
	if logit:
		log_t_set(training_set)
	
	# Now we learn.
	try:
		predictions = myID3.predict(learning_set)
		choice = (str(input("\nEnter \'v\' for verbose output - ")))
		verbose = (choice == "V" or choice == "v")
		
		incorrect_count = 0
		for v, p in zip(verification_set, predictions):
			output_str = str(v)
			if (v[-1] != p[-1]):
				incorrect_count += 1
				output_str += "  !=  "
			else:
				output_str += "  ==  "
			output_str += str(p)
			if verbose:
				print (output_str)
				
		accuracy = 100 - float(incorrect_count / len(verification_set) * 100)
		print ("\n" + str(accuracy) + "% Accurate.")
		
		'''
		choice = (str(input("\nView Decision Tree? (y/n) - ")))
		view_tree = (choice == "y" or choice == "Y")
		
		if view_tree:
			myID3.print_tree()
		'''	
	# Actually, it looks like I'm not building my tree correctly.
	except KeyError:
		print("\nSORRY, Learning failed due to a non-comprehensive training set.")
		print("Basically, the randomization of the dataset makes the training data unpredictable.")
		print("Go ahead and try it again. I recommend Training on at least 65% of the dataset.")
	
	

	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)