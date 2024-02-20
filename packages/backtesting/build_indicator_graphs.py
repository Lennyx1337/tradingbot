import sys
sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
import pandas as pd
import matplotlib.pyplot as plt
import os
from utils import util_functions
from main import main


result_graph = main.get_macd_line(1000, 100, 200)

filename = input("Pls give a name to the png file: ")
script_dir = os.path.dirname(os.path.abspath(__file__))
folder_path= os.path.join(script_dir, "indicator_graphs")

plt.figure(figsize=(10, 6))
plt.plot(pd.Series(result_graph))
plt.xlabel('Time')
plt.ylabel('Values')
plt.title('MACD Line')
plt.grid(True)
plt.savefig(os.path.join(folder_path,f'{filename}'))
plt.show()