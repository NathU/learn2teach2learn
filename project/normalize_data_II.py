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
F_INICIO = 1	# numeric
RESELLER = 2
ID_VENDADOR = 3	# numeric
TIPO_T = 4
ID_CLIENTE = 5	# numeric
F_FIN = 6		# numeric
PAGO = 7
ESTADO = 8
ID_TECNICO = 9	# numeric
DURATION = 10	# numeric

def main(argv):
	
	op = Operaciones("deals2.csv")
	op.format_dates_by(date_format = "month", duration_format = "days")
	#op.nominalize([F_INICIO, F_FIN, ID_VENDADOR, ID_CLIENTE, DURATION])
	
	excluded_columns = []#[ID, RESELLER, ID_TECNICO]
	op.write_newFile("bayes_me", excluded_columns)
	
	# Uncomment below to print sample of newly formatted data.
	'''
	mydata = op.data
	print("\nnew data looks like:")
	for i in range(7):
		print(mydata[i])
	'''
	
	# Next, build prob vectors of companies given month.
	'''
	mydata = op.data
	clients = list(numpy.transpose(mydata))[ID_CLIENTE]
	client_IDs = list(set(clients))
	#print(client_IDs)
	#print(len(client_IDs))
	months = list(set(list(numpy.transpose(mydata))[F_INICIO]))
	#print(str(list(set(months))))
	
	month_dict = {}
	client_dict = {}
	
	for client in client_IDs:
		client_dict[client] = 0
	
	for month in months:
		temp = {}
		temp = client_dict
		month_dict[month] = temp
	
	#print(client_dict)
	#print(month_dict['start.1'])
	'''
	
	'''
	for row in mydata:
		temp = {}
		temp = client_dict
		temp[row[ID_CLIENTE]] += 1
		month_dict[row[F_INICIO]][row[ID_CLIENTE]] += 1
	
	for m in month_dict:
		temp = str(m) + " | "
		for c in month_dict[m]:
			temp += str(month_dict[m][c]) + ", "
		print (temp+"\n")
	'''
	
	return 0

	
	
	
class Operaciones:
	# param date_format control values: "offset", "month", or "bools"
	def __init__(self, filename):
		self.filename = filename
		self.date_format = ""
		self.add_duration = False
		
		raw_data = []
		try:
			file = open("./"+self.filename, "r")
			raw_data = (file.read()).split("\n")
			file.close()
			self.data = list(map((lambda row: row.split(",")), raw_data))
			
		except:
			print("\t error while reading data")
		finally:
			file.close()
		
		
	
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

			
		
	# date_format options: ["offset", "month", "bools"]
	# duration_format options: ["days", "weeks"]
	def format_dates_by(self, date_format, duration_format = "" ):
		self.base_date = self.to_dateObj(self.data[0][F_INICIO])
		self.add_duration = duration_format != ""
		self.duration_format = duration_format

		for i in range(len(self.data)):
			# Format Dates
			f_inicio = self.data[i][F_INICIO]
			f_fin = self.data[i][F_FIN]
			
			# ints 1 to 12
			month_a = list(map(lambda a: int(a), list(f_inicio.split("/"))))[0]
			month_z = list(map(lambda a: int(a), list(f_fin.split("/"))))[0]
			# ints 0 to ?
			day_a = self.normalize_date(self.to_dateObj(f_inicio) - self.base_date)
			day_z = self.normalize_date(self.to_dateObj(f_fin) - self.base_date)
			
			if self.add_duration:
				if duration_format == "days":
					self.data[i].append(day_z - day_a)
				elif duration_format == "weeks":
					self.data[i].append(int((day_z - day_a) / 7))
				
			if date_format == "offset":
				self.data[i][F_INICIO] = day_a
				self.data[i][F_FIN] = day_z
			
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
	
	
	def nominalize(self, numeric_features = [F_INICIO, F_FIN, ID_VENDADOR, ID_CLIENTE, ID_TECNICO]):
		names = {F_INICIO:"start.", F_FIN:"end.", ID_VENDADOR:"salesman.", ID_CLIENTE:"client.", ID_TECNICO:"tech."}
		if self.add_duration:
			names[DURATION] = "dur-"+self.duration_format+"."
		for i in range(len(self.data)):
			for j in range(len(self.data[i])):
				if j in numeric_features:
					name = names[j]
					self.data[i][j] = name+str(self.data[i][j])
	



		
		
		# just some scrap code...
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
	
	
if __name__ == "__main__":
	main(sys.argv)