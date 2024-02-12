from sqlalchemy import create_engine
import pandas as pd 

engine = create_engine('sqlite:///tradingbot.db')
print(pd.read_sql('SELECT * FROM BTCUSDT', engine))
print(pd.read_sql('SELECT Time, High, Low FROM BTCUSDT', engine))
