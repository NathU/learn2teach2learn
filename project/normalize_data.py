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

F_INICIO = 1
RESELLER = 2
TIPO_T = 4
F_FIN = 6
PAGO = 7
ESTADO = 8

def main(argv):
	op = Operaciones()
	mydata = op.data
	
	print("\nsome data:")
	for i in range(7):
		print(mydata[i])

	return 0

	
	
	
class Operaciones:
	# param date_format control values: "offset", "month", or "bools"
	def __init__(self, date_format = "offset" ):
		filename = "./deals2.csv"
		raw_data = []
		try:
			file = open(filename, "r")
			raw_data = (file.read()).split("\n")
			file.close()
			self.data = list(map((lambda row: row.split(",")), raw_data))
			
		except:
			print("\terror while reading data")
		finally:
			file.close()
		
		self.base_date = self.to_dateObj(self.data[0][1])

		# replace each date string with the day offset from base_date
		#	OR, replace each date string with just the month value
		#	OR, replace each date string with a bool vector 12 long
		for i in range(len(self.data)):
			# strings
			f_inicio = self.data[i][F_INICIO]
			f_fin = self.data[i][F_FIN]
			
			# ints 1 to 12
			month_a = list(map(lambda a: int(a), list(f_inicio.split("/"))))[0]
			month_z = list(map(lambda a: int(a), list(f_fin.split("/"))))[0]
			
			final_inicio = None
			final_fin = None
			
			if date_format == "offset":
				final_inicio = self.normalize_date(self.to_dateObj(self.data[i][F_INICIO]) - self.base_date)
				final_fin = self.normalize_date(self.to_dateObj(self.data[i][F_FIN]) - self.base_date)
			
			elif date_format == "month":
				final_inicio = month_a
				final_fin = month_z			
			
			elif date_format == "bools":
				temp = [0,0,0,0,0,0,0,0,0,0,0,0]
				final_inicio = temp
				final_fin = temp
				final_inicio[month_a - 1] = 1
				final_fin[month_z - 1] = 1
			
			self.data[i][F_INICIO] = final_inicio
			self.data[i][F_FIN] = final_fin
	
	
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
	
	
	
	def to_dateObj(self, date_str):
		temp = list(map(lambda a: int(a), list(date_str.split("/"))))
		return datetime.date(temp[2],temp[0],temp[1])
		
	def normalize_date(self, timedelta):
		days = str(list(str(timedelta).split(" "))[0])
		return int(days) if days[0] != "0" else int(0)

		
		
		
		
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