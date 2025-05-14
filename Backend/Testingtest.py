from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Sallii yhteydet esim. Reactista

@app.route('/ping')
def ping():
    return jsonify(message='Toimii')

if __name__ == '__main__':
    app.run(port=3001)
