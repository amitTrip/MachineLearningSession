import cv2
import requests
import base64
imageUrl = 'https://azurestudenttrain.azurewebsites.net/image'

def check_sadness(emotions):
    if 'sadness' in emotions:
        if emotions['sadness'] >= 3:
            print('Are you feeling ok? Do you want to talk about it?')

def upload(frame):
    data = {}
    img = cv2.imencode('.jpg', frame)[1]
    data['image'] = base64.b64encode(img).decode()
    results = requests.post(url=imageUrl, json=data)
    check_sadness(results.json())

cv2.namedWindow('Press space to take a photo')
cam = cv2.VideoCapture(0)


while True:
    ret, frame = cam.read()
    cv2.imshow('Press space to take a photo', frame)
        
    key = cv2.waitKey(1)
    if key%256 == 32:
        upload(frame)
        break

cam.release()
cv2.destroyAllWindow()