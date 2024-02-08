import sys
sys.path.append('Z:/Python_Projekte/tradingbot/packages')

from utils import util_functions

# Beispielwerte für die Indikatoren
prices = [100, 110, 120, 115, 125, 130, 135]
low_price = 100
high_price = 135
short_ema_window = 5
long_ema_window = 10

# Fibonacci Retracement
fibonacci_levels = util_functions.calculate_fibonacci_retracement(low_price, high_price)
print("Fibonacci Retracement Levels:", fibonacci_levels)

# Exponentiell gleitender Durchschnitt (EMA)
ema_values = util_functions.calculate_ema(prices, short_ema_window)
print("Exponentiell gleitender Durchschnitt (EMA) Werte:", ema_values)

# MACD (Moving Average Convergence Divergence)
macd_line = util_functions.calculate_macd(prices, short_ema_window, long_ema_window, "line")
print("MACD Linie:", macd_line)

# Signal Linie
signal_line = util_functions.calculate_signal_line(macd_line)
print("Signal Linie:", signal_line)

# Kauf- und Verkaufssignale
signals = util_functions.calculate_signals(macd_line, signal_line)
print("Kauf- und Verkaufssignale:", signals)

# Relative Strength Index (RSI)
rsi = util_functions.calculate_rsi(prices)
print("Relative Strength Index (RSI):", rsi)