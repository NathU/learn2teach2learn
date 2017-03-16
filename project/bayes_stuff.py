
import numpy
import sys
import datetime

ID = 0			# numeric
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
	filename = "bayes_me.csv"
	file = open("./"+filename, "r")
	raw_data = (file.read()).split("\n")
	file.close()
	data = list(map((lambda row: row.split(",")), raw_data))
	
	#for i in range(7):
		#print(data[i])
		
		
	# Prob of Client given month.
	#start_months = list(set(list(map(int, list(set(list(numpy.transpose(data))[F_INICIO]))))))
	#clients = list(set(list(map(int, list(set(list(numpy.transpose(data))[ID_CLIENTE]))))))
	
	month_client_dict = {}
	for m in range(1,13):
		month_client_dict[str(m)] = {}
	#print(month_client_dict)
	for row in data:
		month_client_dict[row[F_INICIO]][row[ID_CLIENTE]] = 0
	#print(month_client_dict)
	for row in data:
		month_client_dict[row[F_INICIO]][row[ID_CLIENTE]] += 1	
	#print(month_client_dict)
	
	month_totals = {}
	total_transactions = 0
	for m in range(1,13):
		sum = 0
		for t in month_client_dict[str(m)]:
			sum += month_client_dict[str(m)][t]
		month_totals[str(m)] = sum
		total_transactions += sum
	print(month_totals)
	print("Rows: "+str(len(data)))
	print("Transactions Counted: "+str(total_transactions))
	
	# Now Implement Naive Bayes...
	
	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)