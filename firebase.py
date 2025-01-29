
import firebase_admin

from firebase_admin import credentials, firestore


cred = credentials.Certificate(
    "./amar-chatgpt-bot-firebase-adminsdk-fbsvc-c093c9b281.json")

app = firebase_admin.initialize_app(cred)

db = firestore.client()
