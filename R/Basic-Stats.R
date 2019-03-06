# Normal Distribution
help(pnorm)

pnorm(0, mean = 0, sd = 1) # Probability of a number being less than/left of 0
#with a distribution having 0 mean and 1 standard deviations is 50%
#> 0.5

# Probability of a number between +1 and -1 Standard deviations
pnorm(1, mean = 0, sd = 1) - pnorm(-1, mean = 0, sd = 1)
#> 0.6826895

# Probability of a number between +2 and -2 Standard deviations
pnorm(2, mean = 0, sd = 1) - pnorm(-2, mean = 0, sd = 1)
#> 0.9544997

# P1: Calculate the standard deviation for the following numbers
# 12,14,11,18,10.5,11.3,12,14,11,9
#x <- {12,14,11,18,10.5,11.3,12,14,11,9}
# mean => 12.28, sd => 2.52

pnorm(0, mean = 12.28, sd = 2.52)


