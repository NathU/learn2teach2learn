import sys
from my_NeuroNet import *
from week_5_data import *

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
	print(" 2 - Pima Indian Diabetes")
	print("-------------------")
	
	choice = 0
	var = None
	
	while (choice < 1 or choice > 3):
		choice = int(input("\nChoose your data set - "))

	if (choice == 1):
		var = IrisData()
	elif (choice == 2):
		var = PimaData()

	data_and_targets = var.get_data()

	print("data:")
	for i in range(10):
		print(data_and_targets[i])
	
	for i in range(3):
		random.shuffle(data_and_targets)
	
	print("data shuffled:")	
	for i in range(10):
		print(data_and_targets[i])

	
	
	
	
	'''
	t = float(input("\nTrain on what % of the dataset? - "))
	if t > 99 or t < 1:
		t = 70
	train_size = int(t / 100 * len(data_and_targets))
	print("Training size = " + str(train_size) + " of " + str(len(data_and_targets)) + " elements.")
	'''
	#training_set = data_and_targets[0:train_size]
	#verification_set = data_and_targets[train_size:]
	
	verification_set = data_and_targets[0:30]
	#print("Data with targets:")
	#for i in verification_set:
		#print(i)
	
	test_set = list(map(lambda row: row[0:-1], verification_set))
	#print("Data with NO targets:")
	#for i in test_set:
		#print(i)
	
	#myNet = NeuroNet([4, 2, 3])
	myNet = NeuroNet([8, 4, 2])
	myNet.print_network()
	#myNet.feed_forward([5.1, 3.5, 1.4, 0.2])
	#print("Feeding Forward...\n")
	predictions = myNet.predict(test_set)
	myNet.print_network()

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

	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)