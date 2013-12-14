#if we don't have the package needed, install it
#this is crying out for some refactoring
if("jsonlite" %in% rownames(installed.packages()) == FALSE) {install.packages("jsonlite")}
if("ggplot2" %in% rownames(installed.packages()) == FALSE) {install.packages("ggplot2")}
if("splines" %in% rownames(installed.packages()) == FALSE) {install.packages("splines")}

library(ggplot2)
library(jsonlite)
library(splines)

setwd("/home/ben/Documents/GA-DS/regression-homework")


#this needs the json to be in the format [{...}] i.e. a list of objects
# if it is in the more obvious format {'k':[{...}]} then it thinks you have one observation
j <- fromJSON("workouts.json")

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
#convert date col strings into r dates
#as.Date(j$date[1], format="%b %d, %Y")
j$r.date <- sapply(j$date,  function(x){ as.Date(x, format="%b %d, %Y") })

fit <- lm(j$power.w ~  j$duration)
#summary(fit)
#plot(fit)

plot(j$duration, j$power.w)
abline(fit)

ggplot(j, aes(x=j$duration, y=j$power.w)) +
  geom_point(shape=1) +    # Use hollow circles
  geom_smooth()            # Add a loess smoothed fit curve with confidence region
