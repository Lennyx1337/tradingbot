from sqlalchemy import create_engine
import pandas as pd 

engine = create_engine('sqlite:///tradingbot.db')
print(pd.read_sql('SELECT * FROM ETHUSDT', engine))
print(pd.read_sql('SELECT High, Low FROM ETHUSDT', engine))
