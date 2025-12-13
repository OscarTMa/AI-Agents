import yfinance as yf

def get_stock_info(symbol: str):
    """
    Retorna información fundamental y precio actual de una acción.
    Args: symbol (str) - Ticker bursátil (ej: AAPL, TSLA).
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Filtramos solo los datos importantes para no saturar al LLM
        important_data = {
            "currentPrice": info.get("currentPrice"),
            "marketCap": info.get("marketCap"),
            "trailingPE": info.get("trailingPE"),
            "forwardPE": info.get("forwardPE"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "recommendationKey": info.get("recommendationKey"), # Buy/Sell/Hold según analistas
            "targetMeanPrice": info.get("targetMeanPrice"),
            "businessSummary": info.get("longBusinessSummary")[:500] + "..." # Resumen corto
        }
        return str(important_data)
    except Exception as e:
        return f"Error fetching data for {symbol}: {e}"

def get_historical_prices(symbol: str):
    """
    Obtiene el historial de precios del último mes para análisis de tendencia.
    """
    try:
        ticker = yf.Ticker(symbol)
        history = ticker.history(period="1mo")
        # Devolvemos un resumen textual de la tendencia (inicio y fin)
        start_price = history['Close'].iloc[0]
        end_price = history['Close'].iloc[-1]
        change = ((end_price - start_price) / start_price) * 100
        
        return f"Price 1 month ago: {start_price:.2f}. Current Price: {end_price:.2f}. Change: {change:.2f}%"
    except Exception as e:
        return "Could not fetch history."
