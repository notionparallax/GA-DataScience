library('ggplot2')

# First Linear regression?
set.seed(1)

x <- seq(-10, 10, by = 0.01)
y <- 1 - x ^ 2 + rnorm(length(x), 0, 5)

ggplot(data.frame(X = x, Y = y), aes(x = X, y = Y)) + 
  geom_point() +
  geom_smooth(se = FALSE)

summary(lm(y ~ x)) # fit any good?
summary(lm(y ~ x))$r.squared
names(summary(lm(y ~ x))) # if your not sure how to get particular elements on their own
summary(lm(y ~ x))$sigma
plot(lm(y ~ x))


# How about a curve
x.squared <- x ^ 2

ggplot(data.frame(XSquared = x.squared, Y = y), aes(x = XSquared, y = Y)) +
  geom_point() +
  geom_smooth(method = 'lm', se = FALSE)
# All of a sidden it looks like a straight line is needed however x squared is not a straight line
summary(lm(y ~ x.squared)) # fit any good?
summary(lm(y ~ x.squared))$r.squared

plot(lm(y ~ x.squared))

# lets create some more data
set.seed(1)
x <- seq(0, 1, by = 0.01)
y <- sin(2 * pi * x) + rnorm(length(x), 0, 0.1)
df <- data.frame(X = x, Y = y)
ggplot(df, aes(x = X, y = Y)) +
  geom_point()

summary(lm(Y ~ X, data = df))

# lets have a look at the graph
ggplot(data.frame(X = x, Y = y), aes(x = X, y = Y)) +
  geom_point() +
  geom_smooth(method = 'lm', se = T)

plot(lm(Y ~ X, data = df)) #these data look ok, but the problems come out obviously when you look at the plots of the LM

df <- transform(df 
                , X2 = X ^ 2
                , X3 = x ^ 3)
summary(df)
summary(lm(Y ~ X + X2 + X3, data = df))
df.fit <- lm(Y ~ X + X2 + X3, data = df)

# What is the problem with this model?
library(gvlma)
summary(gvlma(df.fit))

library(car)
#states <- as.data.frame(state.x77[,c("Murder", "Population", "Illiteracy", "Income", "Frost")])
#fit <- lm(Murder ~ Population + Illiteracy + Income + Frost, data=states)

# Test Normality
qqPlot(df.fit,  id.method="identify", simulate=TRUE, main="Q-Q Plot")

# Test Independence of errors
durbinWatsonTest(df.fit) # significance indicates a lack of autocorrelation hence independence of errors


crPlots(df.fit) #examine plots for linearity or uncaptured relationships
ncvTest(df.fit) # Test of residuals having constant variance i.e. Homoscedasticity
spreadLevelPlot(df.fit) # look at suggested power can help to decide if a transformation is needed

vif(df.fit)
sqrt(vif(df.fit)) > 2 #if Sqrt of the VIF statistic is larger than 2 indicates a multicollinearity issue between dependents
outlierTest(df.fit)
influencePlot(df.fit, id.method="identify", main="Influence Plot",
              sub="Circle size is proportional to Cook’s distance")

#Variable selection "Forward selection"
library(MASS)
stepAIC(df.fit , selection = "forward")



# Regularisation
poly.fit <- lm(Y ~ poly(X, degree = 1), data = df)
df <- transform(df, PredictedY = predict(poly.fit))
ggplot(df, aes(x = X, y = PredictedY)) +
  geom_point() +
  geom_line()
poly.fit <- lm(Y ~ poly(X, degree = 3), data = df)
df <- transform(df, PredictedY = predict(poly.fit))
ggplot(df, aes(x = X, y = PredictedY)) +
  geom_point() +
  geom_line()
poly.fit <- lm(Y ~ poly(X, degree = 5), data = df)
df <- transform(df, PredictedY = predict(poly.fit))
ggplot(df, aes(x = X, y = PredictedY)) +
  geom_point() +
  geom_line()


x <- seq(0, 1, by = 0.01)
x1 <- x
y <- sin(2 * pi * x) + rnorm(length(x), 0, 0.1)
# using glmnet for regularisation
library(glmnet)
# glmnet neds a matrix for x
glmnet(x, y)

Call:  glmnet(x = x, y = y) 

Df   %Dev   Lambda
# Num of Coefs Non zero (not including intercept)
# %Dev is the R square for the fit
# Lambda high means higher penality for complexity
[1,]  0 0.0000 0.547500
[2,]  1 0.1009 0.498800
[3,]  1 0.1847 0.454500
[4,]  1 0.2542 0.414100
[5,]  1 0.3120 0.377300



# TO regularise we split our data into test and train
set.seed(1)         # initialize random seed for consistency
x <- seq(0, 1, by = 0.01)
y <- sin(2 * pi * x[,1]) + rnorm(length(x[,1]), 0, 0.1)

train.pct <- 0.7    # pct of data to use for training set
N <- length(x)     # total number of records 

train.index <- sample(1:N, train.pct * N)       # random sample of records (training set)


train.x <- x[train.index]       # perform train/test split
train.y <- y[train.index]       # perform train/test split

test.x <- x[-train.index]       # note use of neg index...different than Python!
test.y <- y[-train.index]       # note use of neg index...different than Python!

train.df <- data.frame(X = train.x , Y = train.y)
test.df <- data.frame(X = test.x , Y = test.y)

glmnet.fit <- with(train.df, glmnet(poly(X, degree = 10), Y))
lambdas <- glmnet.fit$lambda

performance <- data.frame()

rmse <- function(y, h)
      {
        return(sqrt(mean((y - h) ^ 2)))
      }

for (d in 1:12)
{
  poly.fit <- lm(Y ~ poly(X, degree = d), data = train.df)
  performance <- rbind(performance,
                       data.frame(Degree = d,
                                  Data = 'Training',
                                  RMSE = rmse(train.y, predict(poly.fit))))

  performance <- rbind(performance,
                     data.frame(Degree = d,
                                Data = 'Test',
                                RMSE = rmse(test.y, predict(poly.fit,
                                                            newdata = test.df))))
}

print(performance)

ggplot( performance, aes ( x = Degree , y = RMSE , linetype = Data))+
    geom_point()+
    geom_line()


# An example of an interaction
fit <- lm(mpg ~ hp + wt + hp:wt, data=mtcars)
summary(fit)
library(effects)
plot(effect("hp:wt", fit, list(wt=c(2.2,3.2,4.2))), multiline=TRUE)

