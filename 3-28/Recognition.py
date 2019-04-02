from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/test', methods=['GET','POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here...
    #====================================================================
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces in the image
    faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
    #flags = cv2.CV_HAAR_SCALE_IMAGE
    )

    print("Found {0} faces!".format(len(faces)))

# Draw a rectangle around the faces
    for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    cv2.imshow("Faces found", img)
    cv2.waitKey(0)

    #--------------------------------------------------------------------

    # build a response dict to send back to client
    response = {'message': 'image received. size={}x{}'.format(img.shape[1], img.shape[0])
                }
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host='127.0.0.1', port=443)