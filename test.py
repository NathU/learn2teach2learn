import sys
import numpy

def main(argv):

	nearest_classes = list([0] * (2 + 1))
	print (nearest_classes)
	
	'''
	mydict = {0.74112688627241152: 2, 1.2083599405262133: 1, 2.1993689618123407: 0, 1.9945862508556176: 5, 1.9839629855920649: 7, 2.6741769864363345: 6, 1.2284823340726763: 3, 1.9832893953520969: 8, 2.1949689305232294: 4}
	vals = list(mydict.values())
	
	print("MyDict:")
	print(mydict)
	print("\nMyDict Sorted:")
	for key in sorted(mydict):
		print (str(key) + " : " + str(mydict[key]))
	
	
	
	mydict = sorted(mydict.iterkeys())
	print("MyDict Sorted?:")
	print(mydict)
	
	print ("values:")
	print (vals)
	print (sorted(mydict))
	
	'''
	
	
if __name__ == "__main__":
	main(sys.argv)