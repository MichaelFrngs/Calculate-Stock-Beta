#To install on pc, type into terminal: pip install pandas-datareader
import pandas_datareader.data as web #This is the pandas data reading API. Lets you read from a website or a source.
import datetime as dt
import pandas as pd
import math
import numpy as np

def Pull_Daily_Prices(ticker, start_year, start_month, end_year, end_month):
    #Starting date for the desired data
    start = dt.datetime(start_year, start_month, 1)
    #Ending date for the desired data
    end = dt.datetime(end_year, end_month, 1)
    #Pulls daily stock data for the desired ticker and desired dates
    Stock_Data = web.DataReader(ticker, 'iex', start, end).reset_index()   
    #Changes the date column from a string type variable to datetime type. Allows use of dt.methods
    Stock_Data['date'] = pd.to_datetime(Stock_Data['date'])
    #Initiate Variable. We'll fill it with the stock data mid-loop.
    DailyStock_Data = pd.DataFrame()

    #Initiate counters
    i=0
    indexNum = 0
    #Creates monthly data by filtering the daily data.
    while i < Stock_Data.shape[0]: #Counts the number of rows in the stock_data dataframe.
        try:
            print(Stock_Data["date"][indexNum])
            #Creates the dataframe by iteratively appending each row.
            DailyStock_Data = DailyStock_Data.append(pd.DataFrame([Stock_Data.iloc[indexNum,]]),ignore_index=True)
            #Market is open 5 days a week. Aprox 4.34 weeks per month. Result is about 22 market days per month. We only want to select one day a month from the data.
            indexNum = indexNum + 1 
            i=i+1
        except:
            print("End")
            break
    #gives us last trading day of each month
    last_day_of_month = pd.bdate_range(start, end, freq='BM')
    #Only retains matches in the daily stock data
    MonthlyStock_Data = DailyStock_Data[DailyStock_Data["date"].isin(last_day_of_month)]
    
     #Creates dynamically named global variable with end results. Allows for ease of use elsewhere. Format is #Data_TICKER
    globals()["Data_%s" %ticker] = MonthlyStock_Data
    return(MonthlyStock_Data)
    
    #Test out the function. Let's pull the data. The parameters are: (ticker, start_year, start_month, end_year, end_month)
Index = Pull_Daily_Prices("SPY",2016,4,2019,4)
Stock = Pull_Daily_Prices("AAPL",2016,4,2019,4)

#Let's display some of the data
print(Index["close"].head())
print(Stock["close"].head())

def evaluate_beta(Index_Prices,Stock_Prices):
    IndexReturns = Index_Prices.pct_change().dropna() #Drops the first term.
    StockReturns = Stock_Prices.pct_change().dropna() #Drops the first term.
    Covariance_yx = np.cov(IndexReturns,StockReturns)[0,1]*12 #Multiplied by 12 to annualize
    Variance_x = np.var(IndexReturns)*12 #Multiplied by 12 to annualize
    Beta = Covariance_yx/Variance_x
    return(Beta)
    
    
 #Evaluates Beta
evaluate_beta(Index["close"],Stock["close"])
