import requests

base_url = 'http://localhost:8000'

# Test für den EMA-Endpunkt
def test_ema():
    data = {"minutes": 5, "ema": 10}
    response = requests.post(f'{base_url}/ema', json=data)
    if response.status_code == 200:
        try:
            print("EMA Response:", response.json())
        except ValueError:
            print("Failed to decode JSON from response:", response.text)
    else:
        print("Failed with status code:", response.status_code, "Response body:", response.text)

# Test für den Fibonacci-Retracement-Endpunkt
def test_fibonacci():
    data = {"minutes": 30}
    response = requests.post(f'{base_url}/fibonacci', json=data)
    print("Fibonacci Response:", response.json())

# Test für den MACD-Line-Endpunkt
def test_macd_line():
    data = {"minutes": 60, "short_ema": 12, "long_ema": 26}
    response = requests.post(f'{base_url}/macd-line', json=data)
    print("MACD Line Response:", response.json())

# Test für den MACD-Signal-Line-Endpunkt
def test_macd_signal_line():
    data = {"minutes": 60, "short_ema": 12, "long_ema": 26, "signal_window": 9}
    response = requests.post(f'{base_url}/macd-signal-line', json=data)
    print("MACD Signal Line Response:", response.json())

# Test für den MACD-Signals-List-Endpunkt
def test_macd_signals_list():
    data = {"minutes": 60, "short_ema": 12, "long_ema": 26, "signal_window": 9}
    response = requests.post(f'{base_url}/macd-signals-list', json=data)
    print("MACD Signals List Response:", response.json())

# Test für den RSI-Endpunkt
def test_rsi():
    data = {"minutes": 14, "window_days": 14}
    response = requests.post(f'{base_url}/rsi', json=data)
    print("RSI Response:", response.json())

# Funktion zum Ausführen aller Tests
def run_all_tests():
    print("Testing EMA Endpoint")
    test_ema()
    print("Testing Fibonacci Endpoint")
    test_fibonacci()
    print("Testing MACD Line Endpoint")
    test_macd_line()
    print("Testing MACD Signal Line Endpoint")
    test_macd_signal_line()
    print("Testing MACD Signals List Endpoint")
    test_macd_signals_list()
    print("Testing RSI Endpoint")
    test_rsi()

if __name__ == "__main__":
    run_all_tests()