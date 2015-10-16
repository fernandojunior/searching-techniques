# http://stackoverflow.com/questions/26553321/how-do-i-program-this-dijkstra-shortest-distance-algorithm-in-r

install.packages("igraph")
library(igraph)

distances = read.csv('brazil58.csv', header = FALSE, sep = ",")
# distances = apply(distances, 1, as.integer)
g <- graph.adjacency(distances, weighted=TRUE)


size = nrow(distances)

out = matrix(NA, nrow=size, ncol=3)

for(i in 1:size)
    for(j in 1:size){
        print(paste(1, j, distances[i, j]))
        out = rbind(out, c(i, j, distances[i, j]))
    }

out = as.data.frame(out)
names(out) = c("start_id","end_id","cost")

g <- graph.data.frame(out, directed=FALSE)

(tmp2 = get.shortest.paths(g, from='1', to='57', mode='all',weights=E(g)$cost))

df2 = rbind(
c(234,235,21.6),
c(234,326,11.0),
c(235,241,14.5),
c(326,241,8.2),
c(241,245,15.3),
c(234,245,38.46))


for (n in 1:iter)
  out[n,] <- c(n, 2*n, n+1)
