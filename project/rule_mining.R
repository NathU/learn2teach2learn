# salesman, client ---> tipo_t
# salesman, client ---> estado

library(arules)
mydata = read.transactions("C:/.conda/envs/cs450/course_work/project/rule_mine_me.csv", sep = ",")
op_rules = apriori(mydata, parameter = list(support = .001, confidence = .001, minlen = 2, maxlen = 3))

interesting = subset(op_rules,lhs %in% "salesman.15")
#interesting = subset(op_rules,lhs %pin% "client.")

#tipo_t = c("Retiro", "Prestamo", "Cobranza", "Soporte", "Venta", "Arriendo")
#estado =c("Terminada", "Prestado", "Anulada", "Facturacion", "Armado", "Contabilidad")

interesting = subset(interesting,rhs %in% "Anulada")
inspect(sort(interesting, by="lift"))
