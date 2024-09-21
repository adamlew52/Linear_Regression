import yfinance as yf
import pandas_datareader as pdr
import datetime
from alpha_vantage.timeseries import TimeSeries
import time
import os
import pandas as pd
from datetime import datetime, timedelta
import json
import sys




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
            
def print_loading_bar(ticker_frame, ticker_symbol, iteration, total, length=40):
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    bar = '#' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r[{bar}] {ticker_frame} data collection is {percent:.2f}% Complete ({ticker_symbol})')
    sys.stdout.flush()

def Historical_data(ticker_symbol):
    ticker_data = yf.Ticker(ticker_symbol)

    periods = ["1d", "5d", '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    granularity_options = ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"]
    
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

    total_combinations = sum(len(granularities) for granularities in period_to_granularity.values())
    count = 0

    metadata_list = []

    for periodInput in period_to_granularity.keys():
        for granularity in period_to_granularity[periodInput]:
            # Fetch historical market data
            ticker = ticker_data.history(period=periodInput, interval=granularity, auto_adjust=False)

            if ticker.empty:
                print(f"\nNo data for period {periodInput} with granularity {granularity}. Skipping...")
                count += 1
                print_loading_bar(ticker_symbol, ticker_symbol, count, total_combinations)
                continue

            ticker = ticker.sort_index()

            start_date = ticker.index.min()
            end_date = ticker.index.max()
            date_of_collection = datetime.now().date()

            ticker['collection_date'] = date_of_collection
            ticker['period'] = periodInput
            ticker['granularity'] = granularity

            #print(f"\nPeriod: {periodInput}, Granularity: {granularity}")
            #print(f"Start Date: {start_date}")
            #print(f"End Date: {end_date}")
            #print(ticker.head())
            #print(ticker.tail())

            ticker_frame = f"{periodInput}_at_{granularity}"

            storage_dir = f"{os.getcwd()}/Data_Collection/Storage_Location/{ticker_frame}/{date_of_collection}/"
            os.makedirs(storage_dir, exist_ok=True)

            file_loc = f"{storage_dir}/{ticker_symbol}_Data_{ticker_frame}.csv"

            try:
                ticker.to_csv(file_loc)
                #print(f"Data saved to {file_loc}")

                metadata_list.append({
                    'file_location': file_loc,
                    'collection_date': str(date_of_collection),
                    'start_date': str(start_date),
                    'end_date': str(end_date),
                    'period': periodInput,
                    'granularity': granularity
                })
            except Exception as e:
                print(f"Failed to save data: {e}")

            count += 1
            print_loading_bar(ticker_symbol, ticker_frame, count, total_combinations)

    metadata_file_loc = f"{os.getcwd()}/Data_Collection/Metadata.json"
    with open(metadata_file_loc, 'w') as f:
        json.dump(metadata_list, f, indent=4)

    print(f"\nMetadata saved to {metadata_file_loc}")
    print(f"Data collection for {ticker_symbol} completed.\n")

#Data_From_Ticker_List() #run this to collect all the recent data