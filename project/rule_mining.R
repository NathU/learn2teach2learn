library(arules)
mydata = read.transactions("C:/.conda/envs/cs450/course_work/project/rule_mine_me.csv", sep = ",")
op_rules = apriori(mydata, parameter = list(support = .005, confidence = .01, minlen = 2, maxlen = 6))

#interesting = subset(op_rules, rhs %in% "Anulada")
interesting = subset(op_rules, lhs %pin% "client.")
inspect(sort(interesting, by="support"))