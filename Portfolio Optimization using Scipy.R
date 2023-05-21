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

# Set the start and end dates
start_date <- Sys.Date() - 5*365  # 5 years ago
end_date <- Sys.Date()  # Today

#data <- getSymbols('AAPL', from = start_date, to = end_date)
#stk_Returns <- c(NA, diff(AAPL$AAPL.Close) / lag(AAPL$AAPL.Close))

logReturns <- data.frame()

for (tic in ticker_list)
  {
  data <- getSymbols(c(tic), from = start_date, to = end_date)
  xts_obj <- list(tic)
  column_data <- xts_obj[[tic]]$Close
  
  }

  stk_ret <- diff(data$tic.Close) / lag(data$tic.Close)
  }

  self.logReturns [tic] = np.log(returns).dropna()
  }




