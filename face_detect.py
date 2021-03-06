import cv2
import sys
import flask
import jsonpickle
import numpy as np
from flask import Flask, request, Response
import json
import requests

# Starting the flask
app = flask.Flask(__name__)
# To send healthy status to SageMaker
# Creation of the ping.html page
@app.route('/', methods=['GET'])
def home():
    return ("<center><h1><b> Written by Carlos Pool Interian </b></h1></center>")

@app.route('/ping', methods=['GET'])
def ping():
    status = 200 #if health else 404
    return flask.Response(response='\n', status=status, mimetype='application/json')

@app.route('/test', methods=['GET'])
def test():
   name = 'family.jpg'
   addr = 'http://127.0.0.1:8080'
   test_url = addr + '/invocations?imageID='+name
   # prepare headers for http request
   content_type = 'image/png'   
   headers = {'content-type': content_type}  
   img = cv2.imread(name)
   # encode image as jpeg
   _, img_encoded = cv2.imencode('.png', img)
   # send http request with image and receive response
   response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
   status = 200
   return flask.Response(response=json.loads(response.text), status=status, mimetype='application/json')     
# To access and manipulate to SageMaker resources
# Creation of the invocations.html page
@app.route('/invocations', methods=['GET', 'POST'])
def call_face_recognition():
   # Get user supplied values
   cascPath = "haarcascade_frontalface_default.xml"
   imagerequest = request  
   # convert string of image data to uint8
   nparr = np.frombuffer(imagerequest.data, np.uint8)
   # decode image
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   # Create the haar cascade
   faceCascade = cv2.CascadeClassifier(cascPath)
   # Read the image
   image = img
   gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   # Detect faces in the image
   faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
   #print("Found {0} faces!".format(len(faces)))
   # Draw a rectangle around the faces   
   # build a response dict to send back to client
   x=faces[:,0]
   y=faces[:,1]
   w=faces[:,2]
   h=faces[:,3]   
   ##Json responce implementation
   imageID = request.args.get('imageID') 
   values = {'imageID' : imageID}
   values.update({'faces' : []})   
   tail = {}   
   for inc in range(len(faces)):
      tail = {'x' : faces[inc][0].tolist(), 'y' : faces[inc][1].tolist(), 'w' : faces[inc][2].tolist(), 'h' : faces[inc][3].tolist()}
      values['faces'].append(tail)   
   #response of json values
   response_2client= json.dumps(values, indent=4)
   # Encode response using jsonpickle
   response_2client = jsonpickle.encode(response_2client)
   # Draw a rectangle around the faces
   for (x, y, w, h) in faces:
        cv2.rectangle(image , (x, y), (x+w, y+h), (0, 255, 0), 2)   
   #showing image
   #cv2.imshow("Faces found", img)
   #cv2.waitKey(0)
   status = 200     
   return flask.Response(response=response_2client, status=status, mimetype='application/json')


app.run(host='127.0.0.1', port=8080)