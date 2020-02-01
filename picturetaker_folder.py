import requests
import base64
import io
from PIL import Image
imageUrl = 'https://azurestudenttrain.azurewebsites.net/image'
imagepath = 'C:\\Trainings\MoodDetector\\images\\happy1.jpg'

def check_sadness(emotions):
    if 'sadness' in emotions:
        if emotions['sadness'] >= 3:
            print('Are you feeling ok? Do you want to talk about it?')

def upload():
    data = {}
    img = Image.open(imagepath)
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    data['image'] = base64.b64encode(imgByteArr).decode()
    results = requests.post(url=imageUrl, json=data)
    check_sadness(results.json())

upload()