from flask import Flask, render_template, request, jsonify
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import io
import base64
import azure.cosmos.cosmos_client as cosmos_client
import uuid

app = Flask(__name__)

cosmos_url = 'https://azureworkshopamtripat.documents.azure.com:443/'
cosmos_primary_key = 'dwLEwbU4NjMqAKHa2tDKNwN6ijR7XLT1wn8P29Imc4vAZK6UKMCQpcCuYffmI935WAUQPaBoYmQdZ9c6XCnwfQ=='
cosmos_collection_link = 'dbs/workshop/colls/faces'

client = cosmos_client.CosmosClient(url_connection=cosmos_url, 
                                    auth={'masterKey': cosmos_primary_key})


app = Flask(__name__)

@app.route('/')
def home():
    docs = list(client.ReadItems(cosmos_collection_link))
    return render_template('home.html', result = docs)

face_api_endpoint = 'https://pythonworkshopantripat.cognitiveservices.azure.com/'
face_api_key = 'd8fed775b19842f38fe20f5b9daade2a'
credentials = CognitiveServicesCredentials(face_api_key)
face_client = FaceClient(face_api_endpoint, credentials=credentials)

def best_emotion(emotion):
  emotions = {}
  emotions['anger'] = emotion.anger
  emotions['contempt'] = emotion.contempt
  emotions['disgust'] = emotion.disgust
  emotions['fear'] = emotion.fear
  emotions['happiness'] = emotion.happiness
  emotions['neutral'] = emotion.neutral
  emotions['sadness'] = emotion.sadness
  emotions['surprise'] = emotion.surprise
  return max(zip(emotions.values(), emotions.keys()))[1]


def get_emotions():
    docs = list(client.ReadItems(cosmos_collection_link))
    emotions = [doc['emotion'] for doc in docs]
    counts = dict()
    for emotion in emotions:
        counts[emotion] = counts.get(emotion, 0) + 1

    return jsonify(counts)


@app.route('/image', methods=['POST'])
def upload_image():
    json = request.get_json()
    base64_image = base64.b64decode(json['image'])

    image = io.BytesIO(base64_image)
    faces = face_client.face.detect_with_stream(image,
                                                return_face_attributes=['emotion'])

    for face in faces:
        doc = {
                'id' : str(uuid.uuid4()),
                'emotion': best_emotion(face.face_attributes.emotion)
              }
        client.CreateItem(cosmos_collection_link, doc)

    return get_emotions()