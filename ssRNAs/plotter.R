#!/usr/bin/env Rscript
library(R4RNA)

x <- readVienna("my_structure.dbn")
x <- expandHelix(x)

pdf("full_5000nt_arc.pdf", width = 40, height = 10)
plotHelix(x, line = TRUE, arrow = FALSE)
dev.off()
