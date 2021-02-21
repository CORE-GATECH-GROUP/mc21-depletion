#!/usr/bin/env bc
# Script to show effect of increasing / decreasing step size
# Simpler than run time comparisons for conference paper as would require
# introducing and verifying framework reference solution. That will
# be shown in upcoming journal paper and has been done in thesis
scale=6
prelim=10
final=300
# number of transport solutions in predictor-corrector reference
# no corrector at EOL solution
pc=(prelim + final) * 2 - 1  
# number of transport solutions in 2.5, 5, and 10 day predictor
s2_5=prelim + final / 2.5
s5=prelim + final / 5
s10=prelim + final / 10
r5=(s5/pc - 1) * 100
print "reduction from 5 day to pc: ", r5, " %\n"
r10=(s10/pc - 1) * 100
print "reduction from 10 day to pc: ", r10, " %\n"
dec2_5=s2_5/s5 - 1
print "increase halving steps 5 -> 2.5: ", dec2_5, "\n"
quit
