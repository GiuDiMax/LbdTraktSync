from flask import Flask, render_template, redirect, flash, send_from_directory, make_response, send_file, jsonify
from syncLast import syncLast
from syncAllRatings import syncAll
from syncLibrary import getDiff

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    return jsonify(syncLast())


@app.route('/library', methods=['POST', 'GET'])
def library():
    return jsonify(getDiff())


@app.route('/ratings', methods=['POST', 'GET'])
def ratings():
    return jsonify(syncAll())


if __name__ == '__main__':
    app.run()
