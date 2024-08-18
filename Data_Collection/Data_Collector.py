import yfinance as yf
import pandas_datareader as pdr
import datetime
from alpha_vantage.timeseries import TimeSeries
import time
import os
import pandas as pd
from datetime import datetime, timedelta


def yFinanceTrial(ticker_symbol): #user-friendly and does not require an API key.
    # Define the ticker symbol
    #ticker_symbol = 'AAPL'

    # Get the data
    ticker_data = yf.Ticker(ticker_symbol)

    # Get historical market data
    #ticker_df = ticker_data.history(period='1mo', start='2023-07-01', end='2024-08-01')

    ticker = ticker_data.history(period="1d", interval="1m", auto_adjust=False)
    print(ticker)

    # Display the data
    #print(ticker_df)

    # Get basic information
    info = ticker.info

    # Access specific data
    current_price = info['currentPrice']
    market_cap = info['marketCap']
    sector = info['sector']

    #print(f"Current Price: {current_price}")
    #print(f"Market Cap: {market_cap}")
    #print(f"Sector: {sector}")
    consolidate_data = sector, current_price, market_cap
    print(consolidate_data)
    return str(consolidate_data)

def write_df_to_csv(df, file_path, index=False):
    """
    Writes the given DataFrame to a CSV file.

    Parameters:
    df (pd.DataFrame): The DataFrame to write to CSV.
    file_path (str): The path to the CSV file to create.
    index (bool): Whether to write the DataFrame index to the file. Defaults to False.
    """
    df.to_csv(file_path, index=index)

class Store_Data:
    def Append(df, file_loc):
        df.to_csv(file_loc, mode='a', index=False, header=False)

        with open(file_loc, 'a') as csv_store:
            df.write()
            current_time_utc = time.gmtime()
            formatted_time_utc = time.strftime("%Y-%m-%d %H:%M:%S", current_time_utc)
            line_mark =  f"----------------------------------------{formatted_time_utc}----------------------------------------\n"
            
            try:
                csv_store.write(line_mark)
            except Exception as e:
                print(f"~~~~~~~~~~~~~~~~~~~~~~`the problem is {e}")

    def Write(df, file_loc):
        #df.to_csv(file_loc, columns=['Column1', 'Column2'], index=False)
        #df.to_csv(file_loc, sep='\t', index=False)

        df.to_csv(file_loc, header=True, index=False)  # Include header
        #df.to_csv(file_loc, header=False, index=False)  # Exclude header

        df.to_csv(file_loc, index=True)   # Include index
        #df.to_csv(file_loc, index=False)  # Exclude index

        df.to_csv(df, mode='a', index=False, header=False)

        #df.to_csv('output.csv', na_rep='NA', index=False)  # Replace NaN with 'NA'

        # lambda modifications
        # Example: Format date columns
        #df['DateColumn'] = df['DateColumn'].dt.strftime('%Y-%m-%d')

        # Example: Format numerical columns
        #df['Amount'] = df['Amount'].apply(lambda x: f"${x:,.2f}")

        #df.to_csv(file_loc, index=False)
        
        #df.to_csv(file_loc, index=False)
        
def Data_From_Ticker_List():
    location = '/Users/adam/Documents/GitHub/Linear_Regression/Data_Collection/list_of_tickers.txt'
    # Open the file in read mode
    with open(location, 'r') as file:
        # Iterate through each line in the file
        for line in file:                                       #this part is the part not working right now
            # Process the line (e.g., print it)
            #time.sleep(5)
            try: 
                line_parsed = line.strip()
                Historical_data(line_parsed) #feeding the ticker symbol into the data collector
            except Exception as e:
                print(f"An error occurred: {e}")
            
def Historical_data(ticker_symbol):
    ticker_data = yf.Ticker(ticker_symbol)

    # Get historical market data
    #ticker_df = ticker_data.history(period='1mo', start='2023-07-01', end='2024-08-01')

    periods = ["1d", "5d", '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    granularity_options = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    
    #periodInput = "5d"
    #granularity = "1m"

    period_to_granularity = {
    "1d": ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d"],
    "5d": ["5m", "15m", "30m", "60m", "90m", "1h", "1d"],
    "1mo": ["1d", "5d", "1wk", "1mo"],
    "3mo": ["1d", "5d", "1wk", "1mo", "3mo"],
    "6mo": ["1d", "5d", "1wk", "1mo", "3mo"],
    "1y": ["1d", "5d", "1wk", "1mo", "3mo"],
    "2y": ["1d", "5d", "1wk", "1mo", "3mo"],
    "5y": ["1d", "5d", "1wk", "1mo", "3mo"],
    "10y": ["1d", "5d", "1wk", "1mo", "3mo"],
    "ytd": ["1d", "5d", "1wk", "1mo"],
    "max": ["1d", "5d", "1wk", "1mo", "3mo"]
    }

    for periodInput in period_to_granularity.keys():
        for granularity in period_to_granularity[periodInput]:
            # Fetch historical market data
            ticker = ticker_data.history(period=periodInput, interval=granularity, auto_adjust=False)

            # Check if data was returned (i.e., the combination is valid)
            if ticker.empty:
                print(f"No data for period {periodInput} with granularity {granularity}. Skipping...")
                continue  # Skip to the next iteration if no data is returned

            # Extract the start and end dates from the DataFrame's index
            start_date = ticker.index.min()
            end_date = ticker.index.max()

            # Get the current date without time
            date_of_collection = datetime.now().date()

            # Directory path
            storage_dir = f"{os.getcwd()}/Data_Collection/Storage_Location/{ticker_symbol}/{periodInput}_at_{granularity}/{date_of_collection}/"
            os.makedirs(storage_dir, exist_ok=True)

            # File path for saving data
            file_loc = f"{storage_dir}/{ticker_symbol}_Data_{periodInput}_at_{granularity}.csv"

            # Write data to CSV
            try:
                ticker.to_csv(file_loc)
                print(f"Data saved to {file_loc}")
            except Exception as e:
                print(f"Failed to save data: {e}")

    

Data_From_Ticker_List()