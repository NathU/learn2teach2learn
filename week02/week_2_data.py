class Week2Data:
	def __init__(self, filename):
		self.filename = filename
		try:
			file = open(filename, "r")
			self.raw_data = (file.read()).split("\n")
			self.raw_data = list(map((lambda row: row.split(",")), self.raw_data))
			self.status = "success"
		except:
			self.status = "error"
		finally:
			file.close()

'''
Serious work needs to be done here in dealing with the catagorical data.
Particularly the 3rd and 4th fields.
'''
class CarData(Week2Data):
	def __init__(self, filename):
		super().__init__(filename)
		self.formatted_data = []
		
		
	def formatData(self):
		self.key = [{"vhigh":4,"high":3,"med":2,"low":1}, {"vhigh":4,"high":3,"med":2,"low":1}, {"2":1, "3":2, "4":3, "5more":4}, {"2":1, "4":2, "more":3}, {"small":1, "med":2, "big":3}, {"low":1, "med":2, "high":3}, {"unacc":0 , "acc":1 , "good":2 , "vgood":3 }]
		for row in self.raw_data:
			temp = []
			for k, r in zip(self.key, row):
				temp.append(k[r])
			self.formatted_data.append(temp)
			

class IrisData(Week2Data):
	def __init__(self, filename):
		super().__init__(filename)
		self.formatted_data = []
		
		
	def formatData(self):
		self.key = {"Iris-setosa":0, "Iris-versicolor":1, "Iris-virginica":2}
		for row in self.raw_data:
			temp = list(map(lambda f: float(f), row[0:len(row) - 1]))
			temp.append(self.key[row.pop()])
			self.formatted_data.append(temp)
			
			
class CancerData(Week2Data):
	def __init__(self, filename):
		super().__init__(filename)
		self.formatted_data = []
		
		
	def formatData(self):
		for row in self.raw_data:
			temp = []
			for i in range(len(row)):
				if (i > 0): # we're ignoring [0], the id number
					if (row[i] == "?"):
						temp.append(-1)
					else:
						temp.append(int(row[i]))
			self.formatted_data.append(temp)
			
			
			
			
			
			
			
			