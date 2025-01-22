library(TreeDist)
library(ape)
library(progress)

newick_g1 <- readLines('g1.data')
newick_g2 <- readLines('g2.data')
g1 <- lapply(newick_g1,function(line){
    read.tree(text=line)
})
g2 <- lapply(newick_g2,function(line){
    read.tree(text=line)
})

calculate_distances <- function(g1, g2, distance) {
    d0 <- c() 
    d1 <- c()  
    
    # Combinaciones internas de g1
    if (length(g1) > 1) {
        for (i in 1:(length(g1) - 1)) {
            for (j in (i + 1):length(g1)) {
                if (distance == "PID") {
                    dist <- TreeDist::PhylogeneticInfoDistance(g1[[i]], g1[[j]])
                }
                if (distance == "CID") {
                    dist <- TreeDist::ClusteringInfoDistance(g1[[i]], g1[[j]])
                }
                if (distance == "MSD") {
                    dist <- TreeDist::MatchingSplitDistance(g1[[i]], g1[[j]])
                }
                d0 <- c(d0, dist)
            }
        }
    }
    
    for (t1 in g1) {
        for (t2 in g2) {
            if (distance == "PID") {
                dist <- TreeDist::PhylogeneticInfoDistance(t1, t2)
            }
            if (distance == "CID") {
                dist <- TreeDist::ClusteringInfoDistance(t1, t2)
            }
            if (distance == "MSD") {
                dist <- TreeDist::MatchingSplitDistance(t1, t2)
            }
            d1 <- c(d1, dist)
        }
    }
    
    mu_0 <- mean(d0)
    sigma_0 <- sd(d0)
    d1_hat <- (d1 - mu_0) / sigma_0
    return(d1_hat)
}

writeLines(as.character(calculate_distances(g1=g1,g2=g2,distance ="CID")),'CID_values.txt')
writeLines(as.character(calculate_distances(g1=g1,g2=g2,distance ="PID")),'PID_values.txt')
writeLines(as.character(calculate_distances(g1=g1,g2=g2,distance ="MSD")),'MSD_values.txt')