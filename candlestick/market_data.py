"""S&P 500 ticker list and daily price download."""
import logging

import pandas as pd
from pytickersymbols import PyTickerSymbols
from tqdm import tqdm
import yfinance as yf

logger = logging.getLogger(__name__)

def reset_dataframe_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Resets the index of a pandas DataFrame while preserving the original columns.

    This function takes a DataFrame as input, resets its index to a default
    integer index, and then selects only the original columns, effectively
    removing any previous index levels as columns.

    Args:
        df (pandas.DataFrame): The DataFrame whose index needs to be reset.

    Returns:
        pandas.DataFrame: A new DataFrame with the index reset and only the
                          original columns retained.

    Example:
        >>> import pandas as pd
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> df = df.set_index('A')
        >>> df
           B
        A
        1  4
        2  5
        3  6
        >>> reset_dataframe_index(df)
           A  B
        0  1  4
        1  2  5
        2  3  6
    """
    original_columns = df.columns  # Store the original column names
    df = df.reset_index()  # Reset the index, which brings the previous index as a column
    df = df[original_columns]  # Select only the original columns
    return df  # Return the DataFrame with the reset index


def load_sp500():
    """
    Prepares a dataset containing S&P 500 stock information.
    Downloads historical candlestick data for each stock and stores it in a dictionary.
    Saves the processed dataframe to a CSV file.

    Returns:
        tuple: (sp500_df, sp500_df_dict, ticker_company_dict), where sp500_df lists the
        tickers with data, sp500_df_dict maps ticker -> OHLCV DataFrame, and
        ticker_company_dict maps ticker -> company name.
    """

    # Initialize PyTickerSymbols object to fetch stock data
    stock_data = PyTickerSymbols()

    # Fetch stock data for S&P 500
    sp500_df = pd.DataFrame(list(stock_data.get_stocks_by_index('S&P 500')))

    # Remove duplicate entries based on 'symbol'
    sp500_df = reset_dataframe_index(sp500_df).groupby('symbol').first().reset_index()

    # Use Yahoo Finance's symbol format for share classes (e.g., BRK.B -> BRK-B)
    sp500_df['symbol'] = sp500_df['symbol'].str.replace('.', '-', regex=False)

    # Download historical candlestick data for all symbols using yfinance
    # The period is set to twice the number of candlestick charts required
    candlestick_df = yf.download(list(sp500_df['symbol'].values),
                                period=f'1y', 
                                interval="1d")

    # Extract date list from candlestick data index
    date_list = [str(each)[:10] for each in list(candlestick_df['Close'].index)]

    # Initialize an empty dictionary to store candlestick data for each ticker
    sp500_df_dict = {}

    # Iterate over each ticker symbol
    for each_ticker in tqdm(sp500_df['symbol'].values, desc="Iterate over each ticker symbol"):
    # debug
    # for each_ticker in tqdm(sp500_df['symbol'].values[:10], desc="Iterate over each ticker symbol"):
        try:
            # Create a temporary dictionary with candlestick data for the current ticker
            temp_dict = {'Date': date_list,
                        'Open': list(candlestick_df['Open'][each_ticker].values),
                        'High': list(candlestick_df['High'][each_ticker].values),
                        'Low': list(candlestick_df['Low'][each_ticker].values),
                        'Close': list(candlestick_df['Close'][each_ticker].values),
                        'Volume': list(candlestick_df['Volume'][each_ticker].values),
                        }
            # Convert the temporary dictionary to a Pandas DataFrame
            temp_df = pd.DataFrame(temp_dict)

            # Check if the first closing price is not NaN (meaning data is available)
            if pd.notna(temp_df['Close'].values[0]):
                # If data is available, add it to the dictionary with the ticker as the key
                sp500_df_dict[each_ticker] = temp_df
        except Exception:
            logger.warning(exc_info=True, msg=f"Skipping {each_ticker}: no candlestick data")

    # Filter the sp500_df to include only tickers with valid candlestick data
    sp500_df = sp500_df[sp500_df['symbol'].isin(list(sp500_df_dict.keys()))]

    # Reset the index of the filtered dataframe
    sp500_df = reset_dataframe_index(sp500_df)

    # Combine multiple industries into a single semicolon-separated string
    sp500_df['industries'] = sp500_df['industries'].apply(lambda x: ';'.join(x))

    # Save the processed dataframe to a CSV file
    sp500_df.to_csv('data/csv/sp500_df.csv', index=False)

    # Map tickers to company names for later use
    ticker_company_dict = dict(zip(sp500_df['symbol'], sp500_df['name']))

    return sp500_df, sp500_df_dict, ticker_company_dict
