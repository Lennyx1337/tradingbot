import pandas as pd
import os
import matplotlib.pyplot as plt
from binance.client import Client
client = Client()

def getdata(symbol, start):
    frame = pd.DataFrame(client.get_historical_klines(symbol, '1h', start))

    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame.set_index('Time', inplace=True)
    frame.index = pd.to_datetime(frame.index, unit = 'ms')
    frame = frame.astype(float)
    return frame

df = getdata('BTCUSDT', '2023-01-01')
df['price'] = df.Open.shift(-1)
df['ret'] = df.Close.pct_change()
df = df.dropna()


def st_momentum_and_tsl_strategy(df, entry, dist):
    profits = []
    in_position = False

    for index, row in df.iterrows():
        if not in_position and row.ret >entry:
            buyprice = row.price
            in_position = True
            trailing_stop =  buyprice * dist
        if in_position:
            if row.Close * dist >= trailing_stop:
                trailing_stop = row.Close * dist 
            if row.Close <= trailing_stop:
                sellprice = row.price
                profit = (sellprice-buyprice)/buyprice - 0.0015
                profits.append(profit)
                in_position = False
        
    filename = input("Bitte geben Sie den Dateinamen für die PNG-Datei ein: ")
    folder_path="./graphs"

    plt.figure(figsize=(10, 6))
    plt.plot((pd.Series(profits)+1).cumprod())
    plt.xlabel('Trades')
    plt.ylabel('Profit')
    plt.title('Profit from Trades') 
    plt.grid(True)
    plt.savefig(os.path.join(folder_path,f'{filename}.png'))
    return plt.show()

st_momentum_and_tsl_strategy(df,0.02,0.99)