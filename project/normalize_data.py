#NOTES
#
#Data Example:
#    0            1           2              3         4             5            6                    7            8          9
#	id,    f_inicio,   reseller,   id_vendedor,   tipo_t,   id_cliente,       f_fin,                pago,      estado,   tecnico
#	 5,   11/5/2012,         \N,            14,    Venta,          242,   11/7/2012,   Pago ya Efectuado,   Terminada,        \N
#
#
#f_inicio: 
# - offset in days
# - bool vector, 12 long
#
#reseller:
# - bool vector, ? long
#
#tipo_t:
# - bool vector, 4 long
#
#pago:
# - bool vector, ? long
# 
#estado:
# - bool vector, 2 long
#
#


import numpy
import sys
import datetime

ID = 0
F_INICIO = 1
RESELLER = 2
ID_VENDADOR = 3
TIPO_T = 4
ID_CLIENTE = 5
F_FIN = 6
PAGO = 7
ESTADO = 8
ID_TECNICO = 9

def main(argv):
	
	op = Operaciones("month")
	
	excluded_columns = [ID, RESELLER, ID_TECNICO]
	op.write_newFile("rule_mine_me", excluded_columns)
	
	# Uncomment below to print sample of newly formatted data.
	'''
	mydata = op.data
	print("\nnew data looks like:")
	for i in range(7):
		print(mydata[i])
	'''

	return 0

	
	
	
class Operaciones:
	# param date_format control values: "offset", "month", or "bools"
	def __init__(self, date_format = "offset" ):
		self.filename = "deals2.csv"
		raw_data = []
		try:
			file = open("./"+self.filename, "r")
			raw_data = (file.read()).split("\n")
			file.close()
			self.data = list(map((lambda row: row.split(",")), raw_data))
			
		except:
			print("\terror while reading data")
		finally:
			file.close()
		
		self.base_date = self.to_dateObj(self.data[0][1])


		for i in range(len(self.data)):
			self.data[i][ID_VENDADOR] = "salesman."+str(self.data[i][ID_VENDADOR])
			self.data[i][ID_CLIENTE] = "client."+str(self.data[i][ID_CLIENTE])
			
			# Format Dates
			f_inicio = self.data[i][F_INICIO]
			f_fin = self.data[i][F_FIN]
			
			# ints 1 to 12
			month_a = list(map(lambda a: int(a), list(f_inicio.split("/"))))[0]
			month_z = list(map(lambda a: int(a), list(f_fin.split("/"))))[0]
			
			if date_format == "offset":
				self.data[i][F_INICIO] = self.normalize_date(self.to_dateObj(self.data[i][F_INICIO]) - self.base_date)
				self.data[i][F_FIN] = self.normalize_date(self.to_dateObj(self.data[i][F_FIN]) - self.base_date)
			
			elif date_format == "month":
				self.data[i][F_INICIO] = month_a
				self.data[i][F_FIN] = month_z			
			
			elif date_format == "bools":
				final_inicio = [0,0,0,0,0,0,0,0,0,0,0,0]
				final_fin = [0,0,0,0,0,0,0,0,0,0,0,0]
				final_inicio[month_a - 1] = 1
				final_fin[month_z - 1] = 1
				temp = self.data[i][0:F_INICIO] + final_inicio + self.data[i][F_INICIO+1:F_FIN] + final_fin + self.data[i][F_FIN+1:]
				self.data[i] = temp
			
		
		# FOr rule mining, we want nominal catagories
		'''
		# TODO: replace 'reseller' with a bool vector
		resellers = list(numpy.transpose(self.data))[RESELLER]
		reseller_vals = list(set(resellers))
		print("\nResellers:")
		print(reseller_vals)
		
		# TODO: replace 'tipo_t' with a bool vector
		types = list(numpy.transpose(self.data))[TIPO_T]
		type_vals = list(set(types))
		print("\nTransaction Types:")
		print(type_vals)
		
		# TODO: replace 'pago' with a bool vector
		pagos = list(numpy.transpose(self.data))[PAGO]
		pago_vals = list(set(pagos))
		print("\nPagos:")
		print(pago_vals)
		
		# TODO: replace 'estado' with a bool vector
		states = list(numpy.transpose(self.data))[ESTADO]
		state_vals = list(set(states))
		print("\nState Values:")
		print(state_vals)
		
		
		salesmen = list(numpy.transpose(self.data))[ID_VENDADOR]
		salesmen_IDs = list(set(salesmen))
		print("\nSalesmen IDs:")
		print(salesmen_IDs)
		
		clients = list(numpy.transpose(self.data))[5]
		client_IDs = list(set(clients))
		print("\nClient IDs:")
		print(client_IDs)
		'''
		
	
	
	
	def to_dateObj(self, date_str):
		temp = list(map(lambda a: int(a), list(date_str.split("/"))))
		return datetime.date(temp[2],temp[0],temp[1])
		
	def normalize_date(self, timedelta):
		days = str(list(str(timedelta).split(" "))[0])
		return int(days) if days[0] != "0" else int(0)

	def write_newFile(self, new_filename, excluded_columns):
		print("Excluded Columns: "+str(excluded_columns))
		# write newly formatted data to a file.
		#new_filename = "new_"+self.filename
		try:
			f = open("./"+new_filename+".csv", 'w')
			for row in self.data:
				#row_to_write = list(map(filter i: i not in excluded_columns, range(len(row))))
				row_to_write = []
				for i in range(len(row)):
					if i not in excluded_columns:
						row_to_write.append(row[i])
				row_str = ",".join(list(map(lambda elem: str(elem), row_to_write)))
				f.write(row_str)
				if row is not self.data[-1]:
					f.write("\n")
				
			f.close()
		except:
			print("...error writing new file...")
		
		
		
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