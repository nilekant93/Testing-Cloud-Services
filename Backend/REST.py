from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

import Week1
import Week3  # tuo Week3 mukaan

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

    if component == 'Week1':
        result, message = Week1.run_test(url)
        return jsonify({
            'status': 'success',
            'test_passed': result,
            'message': message
        }), 200
    elif component == 'Week3':
        result, message = Week3.run_test(url)
        return jsonify({
            'status': 'success',
            'test_passed': result,
            'message': message
        }), 200
    else:
        return jsonify({'status': 'unknown component'}), 400

if __name__ == '__main__':
    app.run(port=3001)
