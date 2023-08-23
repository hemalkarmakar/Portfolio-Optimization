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
library(tidyverse)
library(quantmod)

# Import tickers from csv file
tickerfilepath <- 'https://raw.githubusercontent.com/hemalkarmakar/Portfolio-Optimization/main/Portfolio%20ticker%20list.csv'
tickerDF <- read.csv(tickerfilepath)
ticker_list <- as.list(tickerDF)

# Set the start and end dates
start_date <- Sys.Date() - 5*365  # 5 years ago
end_date <- Sys.Date()  # Today


for (tic in ticker_list)
  {
  # Get historical stock price data
  data <- BatchGetSymbols(tic, from = start_date, to = end_date)}
  
  # Calculate daily returns
  returns[, tic] <- (data) / lag((data))
  logReturns[, tic] <- log(returns)
  }
