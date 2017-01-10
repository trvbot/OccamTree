############################################
### MAP YOUR OCCAM MODEL AS A HYPERGRAPH ###
##### Teresa Schmidt, February 8, 2016 #####
############################################

### FIRST TIME INSTALL THESE PACKAGES, SUBSEQUENT TIMES IGNORE by placing '#' in front:
#install.packages("stringr")
#install.packages("igraph")

### PASTE RA MODEL HERE (IN QUOTES): 
Model = "Pij2Cnr1Cdg:Pye0Cdg:Cdg"

### TYPE PATH TO OCCAM INPUT FILE HERE (IN QUOTES):
InputPath = "C:/Users/owner/Desktop/zsoul/DMIT/slide19 preece run 30.csv"

### RECOMMENDED: TYPE PATH TO DESIRED OUTPUT FILE LOCATION (IN QUOTES):
setwd("C:/Users/zwick/Desktop")

### OPTIONAL: NAME YOUR NETWORK (IN QUOTES):
NetworkName = "Bethesda"

### OPTIONAL: NETWORK SETTINGS:
#Do you want to ignore the variables not in your model? ("Yes" or "No")
Remove = "Yes"
#Variable color: (see http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf)
Vcolor = "mediumaquamarine"
#Variable node size:
size = 1
#Variable label size:
Vlabel = .8
#Hyperedge color:
Acolor = "red4"
#Hyperedge node size:
Asize = 2
#Hyperedge label size:
Alabel = .01

################################
library(stringr)
library(igraph)
Model <- gsub("IVI:", "", Model)
Associations <- as.data.frame(stringsAsFactors=FALSE, strsplit(Model, ":"))
Associations <- as.data.frame(stringsAsFactors=FALSE, gsub("(?!^)(?=[[:upper:]])", "-", Associations[,], perl=TRUE))

Frq = as.matrix(sapply(gregexpr("-",Associations[,]),function(Associations)if(Associations[[1]]!=-1) length(Associations) else NA))
Frq <- as.data.frame(Frq+1)
EdgeOrder = cbind(Freq=Frq, Associations=Associations)
colnames(EdgeOrder) <- c("Order", "Association")
Edges = subset(EdgeOrder, EdgeOrder[,1]==2, stringsAsFactors=FALSE)
Edges <- as.data.frame(str_split_fixed(Edges[,2], "-", 2))
colnames(Edges) <- c("Source", "Target")

Hyper = subset(EdgeOrder, EdgeOrder[,1]>2, stringsAsFactors=FALSE)
colnames(Hyper) <- c("Association", "Members")
Hyper[,2] <- as.character(Hyper[,2])
Hyper[,1] <- 1:nrow(Hyper)
s <- strsplit(Hyper$Members, split = "-")
HyperEdges = data.frame(Source = as.factor(rep(Hyper$Association, sapply(s, length))), Target = unlist(s))

Input = read.table(stringsAsFactors=FALSE, textConnection(readLines(InputPath)[grep(",1,|,2,",readLines(InputPath))]), sep=",")
Input[,] <- gsub("\t", "", as.matrix(Input[,]))
Nodes = cbind.data.frame(ID=Input$V4, Label=Input$V1, Type="variable")
Nodes[,1] <-tolower(as.character(Nodes[,1]))
simpleCap <- function(x) {paste(toupper(substring(x, 1,1)), substring(x, 2), sep="")}
Nodes <- sapply(Nodes[,], simpleCap)
Nodes <- as.data.frame(Nodes)

HyperNodes = as.data.frame(0:nrow(Hyper))
HyperNodes <- cbind.data.frame(HyperNodes, HyperNodes, "HyperEdge")
colnames(HyperNodes) <- c("ID", "Label", "Type")
HyperNodes[,1] <-as.character(HyperNodes[,1])
HyperNodes[,2] <-as.character(HyperNodes[,2])

Edgefile = rbind.data.frame(as.matrix(Edges), as.matrix(HyperEdges))
Nodefile = rbind.data.frame(Nodes, HyperNodes)
Nodefile = Nodefile[!grepl("0", Nodefile[,1]),]
if (Remove=="Yes") Nodefile <- Nodefile[grepl(paste(unique(unlist(Edgefile[,])), collapse="|"), Nodefile[,1]),]

Hypergraph = graph.data.frame(Edgefile, directed=FALSE, vertices=Nodefile[,1])
V(Hypergraph)$color <- ifelse(V(Hypergraph)$name %in% Nodes[,1], Vcolor, Acolor)
V(Hypergraph)$size <- ifelse(V(Hypergraph)$name %in% Nodes[,1], Vsize, Asize)
plot(Hypergraph, vertex.label.color="black", vertex.label.cex=ifelse(V(Hypergraph)$name %in% Nodes[,1], Vlabel, Alabel))
name=paste0(NetworkName, ".pdf")
pdf(name)
plot(Hypergraph, vertex.label.color="black", vertex.label.cex=ifelse(V(Hypergraph)$name %in% Nodes[,1], Vlabel, Alabel))
dev.off()

noquote(c("YOUR NEW FILES CAN BE RETRIEVED AT:", getwd()))
