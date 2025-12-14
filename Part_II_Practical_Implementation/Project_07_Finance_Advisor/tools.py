import yfinance as yf
from langchain_core.tools import tool # <--- IMPORTANTE

@tool # <--- Decorador Mágico: Convierte la función en herramienta para el LLM
def get_stock_info(symbol: str):
    """
    Get the current price, P/E ratio, and fundamental info of a stock.
    Args:
        symbol: The stock ticker symbol (e.g., AAPL, NVDA, TSLA).
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Filtramos datos clave
        important_data = {
            "currentPrice": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "sector": info.get("sector"),
            "recommendationKey": info.get("recommendationKey"),
            "businessSummary": info.get("longBusinessSummary", "")[:300] + "..."
        }
        return str(important_data)
    except Exception as e:
        return f"Error fetching data for {symbol}: {e}"

@tool # <--- Decorador Mágico
def get_historical_prices(symbol: str):
    """
    Get the stock price trend over the last month to analyze volatility.
    Args:
        symbol: The stock ticker symbol.
    """
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo")
        if history.empty:
            return "No data found."
            
        start_price = history['Close'].iloc[0]
        end_price = history['Close'].iloc[-1]
        change = ((end_price - start_price) / start_price) * 100
        
        return f"Price 1 month ago: {start_price:.2f}. Current Price: {end_price:.2f}. Change: {change:.2f}%"
    except Exception as e:
        return f"Error fetching history: {e}"
