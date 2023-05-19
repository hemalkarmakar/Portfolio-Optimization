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
library(quantmod)

# Import tickers from csv file
tickerfilepath <- 'https://raw.githubusercontent.com/hemalkarmakar/Portfolio-Optimization/main/Portfolio%20ticker%20list.csv'
tickerDF <- read.csv(tickerfilepath)
ticker_list <- as.list(tickerDF)

#getSymbols("AAPL", from = "2018-05-19", to = "2023-05-19")

# Set the start and end dates
start_date <- Sys.Date() - 5*365  # 5 years ago
end_date <- Sys.Date()  # Today

for (tic in ticker_list)
  {
  data = getSymbols(tic, from = start_date, to = end_date)}
  
  returns = data/data.shift(1)
  self.logReturns [tic] = np.log(returns).dropna()
  }


