# ------------------------ NOTES ------------------------ 
# 
# We're looking to solve:
#	1) Prob of Client given month:  
#		P(Client|Month) = P(Client,Month) / P(Month)
#
#
#



import numpy
import sys
import datetime
from math import log, exp

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


calc_individual = False

def main(argv):
	# ------------------------------- Preprocessing --------------------------
	filename = "bayes_me.csv"
	file = open("./"+filename, "r")
	raw_data = (file.read()).split("\n")
	file.close()
	data = list(map((lambda row: row.split(",")), raw_data))
	
	#start_months = list(set(list(map(int, list(set(list(numpy.transpose(data))[F_INICIO]))))))
	clients = list(set(list(map(int, list(set(list(numpy.transpose(data))[ID_CLIENTE]))))))
	
	month_client_dict = {} #
	for m in range(1,13):
		month_client_dict[str(m)] = {}
		for c in clients:
			month_client_dict[str(m)][str(c)] = 0

	for row in data:
		month_client_dict[row[F_INICIO]][row[ID_CLIENTE]] += 1	
	
	trans_per_client = {} #
	for c in clients:
		trans_per_client[str(c)] = 0
		
	trans_per_month = {} #
	for m in range(1,13):
		sum = 0
		for c in month_client_dict[str(m)]:
			sum += month_client_dict[str(m)][c]
			trans_per_client[c] += month_client_dict[str(m)][c]
		trans_per_month[str(m)] = sum
	# ---------------------------------------------------------------------------
	
	
	
	M = input("Month: ")
	p_M = trans_per_month[M] / len(data)
	
	if calc_individual:
		#print(clients)
		C = input("Client: ")
		joint_p_CM = month_client_dict[M][C] / len(data)
		bayes1 = joint_p_CM / p_M
		#print(str(joint_p_CM)+" / "+str(p_M)+" = "+str(bayes1)+"  ... right?")
		print("Probability of transaction with Client #"+C+" during Month #"+M+" = "+str(bayes1))
	
	else:
		probs = list(map(lambda c: (month_client_dict[M][str(c)] / len(data)) / (trans_per_month[M] / len(data)), clients))
		
		client_probs = {}
		for c, p in zip(clients, probs):
			client_probs[c] = p
		
		lim = int(input("View top <how many?> most likely Clients: "))
		print("-------------------------------")
		for k, i in zip(sorted(client_probs, key=client_probs.get, reverse=True), range(lim)):
			print("client "+str(k)+": "+str(client_probs[k]))	
	
	
	
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)