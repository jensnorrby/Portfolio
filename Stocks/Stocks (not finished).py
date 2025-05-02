import os
import glob
import copy
import pandas as pd
import numpy as np
import logging
import datetime
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 14
plt.rcParams["axes.labelsize"] = 17
plt.rcParams["axes.titlesize"] = 17

# Headers for prices
PRICE_HEADERS = ["Close/Last", "Open", "High", "Low"]
DATE = "Date"
CLOSE = "Close/Last"
OPEN = "Open"
VOLUMES = "Volume"
SMA50 = "SM50"  # Simple Moving Average 50 days
SMA200 = "SMA200"  # Simple Moving Average 200 days

# Date constants
# Dataset ends at 06/06/2024, and referred to as 'today'
TODAY = pd.to_datetime("2024-06-06", format="%Y-%m-%d")

# Dictionary for the time intervals
TIMES = {
    "max": TODAY - pd.DateOffset(years=10),
    "5yr": TODAY - pd.DateOffset(years=5),
    "1yr": TODAY - pd.DateOffset(years=1),
    "6m": TODAY - pd.DateOffset(months=6),
    "3m": TODAY - pd.DateOffset(months=3),
    "2m": TODAY - pd.DateOffset(months=2),
    "1m": TODAY - pd.DateOffset(months=1),
    "2w": TODAY - pd.DateOffset(days=14),
    "1w": TODAY - pd.DateOffset(days=7),
}

# Some colors for the context manager below
CLRS = [
    "b",
    "g",
    "r",
    "orange",
    "k",
    "c",
    "m",
    "y",
    "navy",
    "olive",
    "peru",
    "darkblue",
    "lime",
    "grey",
]


class NextColor:
    """Context manager to get the same color
    in a with-statement and automatically
    increment to next available color

    How to use:

    plt.figure()
    with NextColor() as color:
        plt.plot(x,y, color=color)
        plt.plot(x, y**y, color=color)

    plt.show()
    """

    i = 0

    def __init__(self):
        if NextColor.i >= len(CLRS):
            NextColor.i = 0

    def __enter__(self):
        """Return the color next in line"""
        return CLRS[NextColor.i]

    def __exit__(self, type, value, traceback):
        """Increment color number"""
        NextColor.i += 1


class Stock:
    def __init__(self, filepath: str, symbol: str):
        """Constructor : sets the symbol name
        and reads+parses the given data filepath

        Args:
            filepath (str): File path to read
            symbol (str): Name of the given symbol
        """
        self.__symbol = symbol
        self.__stock = pd.DataFrame()
        self.__read_stock(filepath)
        self.__add_sma()

    def __read_stock(self, filepath: str):
        """Reads the stock data from the given filepath (relative/absolute)
        and converts it into the proper data types.

        Args:
            filepath (str): path to read
        """
        stock = pd.read_csv(filepath)
        stock["Date"] = pd.to_datetime(stock["Date"])
        stock["Close/Last"] = stock["Close/Last"].str.replace("$", "").astype(float)
        stock["Open"] = stock["Open"].str.replace("$", "").astype(float)
        stock["High"] = stock["High"].str.replace("$", "").astype(float)
        stock["Low"] = stock["Low"].str.replace("$", "").astype(float)
        self.__stock = stock

    def __add_sma(self):
        """Adds the 50 (SMA50) and 200 (SMA200) days Simple Moving
        Averages for the CLOSE price.
        """
        self.__stock["SMA50"] = self.__stock['Close/Last'].rolling(50).mean()
        self.__stock['SMA200'] = self.__stock['Close/Last'].rolling(200).mean()

    def change_since(self, since: datetime) -> float:
        """Returns the % change in value since the given date

        Args:
            since (datetime): change since that date

        Returns:
            float: % price change in percent
        """
        
        price_change = 100*(self.__stock.loc[self.__stock['Date'] == "2024-06-06", 'Close/Last'].item() - self.__stock.loc[self.__stock['Date'] == since, 'Close/Last'].item()) / self.__stock.loc[self.__stock['Date'] == "2024-06-06", "Close/Last"].item()


        return price_change

    def get_date_range(self, start: datetime = None, end: datetime = None) -> "Stock":
        """Extracts a subset of this stock that is limited to
        [start, end[ dates.
        If start or end is not given, then no filtering is applied.
        A new Stock() object is returned that is limited to the given date range.

        Args:
            start (datetime, optional): Start date of the data to return. If None, no limit
            end (datetime, optional): End date of the data to return. If None, no limit.

        Returns:
            Stock: Returns a stock with the data limited to the date range given.

        Raises:
            ValueError: If end is same or before start date
        """
        substock = Stock(self.__filepath, self.__symbol)
        
        substock.__stock = self.__stock[self.__stock["Date"].between(start or self.__stock["Date"].min, end or "2024-06-06")]

        if pd.to_datetime(start or self.__stock["Date"].min) >= pd.to_datetime(end or "2024-06-06"):
            raise ValueError("The date range cannot end before it has begun.")
        
        return substock

    def __getitem__(self, header):
        try:
            return self.__stock[header]
        except KeyError:
            logging.error(f"key [{header}] not found")
            return None

    @property
    def symbol(self) -> str:
        return self.__symbol


class StocksDB:
    def __init__(self, path: str):
        """Reads in all csv files in a path"""
        self.__stocks = {}
        self.read_files(path)

    def read_files(self, path: str):
        """Reads all the csv files in the given path.
        Each will be stored as a {symbol : Stock} in the __stocks attribute.

        Args:
            path (str): relative or absolute path to the stocks directory.
        """
        # Loop over all csv files in the given path
        for filename in glob.glob(os.path.join(path, "*.csv")):
            filename_as_list = filename.split("\\")
            filename_ending = filename_as_list[-1]
            symbol = filename_ending.replace(".csv", "")
            self.__stocks[symbol] = Stock(filename, symbol)

    def __getitem__(self, name: str) -> Stock:
        """Overload to access stocks in the
        underlying data structure, e.g. db['aapl']

        Args:
            name (str): symbol name

        Returns:
            Stock: the wanted Stock
        """
        try:
            return self.__stocks[name]
        except KeyError:
            logging.error(f"key [{name}] not found")
            return None

    def __iter__(self):
        """Implements the iterator to loop over all the stocks"""
        for stock in self.__stocks.values():
            yield stock


class Plot:
    def __init__(self, db: StocksDB, start: datetime = None, end: datetime = None):
        # Set internal attributes
        self.__db = db
        self.__start = start
        self.__end = end

        # Setup plot
        plt.figure(figsize=(14, 6))
        plt.xlabel(DATE)
        plt.grid()

    def candlestick(self, symbol: str):
        """Generate a Candlestick plot of the given symbol name

        Args:
            symbol (str): Stock symbol name to plot
        """
        # INSERT CODE HERE #
        # Fetch stock for the given date interval
        # Calculate metrics needed to make candlesticks
        # Create the candlesticks plot
        # Add the volumes to the plot
        pass

    def plot(self, symbols: list[str]):
        """Creates a time series plot of all the symbols provided
        during the dates given before.

        Args:
            symbols (list[str]): List of symbol names
        """
        # INSERT CODE HERE #
        pass

    def plot_all(self):
        """Plots all the symbols in the StockDB
        during the dates given in the constructor
        """
        # INSERT CODE HERE #
        pass


class Table:
    def __init__(self, db: StocksDB):
        self.__db = db
        pass

    def print(self, sort_by: str = "symbol", limit: int = None):
        """Prints the table

        Args:
            sort_by (str): How to sort the data, default = symbol
            limit (int): How many stocks to print, default = None -> All
        """
        plot_df = pd.DataFrame()

        for stock in self.__db:
            for key, value in TIMES.items():
                plot_df[key] = stock.change_since(value)
            
        plot_df.sort_values(by=[sort_by])
        print(plot_df.head(limit))
