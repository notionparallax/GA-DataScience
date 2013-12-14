#if we don't have the package needed, install it
if("jsonlite" %in% rownames(installed.packages()) == FALSE) {install.packages("jsonlite")}

library(jsonlite)

setwd("/home/ben/Documents/GA-DS/regression-homework")


#this needs the json to be in the format [{...}] i.e. a list of objects
# if it is in the more obvious format {'k':[{...}]} then it thinks you have one observation
json_file <- fromJSON("workouts.json")
