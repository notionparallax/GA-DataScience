library(ggplot2)
library(psych)
library(Hmisc)

# Import Data
hw <- read.table('YOUR_DIRECTORY/01_heights_weights_genders.csv', header=TRUE, sep=",")

#initial look data imported correctly
str(hw)
length(hw)
dim(hw)
class(hw)
summary(hw)
# Careful describe is a function in both psych and Hmisc -- Hint find out how toreference which one you want!
describe(hw)

desc.HW <-describe(hw)
str(desc.HW)

#Some plots to explore the data Consider saving initial plot as an object that you then build upon
ggplot(hw , aes(x = Height)) + geom_histogram(binwidth=1)
ggplot(hw , aes(x = Height , fill = Gender)) + geom_density()

ggplot(hw , aes(x = Weight)) + geom_histogram(binwidth=1)
ggplot(hw , aes(x = Weight , fill = Gender)) + geom_density()
ggplot(hw , aes(x = Weight , fill = Gender)) + geom_density() + facet_grid(Gender~.)

ggplot(hw , aes(x = Height, y = Weight)) + geom_point()
ggplot(hw , aes(x = Height, y = Weight)) + geom_point() + geom_smooth()
ggplot(hw , aes(x = Height, y = Weight , fill = Gender)) + geom_point() + geom_smooth()
ggplot(hw , aes(x = Height, y = Weight , color = Gender)) + geom_point() + geom_smooth()
