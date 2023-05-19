# Name: Hemal Karmakar
# - Oklahoma State University
# - Master of Science in Quantitative Finance
# - hemal.karmakar@okstate.edu

# This R class constructs portfolio of :
#         - maximum Sharpe ratio,
#         - minimum variance,
#         - minimum risk at a target return level,
#         - maximum Sharpe ratio at a target risk level &
#         - efficient frontier.

# Import libraries
library(purrr)

# Import tickers from csv file
tickerfilepath <- 'https://raw.githubusercontent.com/hemalkarmakar/Portfolio-Optimization/main/Portfolio%20ticker%20list.csv'
tickerDF <- read.csv(tickerfilepath)
ticker_list <- replace(tickerDF, tickerDF == "", NaN)


