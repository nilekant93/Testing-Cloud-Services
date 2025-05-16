from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import Week1  # Tuodaan Week1-testit tänne

app = Flask(__name__)
CORS(app)

@app.route('/ping')
def ping():
    return jsonify(message='Toimii')

@app.route('/receive', methods=['POST'])
@cross_origin()
def receive():
    data = request.get_json()
    url = data.get('url')
    component = data.get('component', 'Unknown')

    print(f"Received URL: {url} (from component: {component})")

    # Suorita testi komponentin mukaan
    if component == 'Week1':
        result = Week1.run_test(url)
        return jsonify(status='success', test_passed=result), 200
    else:
        return jsonify(status='unknown component'), 400

if __name__ == '__main__':
    app.run(port=3001)

