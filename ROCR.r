library(ROCR)

data(ROCR.simple)
pred1 <- prediction( ROCR.simple$predictions, ROCR.simple$labels)

perf1 <- performance(pred1,"tpr","fpr")#true positive with False Positive ROC curve!
plot(perf1)

perf2 <- performance(pred1, "prec", "rec")
plot(perf2)

perf3 <- performance(pred1, "sens", "spec")
plot(perf3)


