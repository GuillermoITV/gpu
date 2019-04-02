from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)

# route http posts to this method
@app.route('/default/<name>')
def default(name):
    return 'imageID: ' + name +','
    if __name__ == '-__main__':
        app.run(debug=True)


app.run(host='127.0.0.1', port=443)