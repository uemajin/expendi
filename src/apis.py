import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def get_exchange_rate(source_currency: str, destination_currency: str, date: str) -> float:
    if source_currency == destination_currency:
        return 1.0

    target_date = pd.to_datetime(date)
    start_date = target_date - timedelta(days=5)
    end_date = target_date + timedelta(days=1)

    pair = source_currency + destination_currency + '=X'

    try:
        data = yf.download(pair, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
        if data.empty:
            return 1.0  # Fallback value if no data

        # Find the closest available date before or equal to target
        available_dates = data.index[data.index <= target_date]
        if len(available_dates) == 0:
            return 1.0  # no data before or on the target date

        closest_date = available_dates[-1]
        return float(data.loc[closest_date]['Close'].iloc[0])

    except Exception as e:
        print(f"Exchange rate fetch error: {e}")
        return 1.0
