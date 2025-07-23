import yfinance as yf


def download_stock_data(ticker="AAPL", period='1mo'):
    """
    NOTE
    ----
    cant get SBER UKOIL ...
    """
    stock = yf.Ticker(ticker)
    df = stock.history(period=period)
    return df


if __name__ == "__main__":
    data = download_stock_data()
    print(data)
