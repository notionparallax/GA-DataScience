# Exercise Solutions for Week 8 Decision Trees
# will need the rpart and tree packages
library("rpart")
library("tree")
library("datasets")

# Example to illustrate the difference in using GINI and Information for Decision tree split
data(package = 'rpart')

summary(cu.summary)

fit1 <- rpart(Reliability ~ Price + Country + Mileage + Type, data = cu.summary , parms = list(split='gini'))
fit2 <- rpart(Reliability ~ Price + Country + Mileage + Type, data = cu.summary , parms = list(split='information'))

par(mfrow = c(1,2) , mar = rep(0.1 , 4))

plot(fit1, margin = 0.05 , main = 'gini'); text(fit1, use.n = TRUE, cex=0.8)
plot(fit2, margin = 0.05 , main = 'information'); text(fit2, use.n = TRUE, cex=0.8)

summary(fit1)
summary(fit2)

summary(fit1 , cp= 0.06)


# 1st Import csv file with the computer buy data
buy<- read.csv (file="/home/mohammad/Data Mining/Data Sets/hkTab6_1.csv", sep=',',header=TRUE)

# Check all is good
summary(buy)

# First use rpart for the Model 
# change the minsplit from 20 to 5 (small dataset) same for maxcompete and maxsurrogate (these last 2 not essential)
cont <- rpart.control(minsplit = 5, maxcompete = 2 , maxsurrogate = 1)
buy.tr <- rpart( buys_computer ~ . , buy , method = 'class' , parms = list(split='gini'), control = cont)
# plot the tree with some improvments to make it a bit easier to read
plot(buy.tr, uniform = T , branch = 0.4, compress = T, margin = 0.1 , main = "Computer Buying Decision Tree")
text (buy.tr, all = T, use.n=T, fancy = T)

# Second use tree package for the Model 
t.cont <- tree.control (14, mincut = 2, minsize = 5 , mindev = 0.01)
buy.tr.tree <- tree (buys_computer ~ ., buy , split = "gini" , control = t.cont)
#plot(buy.tr.tree); text(buy.tr.tree, all=TRUE, cex=0.5)
plot(buy.tr.tree)
text(buy.tr.tree , all = TRUE , pretty = 10 , cex=0.8)
title(main = "Decision Tree Buy Computer - Tree package")
