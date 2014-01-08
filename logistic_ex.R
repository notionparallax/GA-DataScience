# ref -- http://www.ats.ucla.edu/stat/r/dae/logit.htm

library(psych)
library(ggplot2)
adm <- read.csv("http://www.ats.ucla.edu/stat/data/binary.csv")
#gre Graduate Response Exam scores)
#gpa grade point average
#rank is a measure of prestige of the under graduate school 1 = High prestige 4 = low

head(adm)
summary(adm)
describe(adm)

xtabs(~admit + rank, data=adm)

# have a look at mean gre, gpa
library(doBy)
summaryBy(gre + gpa ~ admit + rank , data = adm , FUN = c(mean , sd))
summaryBy(gre + gpa ~ admit , data = adm , FUN = c(mean , sd))
summaryBy(gre + gpa ~ rank , data = adm , FUN = c(mean , sd))


# lets have a look at fitting a linear model What issues if any do you expect to find?
lin.fit <- lm(admit ~ ., data=adm)
summary(lin.fit)
plot(lin.fit)

# How about we remove the intercept it is the least important factor in the lm model above
lin.fit2 <- lm(admit ~ 0 + ., data=adm)
summary(lin.fit2)
plot(lin.fit)

# Clearly something is not right! infact something is very wrong.... Residuals are not NORMAL!
# Now lets fit a logistic regression with binomialresiduals
adm$rank <- factor(adm$rank) #make the rank variable a factor instead of a continuous variable

logit.fit <- glm(admit ~ ., family='binomial', data=adm) 
#family=binomial means that it's going to do a logistic regression
summary(logit.fit)
plot(logit.fit) #see anything useful?
# deviance resids -> measure of model fit (like resids in linear model)
# coeffs -> chg in log-odds of the output variable for unit increase in the input variable
# exponentiate coefs to produce odd ratios
# coeffs of indicator (dummy) vars are slightly different...for example, the coeff of rank2 represents the change in the log-odds of the output variable that comes going to a rank2 school instead of a rank1 school
# pay attention to the order of dummy variables and the output variable have a lok at the example http://data.princeton.edu/R/glms.html
# odds ratios can be found by exponentiating the log-odds ratios
exp(coef(logit.fit))

logit.fit.all <- glm(admit ~ gre * gpa * rank, family='binomial', data=adm)
summary(logit.fit.all)

logit.fit.all.2 <- update(logit.fit.all,  ~ . -gre:rank - gpa:rank -gre:gpa:rank)
summary(logit.fit.all.2)
names(logit.fit.all.2)

#compare the models
anova(logit.fit.all.2 , logit.fit.all , test="Chisq")
anova(logit.fit , logit.fit.all.2 , logit.fit.all ,  test="Chisq")
# seems like the interaction is not required and did not significantly inprove the model
anova(logit.fit.all.2 , test="Chisq")
anova(logit.fit.all , test="Chisq")
anova(logit.fit , test="Chisq")

#lets make some new data and predict the output
# note: important to give columns the same names as in the original df
new.data <- with(adm, data.frame(gre=mean(gre), gpa=mean(gpa), rank=factor(1:4)))
summary(new.data)

# predict probs for new data (varying rank)
new.data$rank.prob <- predict(logit.fit.all.2, newdata=new.data, type='response')
new.data

# predict probs for new data (varying gre)
new.data2 <- with(adm, data.frame(gre=rep(seq(from=200, to=800, length.out=100), 4), gpa=mean(gpa), rank=factor(rep(1:4, each=100))))
new.data2$pred <- predict(logit.fit.all.2, newdata=new.data2, type='response')
ggplot(new.data2, aes(x=gre, y=pred)) + geom_line(aes(colour=rank), size=1)

logit.fit.all.2
names(logit.fit.all.2)
logit.fit.all.2$fitted.values
adm.pred <- data.frame(adm , logit.fit.all.2$fitted.values )
head(adm.pred)
names(adm.pred)
ggplot(adm.pred , aes(x = logit.fit.all.2.fitted.values , fill = as.factor(admit) )) + geom_density(alpha=0.3)

pred.mean <- summaryBy(logit.fit.all.2.fitted.values ~ admit , data = adm.pred , FUN = mean)
pred.mean
ggplot(adm.pred , aes(x = logit.fit.all.2.fitted.values , fill = as.factor(admit) )) + 
  geom_density(alpha=0.3) +
  geom_vline (data=pred.mean , aes(xintercept = logit.fit.all.2.fitted.values.mean , colour = as.factor(admit) ))

