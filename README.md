# Gemini Candlestick Investment Fund Simulation

[![Watch the Demo Video](https://img.youtube.com/vi/nJvH27cIxFo/maxresdefault.jpg)](https://www.youtube.com/watch?v=nJvH27cIxFo)

> 🏆 **Google Gemini API Developer Competition Project:**  
> Check out our submission page here: [https://ai.google.dev/competition/projects/gemini-candlestick](https://ai.google.dev/competition/projects/gemini-candlestick)

---

This repository hosts a Python application that simulates the investment decision-making process of the "Gemini Candlestick Investment Fund," a fictional investment board. The simulation employs candlestick chart analysis, technical indicators, and Google's Gemini large language model to inform investment strategies.

## Table of Contents

- [Introduction](#introduction)
- [Key Features](#key-features)
- [Use Cases](#use-cases)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
  - [How to get your Telegram Bot Token & Chat ID](#how-to-get-your-telegram-bot-token--chat-id)
- [Structure](#structure)
- [License](#license)
- [Hardware Requirements](#hardware-requirements)

## Introduction

The Gemini Candlestick Investment Fund application represents a sophisticated solution meticulously crafted to replicate the intricate dynamics of a board of directors' meeting. By harnessing advanced algorithms, it meticulously analyzes stock market data to formulate hypothetical investment strategies. Leveraging candlestick charts, technical indicators, and the computational prowess of Google's Gemini large language model, this application offers a distinctive capability: reviving esteemed figures of the financial realm to engage in comprehensive discussions. This immersive feature enables these luminaries to convene and deliberate as if in a real-world setting. As a result, users are provided with an interactive environment that mirrors authentic financial analysis and decision-making processes, fostering a deeper understanding of investment strategies.

### Board of Directors

The esteemed board of directors comprises notable figures in the realm of financial analysis, each tasked with analyzing specific indicators and offering their expert insights:

1. **Munehisa Homma**, Chairman of the Board: Responsible for scrutinizing Candlestick Pattern Recognition and delivering informed perspectives.
2. **John Bollinger**: Tasked with assessing the Bollinger Bands (BB) indicator and providing analytical commentary.
3. **Leonardo Pisano Fibonacci**: Assigned to evaluate Fibonacci retracement levels and deliver insightful opinions.
4. **Ralph Nelson Elliott**: Engaged in analyzing potential Elliott Wave patterns employing Fibonacci ratios (0.786, 0.618, 0.5, 0.382, and 0.236 on Fibonacci retracement charts), RSI, MACD, and Bollinger Bands to ascertain wave retracements and projections within the patterns, and furnishing comprehensive opinions.
5. **Goichi Hosoda**: Entrusted with the evaluation of the Ichimoku Cloud and furnishing expert opinions.
6. **Joseph Granville**: Responsible for analyzing Volume and On-Balance Volume (OBV) indicators and delivering expert opinions.
7. **Gerald Appel**: Tasked with analyzing the MACD indicator and providing discerning viewpoints.
8. **J. Welles Wilder**: Charged with analyzing RSI and ATR indicators and offering well-founded opinions.
9. **George Lane**: Assigned to evaluate the Stochastic Oscillator indicator and provide expert insights.
10. **Marc Chaikin**: Entrusted with the analysis of the Chaikin Money Flow indicator and delivering comprehensive opinions.

## Key Features

- **Data Acquisition:** Efficiently retrieves historical candlestick data for selected stocks from the S&P 500 index utilizing the `yfinance` library.
- **Technical Analysis:** Conducts a comprehensive analysis by computing various technical indicators, including:
  - Relative Strength Index (RSI)
  - Moving Average Convergence Divergence (MACD)
  - Bollinger Bands
  - Fibonacci Retracement Levels
  - Ichimoku Cloud
  - Stochastic Oscillator
  - Chaikin Money Flow
  - On-Balance Volume (OBV)
  - Average True Range (ATR)
- **Candlestick Charting:** Generates detailed and visually appealing candlestick charts overlaid with technical indicators using `matplotlib` and `mplfinance`.
- **Google Gemini Integration:** Utilizes Google's Gemini large language model to:
  - Simulate discussions and analyses resembling those of board members.
  - Generate comprehensive meeting minutes covering market observations, individual stock analyses, and investment rationale.
  - Summarize actionable insights, key takeaways, and the fund's overall market strategy.
  - Create engaging captions for charts and reports.
- **Telegram Integration:** Automatically distributes daily reports, summaries, and highlighted candlestick charts to a designated Telegram chat via the Telegram Bot API.

## Use Cases

- **Educational Tool:** Serves as a comprehensive resource for understanding the application of candlestick charts and technical indicators in financial analysis, providing concrete examples and hands-on learning opportunities.
- **Simulation Environment:** Creates a secure and controlled platform for experimenting with various investment strategies, allowing users to observe potential outcomes without real financial risk.
- **Algorithmic Trading Inspiration:** Acts as a catalyst for the development of automated trading strategies, utilizing technical indicators and sentiment analysis from language models.
- **Financial Education:** Facilitates learning about different technical indicators, candlestick patterns, and their interpretations through an immersive and interactive simulated environment.

## Getting Started

To get the application up and running, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/thanatchon36/gemini-candlestick.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd gemini-candlestick
   ```

3. **Add your keys** (see [Configuration](#configuration)):
   ```bash
   cp .env.example .env
   # then edit .env
   ```

4. **Start the Application:**
   ```bash
   docker compose up -d --build
   ```

5. **Watch the logs:**
   ```bash
   docker compose logs -f
   ```

Generated reports and charts are saved to the `data/` folder.

### Running without Docker

Requires Python 3.12 or newer. TA-Lib installs from a prebuilt wheel, so you don't need to compile it. To make PDFs, `weasyprint` needs the Pango library (`brew install pango` on macOS, `apt install libpango-1.0-0 libpangoft2-1.0-0` on Debian/Ubuntu).

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
set -a && source .env && set +a   # load keys from .env
python main.py
```

## Configuration

Copy `.env.example` to `.env` and fill in the values. `.env` is git-ignored, so never commit your real keys.

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | Yes | Your Google Gemini API key. Get one at [Google AI Studio](https://aistudio.google.com/apikey). |
| `BOT_TOKEN` | Yes | Your Telegram bot token (see below). |
| `CHAT_ID` | Yes | The ID of your Telegram chat/channel (see below). |
| `GEMINI_MODEL` | No | The Gemini model to use. Defaults to `gemini-3.8-flash`. |

### How to get your Telegram Bot Token & Chat ID

1. **Create a Bot and get `BOT_TOKEN`:**
   - Open Telegram and search for `@BotFather`.
   - Send `/newbot` and follow the prompts to choose a name and username for your bot.
   - Copy the HTTP API access token provided by BotFather (e.g., `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

2. **Create a Channel and add your bot as an Administrator:**
   - Create a new Telegram Channel.
   - Go to Channel Info > **Administrators** > **Add Admin**.
   - Search for your bot username and add it as an administrator.

3. **Get your `CHAT_ID`:**
   - Add `@RawDataBot` as an administrator to your channel temporarily.
   - Post any test message in the channel.
   - `@RawDataBot` will automatically reply with the Channel ID (usually starts with `-100...`).
   - Copy the ID (e.g., `-1002161110558`) and set it as your `CHAT_ID`.
   - You can remove `@RawDataBot` from the channel afterwards.

## Structure

- **`docker-compose.yml`:** Defines the Docker container for running the application.
- **`Dockerfile.custom`:** Specifies instructions for building the Docker image, including installing dependencies and setting up the environment.
- **`requirements.txt`:** Pinned Python dependencies.
- **`.env.example`:** Template for the required environment variables.
- **`geminicandlestick.py`:** Contains the main class, `GeminiCandlestick`, which handles data fetching, processing, charting, and Telegram interactions.
- **`main.py`:** The entry point of the application. Manages the overall workflow of data generation, charting, and Telegram notifications.

## License

This project is submitted to The Gemini API Developer Competition, sponsored by Google LLC. The submission is subject to the [Official Rules of the competition](https://ai.google.dev/competition), including the intellectual property provisions. 

## Hardware Requirements

- **Minimum & Recommended:** CPU: 2 cores (ARM64 or x86_64), RAM: 2GB, Storage: 16 GB

This application has been developed and tested on a MacBook M1, which comfortably meets these requirements.
