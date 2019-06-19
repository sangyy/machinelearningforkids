#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests, sys
from time import sleep
import tellopy
# Gets the contents of an image file to be sent to the
# machine learning model for classifying
def getImageFileData(locationOfImageFile):
    with open(locationOfImageFile, "rb") as f:
        data = f.read()
        if sys.version_info[0] < 3:
            # Python 2 approach to handling bytes
            return data.encode("base64")
        else:
            # Python 3 approach to handling bytes
            import base64
            return base64.b64encode(data).decode()


# This function will pass your image to the machine learning model
# and return the top result with the highest confidence
def classify(imagefile):
    key = "d69f9360-9272-11e9-af13-ff972459e739b25e3836-a1de-4028-a8c6-0db893451b15"
    url = "https://machinelearningforkids.co.uk/api/scratch/"+ key + "/classify"

    response = requests.post(url, json={ "data" : getImageFileData(imagefile) })

    if response.ok:
        responseData = response.json()
        topMatch = responseData[0]
        return topMatch
    else:
        response.raise_for_status()

'''
# CHANGE THIS to the name of the image file you want to classify
demo = classify("test.jpg")

label = demo["class_name"]
confidence = demo["confidence"]


# CHANGE THIS to do something different with the result
print ("result: '%s' with %d%% confidence" % (label, confidence))

'''

drone = tellopy.Tello()
try:
    drone.connect()
    drone.wait_for_connection(60.0)
    demo = classify("test.jpg")

    label = demo["class_name"]
    confidence = demo["confidence"]


    # CHANGE THIS to do something different with the result
    print ("result: '%s' with %d%% confidence" % (label, confidence))
    
    if label == "military":
        drone.takeoff()
        sleep(5)
        drone.flip_forward()
        sleep(5)
        drone.land()
        print("mission complete")
        sleep(5)
    else:
        print("safe now")
        sleep(5)
        

except Exception as ex:
    print(ex)
finally:
    print('Shutting down connection to drone...')
    drone.quit()   
