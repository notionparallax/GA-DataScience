install.packages("jsonlite")
library(jsonlite)

jsonFile <-"workouts.json"
data1 <- fromJSON(file = "workouts.json")
