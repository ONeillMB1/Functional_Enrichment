#!/usr/bin/Rscript --vanilla

get_fisher <- function(df){
  mat <- matrix(as.numeric(df[c(2:5)]), ncol=2)
  f <- fisher.test(as.table(mat))
  return(c(df[1], f$p.value))
}

require("stats")
require("tools")

for (file.name in list.files()) {
  print(file.name)
  name <- file_path_sans_ext(file.name)
  print(name)
  dat <- read.table(file.name,header=F,sep="\t")
  fishers <- t(apply(dat, 1,  get_fisher))
  tt=data.frame(fishers)
  tt[,2]=as.numeric(as.matrix(tt[,2]))
  tt$qval=p.adjust(tt$V2, method="fdr")
  write.table(tt, file=paste(name, "_qval.txt", sep=""), append=FALSE, sep="\t", eol="\n", col.names=FALSE, row.names=FALSE, quote=FALSE, qmethod="double")
  tt$sample=name
  ind= tt[,3] < 0.05
  sig <- (as.matrix(tt[ind,]))
  print(sig)
  write.table(sig, file=paste(name, "_qvalsig.txt", sep=""), append=TRUE, sep="\t", eol="\n", col.names=FALSE, row.names=FALSE, quote=FALSE, qmethod="double")
}
