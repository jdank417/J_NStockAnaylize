# b5dd9bbe937d64ec8c81be6fb999a2ed
# @Author Jason Dank
# @Author Nico Bonanno
#Hey
import json
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

from numpy import double

start_date = "2023-10-01"
end_date = "2023-11-01"
api_key = "b5dd9bbe937d64ec8c81be6fb999a2ed"

ticker = input("Enter Stock Ticker: ")
User_Start_Date = input("Enter Date of Purchase: ")
User_End_Date = input("Enter Current Date: ")




def get_jsonparsed_data(url):
   try:
       res = urlopen(url)
       data = res.read().decode("utf-8")
       return json.loads(data)
   except Exception as e:
       print(f"Error fetching data: {e}")
       return None




def fetch_data_chunks(ticker, start_date, end_date, api_key):
   all_data = []


   while start_date < end_date:
       chunk_end_date = (pd.to_datetime(start_date) + pd.DateOffset(months=1)).strftime('%Y-%m-%d')
       url = f"https://financialmodelingprep.com/api/v3/historical-chart/30min/{ticker}?from={start_date}&to={chunk_end_date}&apikey={api_key}"
       data = get_jsonparsed_data(url)


       if data:
           all_data.extend(data)


       start_date = chunk_end_date


   return all_data


def create_data_structure(data):
   date_close_dict = {}


   for entry in data:
       date = entry['date']
       close_price = double(entry['close'])
       date_close_dict[date] = close_price


   return date_close_dict

def sp500_dictionary(compData):
    sp500_dict = {}

    for entry in compData:
        date = entry['date']
        close_price = double(entry['close'])
        sp500_dict[date] = close_price

    return sp500_dict


def plot_stock_data(date_close_dict, ticker):
   dates = list(date_close_dict.keys())
   close_prices = list(date_close_dict.values())


   plt.figure(figsize=(20, 8))
   date_column = pd.to_datetime(dates).date  # Extract only the date component
   plt.plot(date_column, close_prices, label=f'{ticker} Close Price', color='blue')
   plt.title(f'{ticker} Close Price Chart for ' + start_date + " - " + end_date)
   plt.xlabel('Date')
   plt.ylabel('Close Price')
   plt.legend()
   plt.grid(True)


   # Set the x-axis ticks to display only dates
   plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator())
   plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))


   plt.show()




def get_close_price(date_close_dict, target_date):
   # Try to find the close price for the exact target date
   close_price = date_close_dict.get(target_date, None)


   if close_price is not None:
       return int(close_price)


   # If not found, try to find the close price for a similar date (ignoring the time component)
   try:
       target_date_dt = datetime.strptime(target_date, '%Y-%m-%d').date()
       for date, price in date_close_dict.items():
           if date == target_date_dt:  # Directly compare date objects
               return price
   except ValueError:
       pass


   # If still not found, return "Date not found"
   return "Date not found"

def getroi(date_close_dict):
    endDate = get_close_price(date_close_dict, User_End_Date)
    startDate = get_close_price(date_close_dict, User_Start_Date)
    roi = ((endDate - startDate) / startDate)*100
    return roi

def getefficiency(date_close_dict, sp500_dict):
    if(getroi(sp500_dict) > getroi(date_close_dict)):
        print("This stock is performing worse than the S&P500. Therefore, it is currently an inefficient investment")
    else:
        print("This stock is performing on par or better than the S&P500. Therefore, it is currently an efficient investment")


def main():

   data = fetch_data_chunks(ticker, start_date, end_date, api_key)
   compData = fetch_data_chunks('voo', start_date, end_date, api_key)


   if data:
       df = pd.DataFrame(data)
       df['date'] = pd.to_datetime(df['date']).dt.date  # Convert 'date' column to datetime and extract date component


       # Filter the DataFrame based on the user's specified date range
       df_filtered = df[(df['date'] >= pd.to_datetime(start_date).date()) & (df['date'] <= pd.to_datetime(end_date).date())]


       # Create a data structure with date and close price
       date_close_dict = create_data_structure(df_filtered.to_dict('records'))


       # Plot the stock data
       plot_stock_data(date_close_dict, ticker)


       # Get close price for start day
       close_price_start = get_close_price(date_close_dict, User_Start_Date)

       # Get close price for end day
       close_price_end = get_close_price(date_close_dict, User_End_Date)


       if close_price_start != "Date not found":
           print(f"Close Price for {User_Start_Date}: {close_price_start}")
       else:
           print(f"No data found for the specified date.")

       if close_price_end != "Date not found":
           print(f"Close Price for {User_End_Date}: {close_price_end}")
       else:
           print(f"No data found for the specified date.")


       if compData:
           df = pd.DataFrame(compData)
           df['date'] = pd.to_datetime(
               df['date']).dt.date  # Convert 'date' column to datetime and extract date component

           # Filter the DataFrame based on the user's specified date range
           df_filtered = df[
               (df['date'] >= pd.to_datetime(start_date).date()) & (df['date'] <= pd.to_datetime(end_date).date())]

           # Create a data structure with date and close price
           sp500_dict = sp500_dictionary(df_filtered.to_dict('records'))

           # Now, 'date_close_dict' contains date as keys and close price as values

           # Plot the stock data
           plot_stock_data(sp500_dict, 'voo')

   print('ROI for',ticker,':',getroi(date_close_dict), '%')
   print('ROI for VOO (Vanguard S&P500 Fund): ', getroi(sp500_dict), '%')
   getefficiency(date_close_dict, sp500_dict)

   for date, close_price in date_close_dict.items():
           print(f"Date: {date}, Close Price: {close_price}")


if __name__ == "__main__":
   main()
