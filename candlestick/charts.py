"""Candlestick chart drawing and chart formatting helpers."""
import datetime
import gc
import os

import matplotlib
# Set backend to 'Agg' for non-interactive plotting
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# Set default figure size and DPI
plt.rc('figure', figsize=(15, 12), dpi=300)
from matplotlib.ticker import FuncFormatter  # Custom tick formatting
from mplfinance.original_flavor import candlestick_ohlc  # Candlestick charts
from PIL import Image


def draw_candlestick_chart(ohlc, ticker, company, graph_width, future_cloud_no):
    """
    Generates and saves a candlestick chart image with various technical indicators.

    The chart includes the following subplots:
        - Candlestick chart with Bollinger Bands and Fibonacci retracement levels
        - Volume bars
        - RSI with SMA
        - MACD with histogram
        - Ichimoku Cloud with Fibonacci retracement levels
        - Stochastic Oscillator
        - Chaikin Money Flow (CMF)
        - On-Balance Volume (OBV)
        - Average True Range (ATR)

    The function saves the generated chart as a PNG image.

    Args:
        ohlc (pandas.DataFrame): Output of `indicators.add_indicators`.
        ticker (str): Ticker symbol, used in the title and file names.
        company (str): Company name, used in the title.
        graph_width (float): Width of each candlestick and volume bar.
        future_cloud_no (int): Number of projected Ichimoku Cloud days at the end of `ohlc`.
    """

    data = ohlc.copy()

    # Create a figure and subplots
    fig, (ax1, ax5, ax2, ax8, ax4, ax3, ax9, ax6, ax7) = plt.subplots(
        9, 1, sharex=True, figsize=(20, 30), 
        gridspec_kw={'height_ratios': [1, 1, 0.33, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]}
    )

    # Set background color for all subplots
    for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9]:
        ax.set_facecolor("#151924")

    # Set grid for all subplots
    for ax in [ax1, ax2, ax4, ax5, ax7, ax8, ax9]:
        ax.set_axisbelow(True)
        ax.grid(color='#2E323D', linestyle='-', zorder=0)

    # --- Subplot 1: Candlestick chart with Bollinger Bands and Fibonacci retracement ---
    ax1.set_title(f'{company} ({ticker}): 1d Candlestick Chart (with Technical Indicators)', fontsize=16)

    # Plot Fibonacci retracement levels
    levels = [0, 0.214, 0.382, 0.5, 0.618, 0.764, 1]
    color_list = ['#787B86', '#06BCD4', '#0A9981', '#4CAF51', '#FF9800', '#F23545', '#787B86']
    levels_label = ['1', '0.786', '0.618', '0.5', '0.382', '0.236','0']
    for i, level in enumerate(levels):
        price = ohlc['Low'].min() + (ohlc['High'].max() - ohlc['Low'].min()) * level
        ax1.axhline(price, linestyle='-', linewidth=0.75, color=color_list[i], zorder=1)
        ax1.text(ohlc['Date'].iloc[-1], price, f"{levels_label[i]} " + "(" + "{:.2f}".format(price) + ")", 
                 va='bottom', ha='right', fontsize=12, color=color_list[i], alpha=0.7)

    # Plot Bollinger Bands
    ax1.plot(ohlc['Date'], ohlc['upperband_BB'], color='#F23545', linestyle='-', linewidth=1, zorder=1)
    ax1.plot(ohlc['Date'], ohlc['middleband_BB'], color='#2862FF', linestyle='-', linewidth=1, zorder=1)
    ax1.plot(ohlc['Date'], ohlc['lowerband_BB'], color='#0A9981', linestyle='-', linewidth=1, zorder=1)
    ax1.fill_between(ohlc['Date'], ohlc['lowerband_BB'], ohlc['upperband_BB'], color='#2862FF', alpha=0.078, zorder=1)

    # Format y-axis
    ax1.yaxis.set_major_formatter(FuncFormatter(comma_formatter_2))
    ax1.set_ylabel('Price, BB, and Fib Retracement', fontsize=16)
    ax1.yaxis.set_label_position('left')
    ax1.yaxis.set_ticks_position('both')
    ax1.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax1.yaxis.set_tick_params(labelsize=13)
    ax1.set_ylim(top=ohlc['upperband_BB'].max() + (ohlc['upperband_BB'].max()-ohlc['lowerband_BB'].min())*0.15)

    # Plot candlestick chart
    candlestick_ohlc(ax1, ohlc.values, width=graph_width, colorup='#26A69A', colordown='#F05350', alpha=1.0)

    # --- Subplot 2: Volume ---
    volume_color = ['#1C5E5F' if data['Close'][i] >= data['Open'][i] else '#813539' for i in range(len(data))]
    ax2.bar(data['Date'], data['Volume'], width=graph_width, color=volume_color, zorder=1)
    ax2.set_ylabel('Volume', fontsize=16, labelpad=20)
    ax2.yaxis.set_label_position('left')
    ax2.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    ax2.yaxis.set_ticks_position('both')
    ax2.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax2.yaxis.set_tick_params(labelsize=13)
    ax2.set_ylim(1, ohlc['Volume'].max() + (ohlc['Volume'].max()-ohlc['Volume'].min())*0.20)

    # --- Subplot 3: RSI ---
    ax3.set_ylabel('RSI', fontsize=16)
    ax3.yaxis.set_label_position('left')
    ax3.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax3.fill_between(ohlc['Date'], 30, 70, color='#212035', zorder=1)
    ax3.axhline(y=30, color='grey', linestyle='--', linewidth=0.5, zorder=2)
    ax3.axhline(y=50, color='grey', linestyle='--', linewidth=0.5, zorder=2)
    ax3.axhline(y=70, color='grey', linestyle='--', linewidth=0.5, zorder=2)
    ax3.yaxis.set_tick_params(labelsize=13)
    ax3.set_ylim(1, 99)
    ax3.grid(color='#2E323D', linestyle='-', zorder=1)
    ax3.plot(ohlc['Date'], ohlc['RSI'], color='#7D57C2', linewidth=1, zorder=2)
    ax3.plot(ohlc['Date'], ohlc['RSI_SMA_14'], color='yellow', linewidth=1, zorder=3)

    # --- Subplot 4: MACD ---
    ax4.set_ylabel('MACD', fontsize=16)
    ax4.plot(ohlc['Date'], ohlc['macd'], color='#2862FF', label='MACD', linewidth=1, zorder=1)
    ax4.plot(ohlc['Date'], ohlc['macdsignal'], color='#FF6D00', label='Signal', linewidth=1, zorder=1)
    ax4.yaxis.set_ticks_position('both')
    ax4.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax4.yaxis.set_major_formatter(FuncFormatter(comma_formatter))
    macd_colors = get_color_list(list(ohlc['macdhist'].values))
    ax4.bar(ohlc['Date'], ohlc['macdhist'], color=macd_colors, alpha=0.5, width=graph_width, label='Histogram', zorder=1)
    ax4.yaxis.set_tick_params(labelsize=13)
    ax4.yaxis.set_major_formatter(FuncFormatter(comma_formatter_2))
    max_val = max(ohlc['macd'].max(), ohlc['macdsignal'].max(), ohlc['macdhist'].max())
    min_val = min(ohlc['macd'].min(), ohlc['macdsignal'].min(), ohlc['macdhist'].min())
    ax4.set_ylim(top=max_val + ((max_val - min_val) * 0.15))

    # --- Subplot 5: Ichimoku Cloud ---
    ax5.plot(ohlc['Date'], ohlc['Tenkan_Sen'], label='Tenkan-sen', color='#2862FF', linewidth=1, zorder=1)
    ax5.plot(ohlc['Date'], ohlc['Kijun_Sen'], label='Kijun-sen', color='#B71C1C', linewidth=1, zorder=1)
    ax5.plot(ohlc['Date'], ohlc['Chikou_Span'], label='Chikou Span', color='#43A047', linewidth=1, zorder=1)
    ax5.plot(ohlc['Date'], ohlc['Senkou_Span_A'], label='Senkou Span A (Leading Span A)', color='#A5D6A7', linewidth=1, zorder=1)
    ax5.plot(ohlc['Date'], ohlc['Senkou_Span_B'], label='Senkou Span B (Leading Span B)', color='#EF9A9A', linewidth=1, zorder=1)
    ax5.fill_between(ohlc['Date'], ohlc['Senkou_Span_A'], ohlc['Senkou_Span_B'], 
                    where=ohlc['Senkou_Span_A'] >= ohlc['Senkou_Span_B'], 
                    facecolor='#43A047', alpha=0.125, interpolate=True, zorder=1)
    ax5.fill_between(ohlc['Date'], ohlc['Senkou_Span_A'], ohlc['Senkou_Span_B'], 
                    where=ohlc['Senkou_Span_A'] < ohlc['Senkou_Span_B'], 
                    facecolor='#B71C1C', alpha=0.125, interpolate=True, zorder=1)
    ax5.set_ylabel('Price, Ichimoku Cloud, and Fib Retracement', fontsize=16)
    ax5.yaxis.set_label_position('left')
    ax5.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax5.yaxis.set_tick_params(labelsize=13)

    # Plot Fibonacci retracement levels
    levels_2 = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
    color_list_2 = ['#787B86', '#F23545', '#FF9800', '#4CAF51', '#0A9981', '#06BCD4', '#787B86']
    levels_label_2 = ['0', '0.236', '0.382', '0.5', '0.618', '0.786','1']
    for i, level in enumerate(levels_2):
        price = ohlc['Low'].min() + (ohlc['High'].max() - ohlc['Low'].min()) * level
        ax5.axhline(price, linestyle='-', linewidth=0.75, color=color_list_2[i], zorder=1)
        ax5.text(ohlc['Date'].iloc[-1], price, f"{levels_label_2[i]} " + "(" + "{:.2f}".format(price) + ")", 
                 va='bottom', ha='right', fontsize=12, color=color_list_2[i], alpha=0.7)

    ax5.yaxis.set_major_formatter(FuncFormatter(comma_formatter_2))
    ax5.set_ylim(top=ohlc['High'].max() + (ohlc['High'].max()-ohlc['Low'].min())*0.15)
    candlestick_ohlc(ax5, ohlc.values, width=graph_width, colorup='#26A69A', colordown='#F05350', alpha=1.0)

    # --- Subplot 6: Stochastic Oscillator ---
    ax6.set_ylabel('STO', fontsize=16)
    ax6.yaxis.set_label_position('left')
    ax6.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax6.fill_between(ohlc['Date'], 20, 80, color='#20172E', zorder=1)
    ax6.axhline(y=20, color='grey', linestyle='--', linewidth=0.5, zorder=2)
    ax6.axhline(y=80, color='grey', linestyle='--', linewidth=0.5, zorder=2)
    ax6.yaxis.set_tick_params(labelsize=13)
    ax6.set_ylim(-8, 115)
    ax6.grid(color='#2E323D', linestyle='-', zorder=1)
    ax6.plot(ohlc['Date'], ohlc['K_STO'], color='#09AE0C', linewidth=1, zorder=2)
    ax6.plot(ohlc['Date'], ohlc['D_STO'], color='#B25B11', linewidth=1, zorder=3)

    # --- Subplot 7: Chaikin Money Flow ---
    ax7.axhline(y=0, color='#9598A1', linestyle='--', linewidth=0.5, zorder=1)
    ax7.plot(ohlc['Date'], ohlc['CMF'], color='#09AE0C', linewidth=1, zorder=1)
    ax7.set_ylabel('CMF', fontsize=16)
    ax7.yaxis.set_ticks_position('both')
    ax7.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax7.yaxis.set_tick_params(labelsize=13)
    ax7.set_ylim(top=ohlc['CMF'].max() + (ohlc['CMF'].max()-ohlc['CMF'].min())*0.15)

    # --- Subplot 8: On-Balance Volume ---
    ax8.plot(ohlc['Date'], ohlc['OBV'], color='#2862FF', linewidth=1, zorder=1)
    ax8.set_ylabel('OBV', fontsize=16)
    ax8.yaxis.set_ticks_position('both')
    ax8.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax8.yaxis.set_major_formatter(FuncFormatter(millions_formatter))
    ax8.yaxis.set_tick_params(labelsize=13)
    ax8.set_ylim(top=ohlc['OBV'].max() + (ohlc['OBV'].max()-ohlc['OBV'].min())*0.15)

    # --- Subplot 9: Average True Range ---
    ax9.plot(ohlc['Date'], ohlc['ATR'], color='#B71C1C', linewidth=1, zorder=1)
    ax9.set_ylabel('ATR', fontsize=16)
    ax9.yaxis.set_ticks_position('both')
    ax9.yaxis.set_tick_params(pad=10, direction='inout', length=6, labelright=True, right=True)
    ax9.yaxis.set_major_formatter(FuncFormatter(comma_formatter))
    ax9.yaxis.set_tick_params(labelsize=13)
    ax9.set_xlabel('Date', fontsize=16)
    ax9.xaxis.set_tick_params(labelsize=13)
    ax9.yaxis.set_major_formatter(FuncFormatter(comma_formatter_2))
    ax9.set_ylim(top=ohlc['ATR'].max() + (ohlc['ATR'].max()-ohlc['ATR'].min())*0.15)

    # --- Add titles and labels to subplots ---
    label_list = ["BB ", "SMA ", "close 2 ", f"{title_formatter(ohlc['middleband_BB'].values[-1-future_cloud_no])} ", f"{title_formatter(ohlc['upperband_BB'].values[-1-future_cloud_no])} ", f"{title_formatter(ohlc['lowerband_BB'].values[-1-future_cloud_no])}"]
    colors = ['white', '#868993', '#868993', '#2862FF', '#F23545', '#0A9981', '#EF9A9A']
    color_title(ax1, label_list, colors, y=0.958)

    label_list = ["Fibonacci ", "Retracement ", "0 ", "0.236 ", "0.382 ", "0.5", " 0.618", " 0.786", "1"]
    colors = ['white','white','#787B86', '#F23545', '#FF9800', '#4CAF51', '#0A9981', '#06BCD4', '#787B86']
    color_title(ax1, label_list, colors, y=0.908)

    label_list = ["Ichimoku ", "9 26 52 26 ",
                f"{title_formatter(ohlc['Tenkan_Sen'].loc[ohlc['Tenkan_Sen'].last_valid_index()])} ",
                f"{title_formatter(ohlc['Kijun_Sen'].loc[ohlc['Kijun_Sen'].last_valid_index()])} ",
                f"{title_formatter(ohlc['Chikou_Span'].loc[ohlc['Chikou_Span'].last_valid_index()])} ",
                f"{title_formatter(ohlc['Senkou_Span_A'].values[-1])} ",
                f"{title_formatter(ohlc['Senkou_Span_B'].values[-1])}",
                ]
    colors = ['white', '#868993', '#2862FF', '#B71C1C', '#43A047', '#A5D6A7', '#EF9A9A']
    color_title(ax5, label_list, colors, y=0.958)

    label_list = ["Fibonacci ", "Retracement ", "0 ", "0.236 ", "0.382 ", "0.5", " 0.618", " 0.786", "1"]
    colors = ['white','white','#787B86', '#F23545', '#FF9800', '#4CAF51', '#0A9981', '#06BCD4', '#787B86']
    color_title(ax5, label_list, colors, y=0.908)

    label_list = ["Volume ", f"{human_format(ohlc['Volume'].values[-1-future_cloud_no])}"]
    colors = ['white', volume_color[data[data['Close'].isna()].index[0] - 1]]
    color_title(ax2, label_list, colors, y=0.88)

    label_list = ["RSI ", "14 close ", 
                f"{title_formatter(ohlc['RSI'].values[-1-future_cloud_no])} ",
                f"{title_formatter(ohlc['RSI_SMA_14'].values[-1-future_cloud_no])}",
                ]
    colors = ['white', "#868993", "#7D57C2" , "yellow"]
    color_title(ax3, label_list, colors, y=0.92)

    label_list = ["MACD ", "12 26 close ",
                f"{title_formatter(ohlc['macdhist'].values[-1-future_cloud_no])} ",
                f"{title_formatter(ohlc['macd'].values[-1-future_cloud_no])} ",
                f"{title_formatter(ohlc['macdsignal'].values[-1-future_cloud_no])}",
                ]
    colors = ['white', "#868993", macd_colors[:-future_cloud_no][-1], "#2862FF", "#FF6D00"]
    color_title(ax4, label_list, colors, y=0.92)

    label_list = ["Stochastic Oscillator ", "14 3 80 20 ",
                f"{title_formatter(ohlc['K_STO'].values[-1-future_cloud_no])} ",
                f"{title_formatter(ohlc['D_STO'].values[-1-future_cloud_no])} ",
                ]
    colors = ['white', "#868993", "#07FC00", "#FF7F00"]
    color_title(ax6, label_list, colors, y=0.92)

    label_list = ["CMF ", "20 ",
                f"{title_formatter(ohlc['CMF'].values[-1-future_cloud_no])}",
                ]
    colors = ['white', "#868993", "#09AE0C",]
    color_title(ax7, label_list, colors, y=0.92)

    label_list = ["OBV ", f"{human_format(ohlc['OBV'].values[-1-future_cloud_no])}",
                ]
    colors = ['white', "#2862FF",]
    color_title(ax8, label_list, colors, y=0.92)

    label_list = ["ATR ", "14 RMA ",
                f"{title_formatter(ohlc['ATR'].values[-1-future_cloud_no])}",
                ]
    colors = ['white', "#868993", "#B71C1C",]
    color_title(ax9, label_list, colors, y=0.92)

    # Calculate the date difference between the first two data points for x-axis limit setting
    date_val = ohlc['Date'].values[1] - ohlc['Date'].values[0]

    # Set the x-axis limits, adding padding based on the date difference
    ax1.set_xlim([ohlc['Date'].min() - date_val, ohlc['Date'].max() + date_val])

    # Set x-axis ticks at specific intervals (assuming 26 periods per year)
    ax1.set_xticks([
        ohlc.iloc[0]['Date'],                     # First date
        ohlc.iloc[26 - 1]['Date'],               # End of the 1st period
        ohlc.iloc[26 * 2 - 1]['Date'],          # End of the 2nd period
        ohlc.iloc[26 * 3 - 1]['Date'],          # ... and so on
        ohlc.iloc[26 * 4 - 1]['Date'],
        ohlc.iloc[26 * 5 - 1]['Date'],
        ohlc.iloc[26 * 6 - 1]['Date'],
        ohlc.iloc[(26 * 7 - 1)]['Date'],
        ohlc.iloc[(26 * 8 - 1)]['Date'],
    ])

    # Create a list of x-axis tick labels using 'ori_Date' column
    xticklabels_list = [
        ohlc.iloc[0]['ori_Date'],
        ohlc.iloc[26 - 1]['ori_Date'],
        ohlc.iloc[26 * 2 - 1]['ori_Date'],
        ohlc.iloc[26 * 3 - 1]['ori_Date'],
        ohlc.iloc[26 * 4 - 1]['ori_Date'],
        ohlc.iloc[26 * 5 - 1]['ori_Date'],
        ohlc.iloc[26 * 6 - 1]['ori_Date'],
        ohlc.iloc[(26 * 7 - 1)]['ori_Date'],
    ]

    # Format the date strings to month format
    xticklabels_list = [get_date_month_text(each) for each in xticklabels_list]

    # Make a copy of the original tick labels
    ori_xticklabels_list = xticklabels_list.copy()

    # Append additional tick labels for future dates
    start_i = 26 - 1
    xticklabels_list.append(get_date_month_text(ohlc['ori_Date'].values[start_i - 1]))
    next_i = start_i + 26
    xticklabels_list.append(get_date_month_text(ohlc['ori_Date'].values[next_i]))

    for _ in range(5):
        next_i = next_i + 26
        xticklabels_list.append(get_date_month_text(ohlc['ori_Date'].values[next_i]))

    # Parse the last x-axis tick date with its year (avoids leap-day errors and wrong weekdays)
    last_date = datetime.datetime.strptime(ohlc['ori_Date'].values[next_i], '%Y-%m-%d')

    # Calculate next weekdays (Monday to Friday)
    next_days = []
    days_to_add = 26
    while len(next_days) < days_to_add:
        last_date += datetime.timedelta(days=1)
        if last_date.weekday() < 5:  # Monday to Friday are 0-4
            next_days.append(last_date)

    # Format the next weekdays and append to the original tick labels
    next_days_str = [date.strftime('%d %b') for date in next_days]
    ori_xticklabels_list.extend([next_days_str[-1]])

    # Use the modified tick labels for the plot
    xticklabels_list = ori_xticklabels_list.copy()
    ax1.set_xticklabels(xticklabels_list)

    # --- Adjust layout and save the figure ---
    plt.subplots_adjust(left=0.085, right=0.925, bottom=0.025, top=0.975)
    fig.subplots_adjust(hspace=0.03)
    plt.savefig('data/png/temp.png')

    # Open the image file
    with Image.open("data/png/temp.png") as img:
        # Define the new dimensions required for resizing, specifically for the input images used in the Gemini project.
        new_width, new_height = 2048, 3072

        # Resize the image using LANCZOS resampling for high quality
        img_resized = img.resize((new_width, new_height), resample=Image.LANCZOS)

        # Save the resized image with the ticker as the filename
        img_resized.save(f"data/png/{ticker}.png")

    # Open the resized image
    with Image.open(f"data/png/{ticker}.png") as img:
        # Convert the image to an 8-bit palette mode with 256 colors
        # using adaptive palette generation for optimal color representation
        img = img.convert("P", palette=Image.ADAPTIVE, colors=256)

        # Save the optimized image with reduced file size
        img.save(f"data/png_optimized/{ticker}.png", optimize=True)

    # Remove temporary files and clear memory
    os.remove('data/png/temp.png')
    plt.close(fig)
    plt.close('all')
    plt.clf()
    plt.cla()
    ohlc = None
    data = None
    fig = None
    ax1 = None
    ax2 = None
    ax3 = None
    ax4 = None
    ax5 = None
    ax6 = None
    ax7 = None
    ax8 = None
    ax9 = None
    volume_color = None
    colors = None
    img = None
    img_resized = None
    del ohlc, data, fig, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9
    del volume_color, colors, img, img_resized
    matplotlib.pyplot.close('all')
    matplotlib.use('Agg')
    gc.collect()


def human_format(num):
    """
    Formats a number to a human-readable string using SI unit prefixes.

    Args:
        num: The number to format.

    Returns:
        A string representing the number in a human-readable format (e.g., "1.2K", "15M", "2.5B").
    """

    magnitude = 0  # Initialize the magnitude (power of 1000)
    while abs(num) >= 1000:
        magnitude += 1  # Increment the magnitude for each 1000
        num /= 1000.0  # Divide the number by 1000

    # Format the number with the appropriate suffix
    # ['', 'K', 'M', 'G', 'T', 'P'] corresponds to ["", "Thousand", "Million", "Billion", "Trillion", "Peta"]
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def get_color_list(values):
    """
    Generates a list of colors based on a list of values.

    The color scheme uses green for positive values and red for negative values.
    Darker shades indicate a larger value compared to the previous value.

    Args:
        values: A list of numerical values.

    Returns:
        A list of color strings (hexadecimal format).
    """

    # Define color codes for different shades
    dark_green = '#26A69A'
    light_green = '#B2DFDB'
    light_red = '#FFCDD2'
    dark_red = '#FF5252'

    # Initialize the colors list
    colors = []

    # Initialize the previous value for comparison
    previous_value = values[0]

    # Iterate through the values and assign colors
    for value in values:
        if value < 0:  # Negative value
            if value < previous_value:  # More negative than previous
                colors.append(dark_red) 
            else:  # Less negative than previous
                colors.append(light_red)
        elif value > 0:  # Positive value
            if value > previous_value:  # More positive than previous
                colors.append(dark_green)
            else:  # Less positive than previous
                colors.append(light_green)
        else:  # Zero value
            colors.append(light_green)  # Treat zero as a slightly positive value
        previous_value = value  # Update the previous value for the next iteration

    return colors


def millions_formatter(x, pos):
    """
    Formats a number to a human-readable string with thousands, millions, billions, etc. suffixes.

    Args:
        x: The number to format.
        pos: The position of the tick (not used in this implementation).

    Returns:
        A string representing the formatted number.
    """

    num = x  # Start with the original number
    magnitude = 0  # Initialize the magnitude (0 = no suffix, 1 = K, 2 = M, etc.)

    # Keep dividing by 1000 until the number is less than 1000
    while abs(num) >= 1000:
        magnitude += 1  # Increment the magnitude
        num /= 1000.0  # Divide the number by 1000

    # Create the formatted string using string formatting
    # '%.0f' rounds the number to an integer
    # %s inserts the appropriate suffix from the list
    return '%.0f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def comma_formatter(x, pos):
    """
    Formats a numeric value with commas as thousands separators.

    Args:
        x: The numeric value to format.
        pos: The position of the value (unused in this formatter).

    Returns:
        str: The formatted string with commas as thousands separators.
    """
    return "{:,}".format(x)


def comma_formatter_2(x, pos):
    """
    Formats a numeric value with commas as thousands separators and 2 decimal places.

    Args:
        x: The numeric value to format.
        pos: The position of the value (unused in this formatter).

    Returns:
        str: The formatted string with commas and 2 decimal places.
    """
    return "{:,.2f}".format(x)


def title_formatter(x):
    """
    Formats a numeric value with 2 decimal places.

    Args:
        x: The numeric value to format.

    Returns:
        str: The formatted string with 2 decimal places.
    """
    return "{:.2f}".format(x)


def color_title(ax, labels, colors, textprops={'size': 15}, y=0.96):
    """
    Creates a left-aligned title with multiple colors.

    This function adds a title to the given axes object, where each word 
    in the title can have a different color. 

    Important: 
        Do not change axes limits after calling this function, 
        as it may misalign the title.

    Args:
        ax (matplotlib.axes.Axes): The axes object to add the title to.
        labels (list): A list of strings, where each string is a word in the title.
        colors (list): A list of colors, where each color corresponds to a word in `labels`.
        textprops (dict, optional): A dictionary of text properties to apply to the title. 
                                    Defaults to {'size': 15}.
        y (float, optional): The vertical position of the title in axes coordinates. 
                            Defaults to 0.96 (close to the top).
    """

    # Draw the figure to be able to get text extents
    plt.gcf().canvas.draw()

    # Use axes coordinates for positioning the text
    transform = ax.transAxes  

    # Initial horizontal position - start from the left (x=0)
    x_pos = 0  

    # Dictionary to store the text objects for each label
    text = dict()  

    # Iterate through labels and corresponding colors
    for label, col in zip(labels, colors):
        # Add text to the axes
        text[label] = ax.text(x_pos, y, label,
                                transform=transform,  # Use axes coordinates
                                ha='left',           # Left alignment
                                color=col,             # Set text color
                                **textprops)           # Apply any additional text properties

        # Update x_pos for the next label based on the previous label's width
        x_pos = text[label].get_window_extent().transformed(transform.inverted()).x1


def get_date_month_text(date_str):
    """Converts a date string in 'YYYY-MM-DD' format to 'DD Mon' format.

    Args:
        date_str: The date string in 'YYYY-MM-DD' format.

    Returns:
        The date string in 'DD Mon' format (e.g., '01 Jan').
    """

    # Convert the date string to a datetime object
    date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")

    # Format the datetime object to 'DD Mon' format
    return date_obj.strftime("%d %b")
