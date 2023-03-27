'''
Name: Hemal Karmakar
- Oklahoma State University
- Master of Science in Qunatitative Finance
- hemal.karmakar@okstate.edu
'''

'''
This python class constructs portfolio of :
        - maximum Sharpe ratio,
        - minimum variance,
        - minimum risk at a target return level,
        - maximum Sharpe ratio at a target risk level &
        - efficnet frontier.     
'''

# Import libraries 
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import numpy as np

# Import tickers from csv file
tickerfilepath = 'https://raw.githubusercontent.com/hemalkarmakar/Portfolio-Optimization/main/Portfolio%20ticker%20list.csv'
tickerDF = pd.read_csv(tickerfilepath)
ticker_list = tickerDF.stack().tolist()

class PortfolioOptimization(object):  
    
    def __init__(self):
        
        # Daily return calculation
        self.logReturns = pd.DataFrame()
        
        for tic in ticker_list:
            data = yf.Ticker(tic).history('5y', interval='1d').Close
            returns = data/data.shift(1)
            self.logReturns [tic] = np.log(returns).dropna()
        
        # Annualized covariance, average return, & risk free rate
        self.covar = pd.DataFrame.cov(self.logReturns)*252
        self.mu = self.logReturns.mean()*252
        self.rf = (yf.Ticker('^TNX').history('5y').Close.mean())/100
        
        # Initial weight vector
        equalW = 1/len(self.logReturns.columns)
        self.w0 = []
        self.w0.extend([equalW for i in range(len(self.logReturns.columns))])

        # Allowable asset allocation range (-ve indicates short sales)
        bound = (-1.0, 1.0)
        self.bounds = (bound, ) * len(self.logReturns.columns)
        
        # Constraint: weights sum to 1
        self.weightSum1 = ({'type':'eq', 'fun': self.WeightSum})

    # Constriant: weights sum to 1
    def WeightSum(self, w):
        return np.sum(w)-1
    
    # Portfolio return calculation
    def Rp(self, w):
        w = np.array(w)
        Rw = np.sum(self.mu * w)
        return Rw
    
    # Portfolio risk calculation
    def SigmaP(self, w):
        w = np.array(w)
        sigma2w = np.sqrt( np.dot(w.T, np.dot(self.covar, w)) )
        return sigma2w
    
    # Minimize negative Sharpe ratio
    def NegativeSharpe(self, w):
        SharpeRatio = (self.Rp(w) - self.rf) / self.SigmaP(w)
        return -1*SharpeRatio
    
    # Show asset allocation in a diverging bar chart
    def WeightsDivergenceChart(self):
        x = self.weights.loc[:, ['Weights']]
        self.weights['Weights_z'] = (x - x.mean())/x.std()
        self.weights['colors'] = ['red' if x < 0 else 'green' for x in self.weights['Weights']]
        self.weights.sort_values('Weights_z', inplace=True)
        self.weights.reset_index(inplace=True)

        plt.figure(facecolor='lavender', figsize=(14,10), dpi= 80)
        plt.hlines(y=self.weights.index, color=self.weights['colors'], xmin=0, 
                   xmax=self.weights['Weights_z'], alpha=0.6, linewidth=8)
        
        plt.gca().set(ylabel='$Tickers$', 
                      xlabel='Divergence of the Weights; Red = Short, Green = Long')
        
        plt.yticks(self.weights.index, self.weights.Tickers, fontsize=10)
        plt.title('Diverging Bars of Asset Allocation', fontdict={'size':15})
        plt.grid(linestyle='--', alpha=0.5)
        plt.show()
    
    #--------------------------------------------------------------------------
    ''' Portfolio of Maximum Sharpe Ratio '''
    #--------------------------------------------------------------------------       
    def Portfolio_Maximum_Sharpe(self):
        self.MaximizeSharpe = minimize(self.NegativeSharpe, self.w0, 
                                               method = 'SLSQP', 
                                               bounds = self.bounds, 
                                               constraints = self.weightSum1)
        self.weights = pd.DataFrame()
        self.weights['Tickers'] = ticker_list
        self.weights['Weights'] = pd.DataFrame(self.MaximizeSharpe.x)        
        print('\nSharpe Ratio: ', np.round((-1*self.MaximizeSharpe.fun),2))
        print('Portfolio Return: ', "{:.2%}".format(self.Rp(self.MaximizeSharpe.x)))
        print('Portfolio Risk: ', "{:.2%}".format(self.SigmaP(self.MaximizeSharpe.x)))
        print('Asset Allocation:\n', np.round(self.MaximizeSharpe.x, 5))
        self.WeightsDivergenceChart()
        
    #--------------------------------------------------------------------------
    ''' Portfolio of lowest risk'''
    #--------------------------------------------------------------------------    
    def Portfolio_Minimum_Risk(self):
        self.LowestRisk = minimize(self.SigmaP, self.w0, 
                                            method = 'SLSQP', 
                                            bounds = self.bounds, 
                                            constraints = self.weightSum1)
        self.weights = pd.DataFrame()
        self.weights['Tickers'] = ticker_list
        self.weights['Weights'] = pd.DataFrame(self.LowestRisk.x)
        print('Portfolio Return: ', "{:.2%}".format(self.Rp(self.LowestRisk.x)))
        print('Portfolio Risk: ', "{:.2%}".format(self.SigmaP(self.LowestRisk.x)))       
        print('Asset Allocation:\n', np.round(self.LowestRisk.x, 5))
        self.WeightsDivergenceChart()
        
    #--------------------------------------------------------------------------
    ''' Portfolio with target Expected Return '''
    #--------------------------------------------------------------------------
    def Portfolio_Target_Return(self, target_return): 
        constraints = ({'type':'eq', 'fun': self.WeightSum}, 
                       {'type':'eq', 'fun': lambda w: self.Rp(w) - target_return})
            
        self.TargetReturn = minimize(self.SigmaP, self.w0, 
                                              method = 'SLSQP', 
                                              bounds = self.bounds, 
                                              constraints = constraints)
        self.weights = pd.DataFrame()
        self.weights['Tickers'] = ticker_list
        self.weights['Weights'] = pd.DataFrame(self.TargetReturn.x)
        print('Portfolio Return: ', "{:.2%}".format(self.Rp(self.TargetReturn.x)))
        print('Portfolio Risk: ', "{:.2%}".format(self.SigmaP(self.TargetReturn.x)))        
        print(f'Asset Allocation with {target_return*100} % target return:\n', 
              np.round(self.TargetReturn.x, 5))
        self.WeightsDivergenceChart()
        
    #--------------------------------------------------------------------------
    ''' Portfolio with a target volatility that maximizes the Sharpe Ratio'''
    #--------------------------------------------------------------------------   
    def Portfolio_Target_Volatility(self, target_risk):
        constraints = ({'type':'eq', 'fun': self.WeightSum}, 
                       {'type':'eq', 'fun': lambda w: self.SigmaP(w) - target_risk})
        
        self.TargetVolatility = minimize(self.NegativeSharpe, self.w0, 
                                                  method = 'SLSQP', 
                                                  bounds=self.bounds, 
                                                  constraints = constraints)
        self.weights = pd.DataFrame()
        self.weights['Tickers'] = ticker_list
        self.weights['Weights'] = pd.DataFrame(self.TargetVolatility.x) 
        print('\nSharpe Ratio: ', np.round((-1*self.TargetVolatility.fun),2))
        print('Portfolio Return: ', "{:.2%}".format(self.Rp(self.TargetVolatility.x)))
        print('Portfolio Risk: ', "{:.2%}".format(self.SigmaP(self.TargetVolatility.x)))        
        print(f'Asset Allocation with {target_risk*100} % target risk:\n', 
              np.round(self.TargetVolatility.x, 5))        
        self.WeightsDivergenceChart()

    #--------------------------------------------------------------------------
    ''' Efficient forntier'''
    #--------------------------------------------------------------------------      
    def Portfolio_Efficient_Frontier(self):
        
        # Generate a set of risk-return combination and their optimal weights
        target_returns = np.linspace(-0.08,0.25,50)
        volatilities = []
        
        for r in target_returns:            
            constraints = ({'type':'eq', 'fun': self.WeightSum}, 
                           {'type':'eq', 'fun': lambda w: self.Rp(w) - r})
            
            optimalRiskPortfolio = minimize(self.SigmaP, self.w0, 
                                            method = 'SLSQP', 
                                            bounds = self.bounds, 
                                            constraints = constraints)           
            volatilities.append(optimalRiskPortfolio['fun'])
              
        # Plot the efficient frontier 
        plt.figure(facecolor='lavender', figsize=(14,10), dpi= 80)
        plt.plot(volatilities, target_returns, color='m')
        plt.title('Portfolio Efficient Frontier (Short Sales Allowed)')
        plt.xlabel('Volatility (per year)')
        plt.ylabel('Return (per year)')
        plt.show()
