import cv2, requests, base64
from time import sleep
import tellopy
# Gets an image from the webcam
def getWebcamImageData():
    cam = cv2.VideoCapture(0)
    try:
        ok, image = cam.read()
        if ok != True:
            raise ValueError("Problem using the webcam")
        ok, data = cv2.imencode('.jpg', image)
        if ok != True:
            raise ValueError("Problem getting image data")
        return base64.b64encode(data)
    finally:
        cam.release()


# This function will pass your image to the machine learning model
# and return the top result with the highest confidence
def classify():
    key = "cee703e0-61d7-11e9-9ab5-eb5cc261c27d948af8fb-30e7-4ae1-b552-86c94eaeedff"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : getWebcamImageData() })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()


demo = classify()

label = demo["class_name"]
confidence = demo["confidence"]


# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))

drone = tellopy.Tello()
try:
	drone.connect()
	drone.wait_for_connection(60.0)
	if label == "takeoff":
		drone.takeoff()
		sleep(5)
	elif label == "land":
		drone.land()
		sleep(5)
except Exception as ex:
	print(ex)
finally:
	drone.quit()   

             
