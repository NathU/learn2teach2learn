
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


def main(argv):
	bayes = Bayes()
	month = "4"
	group_size = 5
	res = bayes.calc_group(month, group_size)
	print(res)
	
	write_file(res, month, "test_file" )
	
	return 0
	
	
	
def write_file(results, month, new_filename):
	try:
		f = open("./"+new_filename+".csv", 'w')
		for client in results:
			write_str = client +","+ month +","+ str(results[client]) + "\n"
			f.write(write_str)
		f.close()
	except:
		print("...error writing new file...")
	
	
	
	
	
	
class Bayes:
	def __init__(self):
		# ------------------------------- Preprocessing --------------------------
		filename = "bayes_me.csv"
		file = open("./"+filename, "r")
		raw_data = (file.read()).split("\n")
		file.close()
		self.data = list(map((lambda row: row.split(",")), raw_data))
		
		#start_months = list(set(list(map(int, list(set(list(numpy.transpose(self.data))[F_INICIO]))))))
		self.clients = list(set(list(map(int, list(set(list(numpy.transpose(self.data))[ID_CLIENTE]))))))
		
		self.month_client_dict = {} #
		for m in range(1,13):
			self.month_client_dict[str(m)] = {}
			for c in self.clients:
				self.month_client_dict[str(m)][str(c)] = 0

		for row in self.data:
			self.month_client_dict[row[F_INICIO]][row[ID_CLIENTE]] += 1	
		
		self.trans_per_client = {} #
		for c in self.clients:
			self.trans_per_client[str(c)] = 0
			
		self.trans_per_month = {} #
		for m in range(1,13):
			sum = 0
			for c in self.month_client_dict[str(m)]:
				sum += self.month_client_dict[str(m)][c]
				self.trans_per_client[c] += self.month_client_dict[str(m)][c]
			self.trans_per_month[str(m)] = sum
		# ---------------------------------------------------------------------------
	
	
	def calc_individual(self, M = None, C = None):
		# Expects strings M, C
		if M == None:
			M = input("Month: ")
		if C == None:
			C = input("Client: ")
		p_M = self.trans_per_month[M] / len(self.data)
		joint_p_CM = self.month_client_dict[M][C] / len(self.data)
		bayes1 = joint_p_CM / p_M
		#print(str(joint_p_CM)+" / "+str(p_M)+" = "+str(bayes1)+"  ... right?")
		#print("Probability of transaction with Client #"+C+" during Month #"+M+" = "+str(bayes1))
		return bayes1
	
	def calc_group(self, M = None, lim = 5):
		if M == None:
			M = input("Month: ")
		#if lim == None:
			#lim = int(input("View top <how many?> most likely self.clients: "))
			
		probs = list(map(lambda c: (self.month_client_dict[M][str(c)] / len(self.data)) / (self.trans_per_month[M] / len(self.data)), self.clients))
		
		client_probs = {}
		for c, p in zip(self.clients, probs):
			client_probs[c] = p
		
		self.most_likely_clients = {}
		
		#print("-------------------------------")
		for k, i in zip(sorted(client_probs, key=client_probs.get, reverse=True), range(lim)):
			#print("client "+str(k)+": "+str(client_probs[k]))	
			self.most_likely_clients[str(k)] = client_probs[k]
	
		return self.most_likely_clients # idk why its not sorting as it should...
		#return sorted(self.most_likely_clients, key=self.most_likely_clients.get, reverse=True)
	
	
	
	
	
if __name__ == "__main__":
	main(sys.argv)