install.packages("jsonlite")
library(jsonlite)


json_file <- fromJSON("regression-homework/workouts.json")

json_file <- lapply(json_file, function(x) {
  x[sapply(x, is.null)] <- NA
  unlist(x)
})
