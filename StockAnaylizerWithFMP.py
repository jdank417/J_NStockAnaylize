# b5dd9bbe937d64ec8c81be6fb999a2ed
# @Author Jason Dank
# @Author Nico Bonanno

import json
from urllib.request import urlopen
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from numpy import double
import J_N_SMS
import J_N_SMTP

# Constants
start_date = "2023-10-01"
end_date = "2023-11-01"
api_key = "b5dd9bbe937d64ec8c81be6fb999a2ed"
ticker = input("Enter Stock Ticker: ")
phoneNumber = input("Enter Phone Number: ")
User_Start_Date = "2023-10-06"  # input("Enter Date of Purchase: ")
User_End_Date = "2023-10-13"  # input("Enter Current Date: ")


def get_jsonparsed_data(url):
    try:
        open_url = urlopen(url)
        url_data = open_url.read().decode("utf-8")
        return json.loads(url_data)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def fetch_data_chunks(ticker, start_date, end_date, api_key):
    all_data = []

    while start_date < end_date:
        chunk_end_date = (pd.to_datetime(start_date) + pd.DateOffset(months=1)).strftime('%Y-%m-%d')
        close_price_url = f"https://financialmodelingprep.com/api/v3/historical-chart/30min/{ticker}?from={start_date}&to={chunk_end_date}&apikey={api_key}"
        json_data = get_jsonparsed_data(close_price_url)

        if json_data:
            all_data.extend(json_data)

        start_date = chunk_end_date

    return all_data


def close_price_dictionary(close_price_data):
    date_close_dict = {}

    for entry in close_price_data:
        date = entry['date']
        close_price = double(entry['close'])
        date_close_dict[date] = close_price

    return date_close_dict


def sp500_dictionary(sp500_data):
    sp500_dict = {}

    for entry in sp500_data:
        date = entry['date']
        close_price = double(entry['close'])
        sp500_dict[date] = close_price

    return sp500_dict


def volume_dictionary(close_price_data):
    volume_dict = {}

    for entry in close_price_data:
        date = entry['date']
        volume = double(entry['volume'])
        volume_dict[date] = volume

    return volume_dict


def plot_stock_data(date_close_dict, ticker):
    date_list = list(date_close_dict.keys())
    close_price_list = list(date_close_dict.values())

    plt.figure(figsize=(20, 8))
    date_column = pd.to_datetime(date_list).date  # Extract only the date component
    plt.plot(date_column, close_price_list, label=f'{ticker} Close Price', color='blue')
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
    roi = ((endDate - startDate) / startDate) * 100
    return roi


def getefficiency(date_close_dict, sp500_dict):
    if (getroi(sp500_dict) > getroi(date_close_dict)):
        print("This stock is performing worse than the S&P500. Therefore, it is currently an inefficient investment")
    else:
        print(
            "This stock is performing on par or better than the S&P500. Therefore, it is currently an efficient investment")


def get_dividend(ticker, api_key):
    try:
        div_url = f"https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{ticker}?apikey={api_key}"
        div_data = get_jsonparsed_data(div_url)

        if 'historical' in div_data:
            dividends_history = div_data['historical']
            dividends_info = [(dividend['date'], dividend['adjDividend']) for dividend in dividends_history]
            div_dict = dict(dividends_info)
            return div_dict

        print(f"No dividend data found for {ticker}.")
        return None

    except Exception as e:
        print(f"Error fetching dividend data: {e}")
        return None


def get_close(symbol, start, end):
    closeData = fetch_data_chunks(symbol, start, end, api_key)
    if closeData:
        df = pd.DataFrame(closeData)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df_filtered = df[
            (df['date'] >= pd.to_datetime(start_date).date()) & (df['date'] <= pd.to_datetime(end_date).date())]
        date_close_dict = close_price_dictionary(df_filtered.to_dict('records'))
    return date_close_dict


def main():
    # Constants for SMS configuration
    number = phoneNumber
    provider = "Verizon"
    sender_credentials = ("jnstockanalyize@gmail.com", "tplr znil sobq eazj")

    closeData = fetch_data_chunks(ticker, start_date, end_date, api_key)
    sp500Data = fetch_data_chunks('VOO', start_date, end_date, api_key)
    divData = get_dividend(ticker, api_key)
    volumeData = fetch_data_chunks(ticker, start_date, end_date, api_key)

    if closeData:
        # Plot the stock data
        df = pd.DataFrame(closeData)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df_filtered = df[
            (df['date'] >= pd.to_datetime(start_date).date()) & (df['date'] <= pd.to_datetime(end_date).date())]
        date_close_dict = close_price_dictionary(df_filtered.to_dict('records'))
        plot_stock_data(date_close_dict, ticker)
        close_price_start = get_close_price(date_close_dict, User_Start_Date)
        close_price_end = get_close_price(date_close_dict, User_End_Date)

        # Print the close prices for the specified dates
        if close_price_start != "Date not found":
            print(f"Close Price for {User_Start_Date}: {close_price_start}")
        else:
            print(f"No data found for the specified date.")

        if close_price_end != "Date not found":
            print(f"Close Price for {User_End_Date}: {close_price_end}")
        else:
            print(f"No data found for the specified date.")

        # Qualify Divdata
        if divData:
            df = pd.DataFrame(closeData)
            df['date'] = pd.to_datetime(df['date']).dt.date
            div_Dict = get_dividend(ticker, api_key)
            plot_stock_data(div_Dict, ticker)

        # Qualify VolumeData
        if volumeData:
            df = pd.DataFrame(closeData)
            df['date'] = pd.to_datetime(df['date']).dt.date
            volume_Dict = volume_dictionary(df_filtered.to_dict('records'))
            plot_stock_data(volume_Dict, ticker)

        # Qualify SP500Data
        if sp500Data:
            df = pd.DataFrame(sp500Data)
            df['date'] = pd.to_datetime(df['date']).dt.date
            df_filtered = df[
                (df['date'] >= pd.to_datetime(start_date).date()) & (df['date'] <= pd.to_datetime(end_date).date())]
            sp500_dict = sp500_dictionary(df_filtered.to_dict('records'))
            plot_stock_data(sp500_dict, 'VOO')

        # Send ROI via SMS and thank-you message
        try:
            # Send ROI via SMS
            message_to_send_sms = f"Your ROI for {ticker} is {getroi(date_close_dict)}%"

            # Print the ROI message before sending
            print("ROI Message:")
            print(message_to_send_sms)

            # Split the message into smaller parts
            message_parts = [message_to_send_sms[i:i + 160] for i in range(0, len(message_to_send_sms), 160)]

            # Send each part separately
            for part in message_parts:
                J_N_SMS.send_sms_via_email(number, part, provider, sender_credentials)

            print(f"ROI sent successfully via SMS to {number}.")

            # Thank-you message
            thank_you_message = "Thank you for using J&N Stock Analyze! We appreciate your business."

            # Print the thank-you message before sending
            print("Thank-You Message:")
            print(thank_you_message)

            # Send thank-you message
            J_N_SMS.send_sms_via_email(number, thank_you_message, provider, sender_credentials)
            print(f"Thank-you message sent successfully via SMS to {number}.")

        except Exception as e:
            print(f"Error sending ROI and thank-you message via SMS: {e}")

    # Send Data via Email
    sender_email = 'jnstockanalyize@gmail.com'
    app_password = 'tplr znil sobq eazj'
    recipient_email = 'jasondank@yahoo.com'
    email_subject = 'J&N Stock Analyze'
    email_message = f"Your ROI for {ticker} is {getroi(date_close_dict)}%"
    J_N_SMTP.send_email(sender_email, app_password, recipient_email, email_subject, email_message)


    # Print date_close_dict
    print('')
    print('Daily Close Prices for', ticker, ':')
    for date, close_price in date_close_dict.items():
        print(f"Date: {date}, Close Price: {close_price}")

    # Print sp500_dict
    print('')
    print('Daily Close Prices for VOO (Vanguard S&P500 Fund):')
    for date, close_price in sp500_dict.items():
        print(f"Date: {date}, Close Price: {close_price}")

    # Print div_dict
    print('')
    print(f'Dividend data for {ticker}:')
    for date, div_Data in div_Dict.items():
        print(f"Date: {date}, div_Data: {div_Data}")

    # Print volume_dict
    print('')
    print(f'Volume data for {ticker}:')
    for date, volumeData in volume_Dict.items():
        print(f"Date: {date}, volume_Data: {volumeData}")


if __name__ == "__main__":
    main()
