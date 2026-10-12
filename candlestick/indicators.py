"""Technical indicators calculated on OHLCV price data."""
import matplotlib.dates as mdates
import pandas as pd
import talib

from candlestick.market_data import reset_dataframe_index


def add_indicators(ohlc, candlestick_chart_no, future_cloud_no):
    """
    Adds technical indicators to a ticker's OHLCV data and prepares it for charting.

    This function calculates various technical indicators and prepares a DataFrame
    with candlestick data (OHLC), RSI, MACD, Bollinger Bands, Stochastic Oscillator,
    CMF, OBV, ATR, and Ichimoku Cloud.

    Args:
        ohlc (pandas.DataFrame): Daily Date, Open, High, Low, Close, Volume data for one ticker.
        candlestick_chart_no (int): Number of trading days to show on the chart.
        future_cloud_no (int): Number of days the Ichimoku Cloud is projected ahead.

    Returns:
        pandas.DataFrame: A DataFrame containing the prepared candlestick data.
    """

    ohlc = ohlc.copy()

    # Convert 'Date' column to matplotlib's numerical date format
    ohlc['ori_Date'] = ohlc['Date']  # Store original date for later use
    ohlc['Date'] = mdates.date2num(ohlc['Date'])

    # Calculate technical indicators

    # RSI
    ohlc['RSI'] = talib.RSI(ohlc['Close'].values)
    ohlc['RSI_SMA_14'] = talib.SMA(ohlc['RSI'], timeperiod=14)  # 14-day SMA of RSI

    # MACD
    close_prices = ohlc['Close']
    macd, macd_signal, macd_hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
    ohlc['macd'] = macd
    ohlc['macdsignal'] = macd_signal
    ohlc['macdhist'] = macd_hist

    # Bollinger Bands
    upperband, middleband, lowerband = talib.BBANDS(ohlc['Close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    ohlc['upperband_BB'] = upperband
    ohlc['middleband_BB'] = middleband
    ohlc['lowerband_BB'] = lowerband

    # Stochastic Oscillator (calculation assumed to be in 'calculate_stochastic_oscillator' method)
    ohlc = calculate_stochastic_oscillator(ohlc)

    # Chaikin Money Flow (CMF)
    ohlc = calc_cmf(ohlc)

    # On-Balance Volume (OBV)
    ohlc['OBV'] = talib.OBV(ohlc['Close'], ohlc['Volume'])

    # Average True Range (ATR)
    ohlc['ATR'] = talib.ATR(ohlc['High'], ohlc['Low'], ohlc['Close'])

    # Ichimoku Cloud (calculation assumed to be in 'calculate_ichimoku' method)
    ohlc = calculate_ichimoku(ohlc, future_cloud_no)

    # Select data for candlestick chart and future cloud
    ohlc = reset_dataframe_index(ohlc.tail(candlestick_chart_no + future_cloud_no))

    # Create a list of consecutive dates for the x-axis
    concat_date_list = []
    for i in range(candlestick_chart_no + future_cloud_no):
        concat_date_list.append(ohlc['Date'].max() - (i + 1))
    ohlc['Date'] = concat_date_list[::-1]  # Assign the dates in reverse order

    return ohlc


def calculate_ichimoku(ohlc, future_cloud_no):
    """
    Calculates the Ichimoku Cloud indicator.

    Args:
        ohlc (pd.DataFrame): DataFrame containing Open, High, Low, Close prices.
        future_cloud_no (int): Number of days to project the cloud ahead.

    Returns:
        pd.DataFrame: DataFrame with Ichimoku Cloud components.
    """

    df = ohlc.copy()

    # Tenkan-sen (Conversion Line): (Highest High + Lowest Low) / 2 for the past 9 periods
    high_9 = df['High'].rolling(window=9).max()
    low_9 = df['Low'].rolling(window=9).min()
    df['Tenkan_Sen'] = (high_9 + low_9) / 2

    # Kijun-sen (Base Line): (Highest High + Lowest Low) / 2 for the past 26 periods
    high_26 = df['High'].rolling(window=26).max()
    low_26 = df['Low'].rolling(window=26).min()
    df['Kijun_Sen'] = (high_26 + low_26) / 2

    # Senkou Span A (Leading Span A): (Tenkan-sen + Kijun-sen) / 2 plotted 26 periods ahead
    df['Senkou_Span_A'] = ((df['Tenkan_Sen'] + df['Kijun_Sen']) / 2).shift(26)

    # Senkou Span B (Leading Span B): (Highest High + Lowest Low) / 2 for the past 52 periods plotted 26 periods ahead
    high_52 = df['High'].rolling(window=52).max()
    low_52 = df['Low'].rolling(window=52).min()
    df['Senkou_Span_B'] = ((high_52 + low_52) / 2).shift(26) 

    # Chikou Span (Lagging Span): Closing price plotted 26 periods behind
    df['Chikou_Span'] = df['Close'].shift(-26)

    # Calculate future Senkou Spans
    future_Senkou_Span_A = list((df['Tenkan_Sen'].tail(26) + df['Kijun_Sen'].tail(26)) / 2)[:future_cloud_no]
    future_Senkou_Span_B = list((high_52.tail(26) + low_52.tail(26)) / 2)[:future_cloud_no]

    # Generate future dates for the cloud
    future_26 = []
    date_val = df['Date'].values[1] - df['Date'].values[0]  # Assuming 'Date' column exists
    for i in range(1, future_cloud_no+1):
        val = df['Date'].tail(1).values[0] + i*date_val
        future_26.append(val)
    future_vals = pd.DataFrame({'Date': future_26})

    # Extend the DataFrame with future dates
    df = pd.concat([df, future_vals], ignore_index=True)

    # Extend Senkou Spans into the future
    all_Senkou_Span_A = list(df['Senkou_Span_A'].values[:-future_cloud_no]) + future_Senkou_Span_A
    df['Senkou_Span_A'] = all_Senkou_Span_A
    all_Senkou_Span_B = list(df['Senkou_Span_B'].values[:-future_cloud_no]) + future_Senkou_Span_B
    df['Senkou_Span_B'] = all_Senkou_Span_B

    return df


def calculate_stochastic_oscillator(data, time_period_k=14, smoothing_period_d=3):
    """
    Calculates the stochastic oscillator (K and D lines) for a given dataset.

    Args:
        data (pandas.DataFrame): DataFrame containing financial data with 'High', 'Low', and 'Close' columns.
        time_period_k (int, optional): Time period for calculating the %K line. Defaults to 14.
        smoothing_period_d (int, optional): Smoothing period for calculating the %D line (moving average of %K). 
                                           Defaults to 3.

    Returns:
        pandas.DataFrame: The input DataFrame with added 'K_STO' and 'D_STO' columns representing 
                          the %K and %D lines of the stochastic oscillator.
    """

    # Calculate the lowest low over the given time period (N)
    data['low_N'] = data['Low'].rolling(time_period_k).min()

    # Calculate the highest high over the given time period (N)
    data['high_N'] = data['High'].rolling(time_period_k).max()

    # Calculate the %K line (Stochastic Oscillator)
    data['K_STO'] = 100 * (data['Close'] - data['low_N']) / (data['high_N'] - data['low_N'])

    # Calculate the %D line (Moving Average of %K)
    data['D_STO'] = data['K_STO'].rolling(smoothing_period_d).mean()

    # Remove temporary columns 'low_N' and 'high_N' as they are no longer needed
    data.drop(columns=['low_N', 'high_N'], inplace=True)

    return data


def calc_cmf(ask_series):
    """
    Calculate the Chaikin Money Flow (CMF) indicator.

    Args:
        ask_series (pd.DataFrame): DataFrame containing the ask price data with columns 'High', 'Low', 'Close', and 'Volume'.

    Returns:
        pd.DataFrame: DataFrame with the CMF column added.
    """

    # Calculate the Money Flow Multiplier (MFV)
    ask_series["cmfm"] = (((ask_series["Close"] - ask_series["Low"]) - (ask_series["High"] - ask_series["Close"])) 
                         / (ask_series["High"] - ask_series["Low"]))

    # Calculate the Money Flow Volume (MFV)
    ask_series["cmfv"] = ask_series["cmfm"] * ask_series["Volume"]

    # Calculate the CMF over a 20-period rolling window
    ask_series["CMF"] = (ask_series['cmfv'].rolling(window=20).mean() / 
                         ask_series['Volume'].rolling(window=21).mean())

    # Remove temporary columns
    ask_series.drop(columns=['cmfm', 'cmfv'], inplace=True)

    return ask_series
