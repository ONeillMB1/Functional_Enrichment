get_cutoffs <- function(indat){
  dat <- na.omit(indat)
  all <- as.character(dat$V1)
  print(length(all))
  cutoff <- quantile(dat$mean, c(0.05, 0.95), na.rm=TRUE)
  print(cutoff[1])
  print(cutoff[2])
  ind.bot <- dat[,12] < cutoff[1]
  ind.top <- dat[,12] > cutoff[2]
  top <- as.character(dat$V1[ind.top])
  bottom <- as.character(dat$V1[ind.bot])
  write(bottom, file= paste(c(deparse(substitute(indat))), "_bot.txt", sep = ""), ncolumns = 1)
  write(top, file= paste(c(deparse(substitute(indat))), "_top.txt", sep = ""), ncolumns = 1)
  write(all, file= paste(c(deparse(substitute(indat))), "_all.txt", sep = ""), ncolumns = 1)
} 

get_cutoffs(c2)


make_files <- function(indat){
  dat <- na.omit(indat)
  all <- as.character(dat$V1)
  print(length(all))
  cutoff <- quantile(dat$diff, c(0.05, 0.95), na.rm=TRUE)
  print(cutoff[1])
  print(cutoff[2])
  ind.bot <- dat[,7] < cutoff[1]
  ind.top <- dat[,7] > cutoff[2]
  top <- as.character(dat$V1[ind.top])
  bottom <- as.character(dat$V1[ind.bot])
  write(bottom, file= paste(c(deparse(substitute(indat))), "_bot.txt", sep = ""), ncolumns = 1)
  write(top, file= paste(c(deparse(substitute(indat))), "_top.txt", sep = ""), ncolumns = 1)
  write(all, file= paste(c(deparse(substitute(indat))), "_all.txt", sep = ""), ncolumns = 1)
} 

make_files(b12)