from flask import Flask, jsonify, request
from flask_cors import CORS
import sys

# Füge den Pfad zu deinen Paketen hinzu
sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
sys.path.append('Z:/Python_Projekte/tradingbot/packages')

app = Flask(__name__)
CORS(app)

# Handler für OPTIONS-Anfragen (CORS preflight)
@app.route('/tradingbot/main/fib', methods=['OPTIONS'])
def handle_options():
    # Setze die CORS-Header
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'Content-Type'
    }
    return ('', 204, headers)

# Handler für POST-Anfragen
@app.route('/tradingbot/main/fib', methods=['POST'])
def handle_post():
    # Verarbeite hier deine POST-Anfragenlogik
    # Aktuell wird nur eine Erfolgsnachricht zurückgegeben
    return jsonify({'message': 'Received POST request'}), 200

if __name__ == '__main__':
    app.run(debug=True)






# from flask import Flask
# from flask_cors import CORS
# import sys
# sys.path.append('C:/Users/lenna/LokaleDaten/applied_project/tradingbot/packages')
# sys.path.append('Z:/Python_Projekte/tradingbot/packages')

# app = Flask(__name__)
# CORS(app)

# from packages import *

# if __name__ == '__main__':
#     app.run(debug=True)