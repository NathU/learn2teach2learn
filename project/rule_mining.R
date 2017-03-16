library(arules)
mydata = read.transactions("C:/.conda/envs/cs450/course_work/project/rule_mine_me.csv", sep = ",")
op_rules = apriori(mydata, parameter = list(support = .005, confidence = .005, minlen = 2, maxlen = 4))
interesting = subset(op_rules,lhs %pin% "start.")
interesting = subset(interesting,rhs %pin% "client.")
inspect(sort(interesting, by="support"))




more = subset(interesting, rhs %pin% "client.")

inspect(sort(more, by="support"))
