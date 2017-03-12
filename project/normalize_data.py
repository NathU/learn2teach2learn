
#import numpy
import sys
import datetime

def main(argv):
	data = operaciones()
	base_date = to_dateObj(data[0][1])

	print("PRE-normalize:")
	for i in range(7):
		print(data[i])

	print("POST-normalize:")
	# replace each date string with the day offset from base_date
	for i in range(len(data)):
		data[i][1] = normalize_date(to_dateObj(data[i][1]) - base_date)
		data[i][7] = normalize_date(to_dateObj(data[i][6]) - base_date)
		#print(data[i])
	#print(data[-1])
	
	for i in range(7):
		print(data[i])

	return 0

	
	
def to_dateObj(date_str):
	#print("\tdate_str = "+date_str)
	temp = list(map(lambda a: int(a), list(date_str.split("/"))))
	#print("\ttemp = "+str(temp))
	return datetime.date(temp[2],temp[0],temp[1])
	
def normalize_date(timedelta):
	days = str(list(str(timedelta).split(" "))[0])
	return int(days) if days[0] != "0" else int(0)
	
	
	
def operaciones():
	filename = "./deals2.csv"
	raw_data = []
	try:
		file = open(filename, "r")
		raw_data = (file.read()).split("\n")
		file.close()
		raw_data = list(map((lambda row: row.split(",")), raw_data))
		
		
		
	except:
		print("error while reading data")
	finally:
		file.close()
		return raw_data
	
	
'''
# This is just reference code to help me...

def abaloneData():
	filename = "./abalone.csv"
	new_filename = "./abalone_prepped.csv"
	try:
		file = open(filename, "r")
		raw_data = (file.read()).split("\n")
		file.close()
		raw_data = list(map((lambda row: row.split(",")), raw_data))
		formatted_data = []
		
		print(raw_data[0])
		
		targets = list(numpy.transpose(raw_data))[-1]
		
		nominal_data = list(numpy.transpose(raw_data))[0]
		key = {"M":0,"I":1,"F":2}
		three_rows = []
		for g in nominal_data:
			gender = [0,0,0]
			gender[key[str(g)]] = 1
			formatted_data.append(gender)
		formatted_data = list(numpy.transpose(formatted_data))
		formatted_data = list(map(lambda row: list(row), formatted_data))
		
		print(formatted_data[0])
		
		raw_data = list(numpy.transpose(raw_data))[1:-1] # avoid targets & first column
		raw_data = list(map(lambda row: list(map(float, row)), raw_data)) # numericize for normalization
		
		for row in raw_data:
			temp = zscore(row)
			# to Decimal, chop precision to 5, to string, to float, ta-da!
			temp = list(map(lambda f: float((Decimal(str(f)).quantize(Decimal('1.00000'))).to_eng_string()), temp))
			formatted_data.append(temp)
		formatted_data.append(targets)
		formatted_data = list(numpy.transpose(formatted_data))
		formatted_data = list(map(lambda row: list(row), formatted_data))
		
		print(formatted_data[0])
		
		try:
			f = open(new_filename, 'w')
			for row in formatted_data:
				nums = list(map(lambda f: float(f), row[:-1]))
				f.write(str(nums)[1:-1] + ", " + row[-1] + "\n")
			f.close()
		except:
			print("...error writing new file...")

	except:
		print("error while reading data")
	finally:
		file.close()
'''

	
	
if __name__ == "__main__":
	main(sys.argv)