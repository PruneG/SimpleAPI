from flask import Flask, jsonify
app = Flask(__name__)

@app.route ('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, MV!'})

@app.route ('/hola', methods=['GET'])
def hola():
    return jsonify({'message': 'Hola, MV!'})

@app.route ('/bonjour', methods=['GET'])
def bonjour():
    return jsonify({'message': 'Bonjour, MV!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)

