library(stats)
library(ggplot2)
set.seed(1)

# for our first example, let's create some synthetic easy-to-cluster data
d <- data.frame()
d <- rbind(d, data.frame(x=1 + rnorm(20, 0, 0.1), y=1 + rnorm(20, 0, 0.1), label=as.factor(rep(1, each=20))))
d <- rbind(d, data.frame(x=1 + rnorm(20, 0, 0.1), y=3 + rnorm(20, 0, 0.1), label=as.factor(rep(2, each=20))))
d <- rbind(d, data.frame(x=3 + rnorm(20, 0, 0.1), y=1 + rnorm(20, 0, 0.1), label=as.factor(rep(3, each=20))))
d <- rbind(d, data.frame(x=3 + rnorm(20, 0, 0.1), y=3 + rnorm(20, 0, 0.1), label=as.factor(rep(4, each=20))))

# have a look...this looks easy enough
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=label)) + ggtitle('d -- easy clusters')

# perform clustering
result1 <- kmeans(d[,1:2], 4)

#lets compare a few cluster solutions
result12 <- kmeans(d[,1:2], 2)
d$cluster12 <- as.factor(result12$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster12)) + ggtitle('kmeans result1 -- (k=2)')

result13 <- kmeans(d[,1:2], 3)
d$cluster13 <- as.factor(result13$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster13)) + ggtitle('kmeans result1 -- (k=3)')

result14 <- kmeans(d[,1:2], 4)
d$cluster14 <- as.factor(result14$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster14)) + ggtitle('kmeans result1 -- (k=4)')

result15 <- kmeans(d[,1:2], 5)
d$cluster15 <- as.factor(result15$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster15)) + ggtitle('kmeans result1 -- (k=5)')

res.comp <- as.data.frame ( rbind(  c(2 ,result12$tot.withinss)
                  , c(3 ,result13$tot.withinss)
                  , c(4 ,result14$tot.withinss)
                  , c(5 ,result15$tot.withinss)
                    ) )

ggplot(res.comp,aes(res.comp[,1] , as.numeric(res.comp[,2]) ))+
       geom_line()
# here are the results...note the algorithm found clusters whose means are close to the true means of our synthetic clusters
result1

# plot results...we are looking good
d$cluster1 <- as.factor(result1$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster1)) + ggtitle('kmeans result1 -- success!\n(k=4)')

# suppose we repeat these steps...what do you expect to happen?
result2 <- kmeans(d[,1:2], 4)

# notice that the fit got worse!
# (eg, large decrease in between_SS / total_SS...also cluster means are not as good as before)
result2

# and this scatterplot shows that something is obviously not right...what happened?
d$cluster2 <- as.factor(result2$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster2)) + ggtitle('kmeans result2 -- trouble\n(k=4)')

# this instability is a result of the random initial seeds that the clustering algorithm uses
# if two initial seeds begin in the same cluster, then the algorithm will have difficulty finding all the clusters
# (in particular, the cluster which doesn't contain an initial seed will be difficult to identify)
# (note that in any case, the algorithm will still return exactly as many clusters as you asked it to!)

# so how can we create a more stable clustering fit? by repeating the fit several times and taking an average
# (this is effectively an ensemble clustering technique...we will talk about ensemble methods in more detail later)
result3 <- kmeans(d[,1:2], 4, nstart=10)
result3
d$cluster3 <- as.factor(result3$cluster)
ggplot(d, aes(x=x, y=y)) + geom_point(aes(colour=cluster3)) + ggtitle('kmeans result3 -- stable convergence\n(k=4, nstart=10)')

#

# what happens if we introduce a new length scale into the problem? how many clusters are in the dataset now?
d2 <- rbind(d[,1:3], data.frame(x=1000+rnorm(20,0,50), y=1000+rnorm(20,0,50), label=as.factor(rep(5, each=20))))
ggplot(d2, aes(x=x, y=y)) + geom_point(aes(colour=label)) + ggtitle('d2 -- multiple length scales')

# as you can see, things go haywire...recall that clustering results are kind of a heuristic
# (in particular, not invariant to a change in units!)
result4 <- kmeans(d2[,1:2], 5, nstart=10)
d2$cluster4 <- as.factor(result4$cluster)
ggplot(d2, aes(x=x, y=y)) + geom_point(aes(colour=cluster4)) + ggtitle('kmeans result4 -- trouble\n(k=5, nstart=10)')

#Lets standardis the variables and see what happens
ds <- data.frame(scale(d2[,1:2],center =TRUE , scale=TRUE))
result5 <- kmeans(ds, 4, nstart=10)
ds$cluster4 <- as.factor(result5$cluster)
ggplot(ds, aes(x=x, y=y)) + geom_point(aes(colour=cluster4)) + ggtitle('kmeans result5 -- trouble\n(k=5, nstart=10)')


# now let's try k-means clustering with the iris dataset
iris.result <- kmeans(iris[,1:4], 3)

# look at clustering results...you can already tell something is up
iris.result$cluster

# combine clustering results with input data (as factor)

# let's look at the scatterplots of clustering results & true labels together (using package gridExtra)
# first install this guy
library(gridExtra)

# now create our two scatterplots...note that ggplot returns an *object* which can be stored!
iris2 <- cbind(iris, cluster=as.factor(iris.result$cluster))
p1 <- ggplot(iris2, aes(x=Sepal.Width, y=Petal.Width)) + geom_point(aes(colour=cluster)) + ggtitle('clustering results')
p2 <- ggplot(iris, aes(x=Sepal.Width, y=Petal.Width)) + geom_point(aes(colour=Species)) + ggtitle('true labels')

# so what is going on here?
grid.arrange(p1, p2)

# although clustering is a unsupervised learning technique it does an OK job at matching known groups