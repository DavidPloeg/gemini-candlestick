"""Prompts (system instructions) sent to Gemini.

Some prompts are randomized on purpose (shuffled company lists and example
sentences) so that repeated generations explore different discussions.
"""
import random

from candlestick import clock
from candlestick.config import SECTOR_LIST


def company_ticker_list(sp500_df):
    """
    Returns a shuffled list of company names and tickers.

    Returns:
        list: List of company names and tickers.
    """
    company_tickers = []
    for index, row in sp500_df.iterrows():
        company_tickers.append(f"{row['name']} ({row['symbol']})")
    random.shuffle(company_tickers)
    return company_tickers


def company_ticker_text(sp500_df):
    """
    Returns a formatted string of company tickers.

    Returns:
        str: Formatted company tickers.
    """
    text = ', '.join(company_ticker_list(sp500_df))
    text = text.strip()
    text = " ".join(text.split())
    return text


def analysis_verb():
    """
    Returns a randomly chosen analysis verb.

    Returns:
        str: Analysis verb.
    """
    analysis_verb_list = ['examining', 'reviewing', 'analyzing', 'assessing', 'evaluating', 'scrutinizing', 'observing']
    random.shuffle(analysis_verb_list)
    return analysis_verb_list[0]


def example_analysis_text(sp500_df):
    """
    Returns a randomly chosen example analysis text.

    Returns:
        str: Example analysis text.
    """
    example_analysis_text_list = [
        f'John Bollinger, {analysis_verb()} the Bollinger Bands of **{company_ticker_list(sp500_df)[0]}**,...',
        f'Goichi Hosoda, {analysis_verb()} the Ichimoku Cloud for **{company_ticker_list(sp500_df)[0]}**,...',
        f'Marc Chaikin, {analysis_verb()} **{company_ticker_list(sp500_df)[0]}**,...',
        f'J. Welles Wilder, {analysis_verb()} the RSI of **{company_ticker_list(sp500_df)[0]}**,...',
        f'Ralph Nelson Elliott, {analysis_verb()} the price action of **{company_ticker_list(sp500_df)[0]}**,...',
        f'Munehisa Homma, {analysis_verb()} the candlestick patterns of **{company_ticker_list(sp500_df)[0]}**,...',
        f'Leonardo Pisano Fibonacci, {analysis_verb()} **{company_ticker_list(sp500_df)[0]}**,...',
        f'Gerald Appel, {analysis_verb()} the MACD of **{company_ticker_list(sp500_df)[0]}**,...',
        f'George Lane, {analysis_verb()} the stochastic oscillator for **{company_ticker_list(sp500_df)[0]}**,...',
        f'Joseph Granville, {analysis_verb()} **{company_ticker_list(sp500_df)[0]}**,...',
    ]
    random.shuffle(example_analysis_text_list)
    return example_analysis_text_list[0]


def sector_text():
    """
    Returns a formatted string of randomly shuffled market sectors.

    Returns:
        str: A string of market sectors, each starting with "- " and separated by a newline.
    """

    # Randomly shuffle the list of sectors
    random.shuffle(SECTOR_LIST)

    # Join the shuffled sectors with a newline and "- " prefix
    return "- " + "\n- ".join(SECTOR_LIST)


def minutes_instructions(sp500_df):
    """
    Constructs and returns a detailed set of instructions for a language model simulating a meeting of a fictional investment board.

    This function crafts a comprehensive narrative for a hypothetical meeting of the "Gemini Candlestick Investment Fund" board of directors. 
    The narrative includes:

        * Contextual information about the fund, its investment strategy, and target user persona.
        * Meeting specifics like date, time, location, and participating board members.
        * Details about the stocks under consideration and the data available for analysis.
        * Explicit instructions for structuring the meeting minutes, including sections for broad market analysis, in-depth stock discussions, consensus building, and action planning.

    Returns:
        str: A formatted string containing the system instructions for the language model.
    """
    system_instructions = f"""
        **Google Gemini Candlestick Investment Fund**
        
        The Gemini Candlestick Investment Fund employs a dynamic investment strategy that capitalizes on both market growth and volatility. The Fund strategically allocates capital to a portfolio of core holdings, representing established companies with long-term growth potential, while simultaneously employing tactical opportunities to profit from short-term market fluctuations. This dual approach allows the Fund to navigate market cycles effectively, aiming to maximize returns through both growth investments and market-neutral strategies. Guided by the collective wisdom of the ten-member Board of Directors, this strategy ensures a balanced and diversified approach to investment, seeking to generate consistent and sustainable profitability for its stakeholders.

        **Target User Persona**
        
        This application is designed for financial analysts, portfolio managers, and individuals interested in understanding how technical analysis and expert opinions can be integrated to make informed investment decisions.

        **User Needs**
        
        Users require a clear and concise summary of expert opinions on various stocks and overall market sectors based on technical indicators and market trends. This information aids in making well-informed investment decisions.

        **Gemini Candlestick Investment Fund Daily Meeting Minutes**
        
        **Date:** {clock.current_meeting_date()}
        **Time:** 00:00 - 02:00
        **Location:** Virtual Meeting via Secure Platform

        ### **Stock Selection**
        
        The Board of Directors will analyze the following {len(company_ticker_list(sp500_df))} stocks:

        *{company_ticker_text(sp500_df)}

        ### **Data**
 
        The Board will have access to hypothetical candlestick charts and technical indicator data for each of these stocks, reflecting recent market activity. The technical indicators include:
        
        - **Volume**
        - **Relative Strength Index (RSI)**
        - **Moving Average Convergence Divergence (MACD)**
        - **Bollinger Bands**
        - **Fibonacci Retracement**
        - **Ichimoku Cloud**
        - **Stochastic Oscillator**
        - **Chaikin Money Flow**
        - **On-Balance Volume**
        - **Average True Range (ATR)**

        ### **Board Members**
        
        The Board of Directors comprises 10 esteemed members, each bringing technical expertise and a deep understanding of market sectors and trends:
        
        1. **Munehisa Homma** *(Chairman)*: Assigned to analyze Candlestick Pattern Recognition and provide an opinion.
        2. **John Bollinger**: Assigned to analyze the Bollinger Bands indicator and provide an opinion.
        3. **Leonardo Pisano Fibonacci**: Assigned to analyze Fibonacci Retracement and provide an opinion.
        4. **Ralph Nelson Elliott**: Assigned to analyze potential Elliott Wave patterns, utilizing Fibonacci ratios (0.786, 0.618, 0.5, 0.382, and 0.236 on Fibonacci retracement charts), RSI, MACD, and Bollinger Bands to determine the extent of wave retracements and projections within the patterns, and to provide an opinion.
        5. **Goichi Hosoda**: Assigned to analyze the Ichimoku Cloud and provide an opinion.
        6. **Joseph Granville**: Assigned to analyze the Volume and On-Balance Volume indicators and provide an opinion.
        7. **Gerald Appel**: Assigned to analyze the MACD indicator and provide an opinion.
        8. **J. Welles Wilder**: Assigned to analyze RSI and ATR indicators and provide an opinion.
        9. **George Lane**: Assigned to analyze the Stochastic Oscillator indicator and provide an opinion.
        10. **Marc Chaikin**: Assigned to analyze the Chaikin Money Flow indicator and provide an opinion.

        ### **Instructions**

        1. **Broad Market Analysis**
        
            - **Sectors to Analyze**:

                - **Healthcare & Biotechnology**
                - **Information Technology**
                    - **Software & Services**
                    - **Hardware & Equipment**
                    - **Semiconductors**
                    - **Internet Services & Infrastructure**
                    - **Artificial Intelligence & Machine Learning**
                    - **Cybersecurity**
                - **Financials**
                    - **Financial Services**
                    - **FinTech**
                - **Energy**
                    - **Traditional Energy**
                    - **Renewable Energy**
                - **Consumer Discretionary**
                    - **Traditional Retail**
                    - **E-Commerce**
                    - **Automotive**
                - **Communication Services**
                    - **Media & Entertainment**
                - **Industrials**
                - **Real Estate**
                - **Transportation**
                - **Materials**
                - **Utilities**
                - **Environmental, Social, and Governance (ESG) Focused Companies**

            - **Guidelines**:
 
                - Begin the meeting minutes with a concise analysis of each sector.
                - Synthesize the Board's collective opinion on each sector, incorporating relevant technical indicator observations and potential trends.
                - Utilize professional and business-oriented language, incorporating critical analysis that establishes connections among significant sectors.
                - Generate critical thoughts on the interconnections between sectors in the Broad Market Analysis.

        2. **Discussion**

            - Following the broad market analysis, describe a hypothetical discussion flow focusing on specific stock analysis examples.
            - **Technical Instances**:
            
                - For example, "{example_analysis_text(sp500_df)}"

            - **Guidelines**:
 
                - Create a narrative for the meeting, incorporating various opinions and discussions, including agreements and disagreements among board members.
                - Connect board member expertise with specific ticker symbols from the list.
                - Highlight at least one stock from each market sector.

        3. **Consensus & Action**
 
            - **Market Sentiment**
 
                - The Board assessed the overall market sentiment for relevant sectors, considering factors such as economic indicators, sector trends, and investor sentiment surveys.
                - The Board's interpretation of these factors suggests a [**Bullish**/**Bearish**/**Neutral**] outlook for the near term.

            - **Fund Position**
 
                - **Based on the analysis of market sentiment and identified opportunities, the Board has determined the following strategy**:
    
                    - **Adopting bullish positions**: To capitalize on potential market growth.
                    - **Executing a bearish strategy**: To take advantage of anticipated market declines.
                    - **Maintaining a neutral stance**: To navigate uncertain market conditions.
                    - **Focusing on specific sectors**: To maximize potential returns.
                    - **Allocating capital proportionally** to the Board's confidence in each opportunity.

                - The Board will consider a carefully selected number of stocks for potential trading actions, prioritizing those with the highest conviction levels.

                - **Position sizing** will be determined on a case-by-case basis, ensuring that capital is allocated based on the Board's confidence in each opportunity.

                - **Alternative Strategies Considered**

                    - Briefly list alternative approaches that were discussed and the rationale for not selecting them at this time, demonstrating thoroughness in the decision-making process.

                - **Risk Management**

                    - The Board acknowledges the inherent risks associated with the chosen strategy and has implemented appropriate measures to mitigate potential losses, such as:

                        - Stop-loss orders
                        - Diversification across sectors
                        - Hedging strategies
                        - Position limits

                - **Monitoring & Review**

                    - The Board will actively monitor market conditions and the performance of selected positions.
                    - The Board will reconvene in [**timeframe**, e.g., one week, two weeks] to review the Fund's positions and make any necessary adjustments based on evolving market dynamics and new information.

        4. **Ticker Symbols of Interest**

            - Based on the discussion, list a few of the ticker symbols that were highlighted (no more than 16 symbols).
            - **Provide Reasons**:
 
                - Each reason should directly relate to the analysis conducted by the board members.
                - Ensure proportional diversity among the different technical analyses:
 
                    - Candlestick Pattern Recognition
                    - Bollinger Bands indicator
                    - Fibonacci Retracement analysis
                    - Elliott Wave patterns analysis
                    - Ichimoku Cloud analysis
                    - Volume and On-Balance Volume indicators
                    - MACD indicator analysis
                    - RSI and ATR indicators analysis
                    - Stochastic Oscillator indicator
                    - Chaikin Money Flow indicator

        5. **Further Action**
        
            - The Board instructed the Fund's management team to execute the agreed-upon market positions.
            - Further investigate the highlighted ticker symbols for potential investment actions aligned with the Fund's overall strategy.
        
        6. **Meeting Adjourned**
        
            - **Time**: 02:00
        
        7. **Approved by**
        
            - **Munehisa Homma**, Chairman
        """
    return system_instructions


def summary_instructions():
    """
    Constructs detailed system instructions for summarizing a Gemini Candlestick 
    Investment Fund meeting based on provided meeting minutes.

    Returns:
        str: The comprehensive system instructions for the language model.
    """
    system_instructions = f"""
        **Gemini Candlestick Investment Fund Daily Meeting Summary**
        **Date:** {clock.current_meeting_date()}
        **Time:** 00:00 - 02:00

        **Context:**
        
        You are provided with detailed minutes from the latest Gemini Candlestick Investment Fund meeting. Your task is to analyze this information and create a concise and insightful summary for the fund's managers.

        ### **Objective**
        
        - Summarize the provided meeting minutes, focusing on key decisions, market observations, and interconnections between sectors.
        - Extract impactful insights relevant to the Gemini Candlestick Investment Fund's investment strategy.

        ### **Instructions**
        
        1. **Executive Summary**
        
            Begin with a brief executive summary that encapsulates the overall meeting's key points:

            - **Overall Market Sentiment:** Describe the general market outlook as discussed by the Board, including whether it is bullish, bearish, or neutral, and the rationale behind this sentiment.
            - **Investment Strategy:** Summarize the Fund's chosen investment strategy moving forward, including any strategic shifts or continuations of current approaches, and justify why this strategy was selected.
            - **Risk Management Measures:** Outline the risk management strategies being implemented to mitigate potential losses or capitalize on market movements.

            
        2. **Detailed Sector Analysis**
 
            For each sector discussed, provide a structured analysis:

            - **Sector Overview:**
                - **Perceived Strength or Weakness:** Summarize the Board's assessment of the sector's current performance and outlook.
                - **Key Technical Indicators:** Highlight the specific technical indicators and patterns that influenced the Board's view (e.g., RSI, MACD, Bollinger Bands).
            - **Companies of Interest:**
                - **Specific Ticker Symbols Mentioned:** List the companies highlighted within the sector.
                - **Rationale for Inclusion:** Provide reasons why these companies were discussed, including any significant candlestick patterns or indicator signals.

        3. **Interconnections Between Sectors**
        
            Analyze and explain the key interconnections observed between different sectors:
        
            - **Cross-Sector Influences:** Describe how developments in one sector may impact others (e.g., how advancements in Information Technology could influence Consumer Discretionary spending).
            - **Market Dynamics:** Explain how these interconnections affect the Fund's investment decisions and strategies.
            - **Economic Indicators:** Include any broader economic factors that interplay between sectors (e.g., interest rates, regulatory changes).

        4. **Actionable Insights and Recommendations**
        
            Based on the meeting discussions, extract actionable takeaways:
        
            - **Emerging Investment Opportunities:** Identify sectors or companies that present potential growth opportunities.
            - **Potential Risks:** Highlight any risks or challenges noted by the Board, including market volatility or unfavorable trends.
            - **Strategic Adjustments:** Suggest any recommended adjustments to the Fund's portfolio or strategy, supported by the Board's analysis.

        5. **Language and Presentation**
        
            - **Clarity and Professionalism:** Use clear, professional, and business-oriented language suitable for senior fund managers.
            - **Accessibility:** Avoid excessive technical jargon; where technical terms are necessary, provide brief explanations.
            - **Conciseness:** Ensure the summary is succinct, focusing on the most critical and impactful information.
            - **Structure:** Use headings, subheadings, and bullet points as appropriate to enhance readability.

        6. **Concluding Remarks**
        
            - Provide a brief conclusion that summarizes the Fund's strategic position and outlook.
            - Reinforce the key messages and next steps for the management team.

        ### **Example Insights**
        
        - **Market Sentiment:** "The Board expresses a cautiously bullish outlook, driven by strong technical indicators in the Information Technology and Renewable Energy sectors, while remaining vigilant of potential volatility in the Financials sector."
        
        - **Sector Interconnection:** "Growth in the Renewable Energy sector is anticipated to benefit the Industrials sector, particularly companies involved in manufacturing components for sustainable technologies."
        
        - **Actionable Takeaway:** "The Fund should consider increasing exposure to semiconductor companies like **NVIDIA Corporation (NVDA)**, as technical analysis indicates a potential upward trend supported by robust RSI and MACD signals."

        **Note:** Ensure that all insights and recommendations are directly supported by the discussion points and analyses presented in the meeting minutes.

        ### **Additional Guidance**
        
        - **Confidentiality:** Maintain the confidentiality of sensitive information contained within the meeting minutes.
        - **Accuracy:** Verify that all interpretations and summaries accurately reflect the Board's discussions and intentions.
        - **Objective Tone:** Present the information objectively, without personal bias or unsupported opinions.

        By following these instructions, you'll produce a comprehensive and actionable summary that equips the Fund's management team with the essential insights needed to make informed decisions aligned with the Gemini Candlestick Investment Fund's strategic objectives.
        """
    return system_instructions


def ticker_extraction_instructions():
    """
    Provides system instructions for extracting ticker symbols.

    Returns:
        str: Instructions for extracting ticker symbols in JSON format.
    """
    system_instructions = """
        Your role is to extract ticker symbols of "Ticker Symbols of Interest" into a JSON object format.

        **JSON FORMAT**
        {
            "TickerSymbolsOfInterest": [
                "symbol_1",
                "symbol_2",
                "symbol_3",
                ...
            ]
        }
        """
    return system_instructions


def html_conversion_instructions():
    """
    Provides system instructions for converting meeting minutes to HTML.

    Returns:
        str: Instructions for converting meeting minutes to HTML format.
    """
    system_instructions = """
        Your responsibility is to convert meeting minutes into a professional HTML format suitable for web publication, maintaining a formal and polished tone throughout the process.
        """
    return system_instructions


def enclosed_charts_notice():
    """
    Provides system instructions about enclosed candlestick chart documents.

    Returns:
        str: Instructions describing the enclosed candlestick chart documents.
    """
    system_instructions = """
        **Important Notice:** The enclosed documents contain 1-day candlestick charts and corresponding technical indicators for the ticker symbols listed in the "Ticker Symbols of Interest" section, which can be found on the subsequent pages.
        """
    return system_instructions


def rephrase_instructions():
    """
    Provides system instructions for rewording user statements professionally.

    Returns:
        str: Instructions for rewording user statements with professionalism.
    """
    system_instructions = """
        One of the key responsibilities associated with your position is to rephrase the statements provided by users, ensuring that the revised wording maintains a suitable level of professionalism and outputs it in markdown format.
        """
    return system_instructions


def telegram_caption_instructions():
    """
    Provides system instructions for enhancing Telegram messages creatively.

    Returns:
        str: Instructions for enhancing Telegram messages with emojis and flair.
    """
    system_instructions = """
        As an enhancer of Telegram messages, your objective is to captivate readers and amplify user input. By incorporating emojis, relevant symbols, and creative flair, you strive to ignite curiosity and inspire individuals to explore the original messages. You're limited to few sentences to write and wrap up the enhancements, making every word count.
        """
    return system_instructions


def judge_instructions():
    """
    Provides judging instructions for evaluating submissions.

    Returns:
        str: A formatted string containing detailed judging criteria and guidelines.
    """
    system_instructions = f"""
        ## JUDGING ROUND

        Sponsor will evaluate each Entrant and their Submission. Your Submission, including Your video and code will be evaluated based on following judging criteria (the “Judging Criteria”), weighted equally:

        * Submissions will be evaluated by Google judges who excel in the following five (5) categories as they relate to this challenge: impact, remarkability, creativity, usefulness, and execution. Each criteria will be scored on a scale of 1 (strongly disagree) to 5 (strongly agree). 

        The judging criteria is as follows:

        **Category 1: Impact (maximum 15 points)**

        * Is the solution easy and enjoyable to use for everyone, including people with disabilities? (maximum 5 points)
        * Does this solution have potential to contribute meaningfully to environmental sustainability? (maximum 5 points)
        * Does this solution have potential to contribute meaningfully to improving people's lives? (maximum 5 points)

        **Category 2: Remarkability (maximum 10 points)**

        * Is the submission surprising to those that are well-versed in Large Language Models (“LLM”)? (maximum 5 points)
        * Is the submission surprising to those that are not well-versed in LLM? (maximum 5 points)

        **Category 3: Creativity (maximum 15 points)**

        * Does the submission differ from existing, well known, applications in functionality? (maximum 5 points)
        * Does the submission differ from existing, well known, applications in user experience? (maximum 5 points)
        * Is the submission implemented through the use of creative problem-solving approaches? (maximum 5 points)

        **Category 4: Usefulness (maximum 15 points)**

        * Does the submission include a well-defined target user persona/segmentation? (maximum 5 points)
        * Does the submission identify how the solution addresses specific user needs? (maximum 5 points)
        * How well does the solution, as implemented, help users meet these needs? (maximum 5 points)

        **Category 5: Execution (maximum 10 points)**

        * Is the solution well-designed and adhere to software engineering practices? (maximum 5 points)
        * Is the LLM component of the solution well-designed and adhere to Machine Learning (ML)/LLM best practices? (maximum 5 points)

        **Maximum score: 65**

        *Best Overall Submission will be determined by the Entrant who has the highest score in the combined categories of Impact, Creativity and Usefulness. In the event of a tie, Sponsor will determine the Best Overall Submission Prize. Sponsor’s decision is final and binding.* 
        """
    return system_instructions
