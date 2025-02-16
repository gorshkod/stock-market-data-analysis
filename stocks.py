"""
stocks.py

A Python script to retrieve and process stock data from the NASDAQ API.

Currently, the script only retrieves the data and prints it in JSON format.

Usage: python stocks.py <TICKER1> ...

Author: Daniil Gorshkov
"""
import sys # For getting command-line arguments
from requests import get # For downloading data from the NASDAQ API
from datetime import date # For etting the start date for the data range
from json import dumps # For printing the data in JSON format (testing acquisition)

def download_data(ticker: str) -> dict:
    """
    Returns past 5 years of stock data for the given ticker in JSON format if the download is successful.
    """
    ticker = ticker.upper()
    today = date.today()
    start = str(today.replace(year=today.year - 5))
    base_url = "https://api.nasdaq.com"
    path = f"/api/quote/{ticker}/historical?assetclass=stocks&fromdate={start}&limit=9999"
    
    # Concatenate the base URL and the path to get the full URL
    full_url = base_url + path
    
    # Set the User-Agent header to avoid getting blocked by the server
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = get(full_url, headers=headers) # Send an HTTP GET request to the URL
        response.raise_for_status() # Raise an exception if the HTTP response status code is not 200
        response = response.json() # Convert the response to a dictionary
        
        # Check if the 'data' field is null or empty (happens for invalid tickers)
        if response["data"] is None:
            print(f"Data acquisition error for ticker '{ticker}': no data found")
            return {} # Return an empty dictionary if no data was found
        
        return response
    except Exception as e:
        print(f"Data acquisition error for ticker {ticker}: {e}")
        
    return {} # Return an empty dictionary if an error occurred

def process_data(data: dict) -> dict:
    """
    Processes the data and returns a dictionary with the minimum, maximum, average, and median closing prices.
    Not implemented yet.
    """
    pass

def main():
    arguments = sys.argv
    if len(arguments) < 2: # If the user did not provide any tickers, print the usage message and exit
        print("Usage: python stocks.py <TICKER1> ...") 
        sys.exit(1)
    
    for ticker in arguments[1:]: # Process each ticker
        data = download_data(ticker) # Download the data
        print(dumps(data, indent=4)) # Print the data in JSON format (for testing)
        

if __name__ == "__main__": # Run the main function if the script is executed directly and not imported
    main()