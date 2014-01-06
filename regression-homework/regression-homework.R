#if we don't have the package needed, install it
#this is crying out for some refactoring
if("jsonlite" %in% rownames(installed.packages()) == FALSE) {install.packages("jsonlite")}
if("ggplot2" %in% rownames(installed.packages()) == FALSE) {install.packages("ggplot2")}
if("splines" %in% rownames(installed.packages()) == FALSE) {install.packages("splines")}
if("psych" %in% rownames(installed.packages()) == FALSE) {install.packages("psych")}

library(ggplot2)
library(jsonlite)
library(splines)
library(psych)

setwd("/home/ben/Documents/GA-DS/regression-homework")


#this needs the json to be in the format [{...}] i.e. a list of objects
# if it is in the more obvious format {'k':[{...}]} then it thinks you have one observation
j <- fromJSON("workouts.json")

summary(j)
describe(j)
#Error in if (inherits(X[[j]], "data.frame") && ncol(xj) > 1L) X[[j]] <- as.matrix(X[[j]]) : missing value where TRUE/FALSE needed

# For some reason it puts all the markers into the first obs, 
# it doesn't matter because marker isn't needed, but in future 
# this is going to be a problem
j$marker <- NULL

#rename the columns
#existing:       "sessionId"  "name"  "date"  "x"         "y"      "color" 
colnames(j) <- c("sessionId", "name", "date", "duration", "power", "color" )

#remove colour too, not useful
j$color <- NULL

#### data processing ####
fpsTOw <- 1.355817948
j$power.w <- sapply(j$power,  function(x){ x * fpsTOw })
j$power.w.log <- sapply(j$power,  function(x){ log(x) })
j$power.w.sqrt <- sapply(j$power,  function(x){ sqrt(x) })
#convert date col strings into r dates
#as.Date(j$date[1], format="%b %d, %Y")
j$r.date <- sapply(j$date,  function(x){ as.Date(x, format="%b %d, %Y") })

fit <- lm(j$power.w ~  j$duration)

plot(j$duration, j$power.w)
myLM <- lm(j$duration ~ poly(j$power.w, 4, raw=TRUE))
points(j$duration, predict(myLM), type="l", col="red", lwd=2)

poly.fit <- lm(j$power.w ~ poly(j, degree = 3), data = j)
#summary(fit)
plot(fit)

#This page was helpful
#http://www.r-bloggers.com/polynomial-regression-techniques/

plot(j$duration, j$power.w)
abline(myLM)

ggplot(j, aes(x=j$duration, y=j$power.w.log)) +
          geom_point(shape=1)+      # Use hollow circles
          geom_smooth(method=lm)+   # Add linear regression line 
          stat_smooth(method="lm", 
                      se=TRUE, 
                      fill=NA,                      
                      formula=y ~ poly(x, 3, raw=TRUE),
                      colour="red",
                      fullrange=TRUE #should the fit span the full range of the plot, or just the data
                      )

