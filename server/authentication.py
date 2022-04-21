import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

credjson = {
  "type": "service_account",
  "project_id": "fallguys-c4e9b",
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY'),
  "client_email": "firebase-adminsdk-k5lql@fallguys-c4e9b.iam.gserviceaccount.com",
  "client_id": "117028498074544091262",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-k5lql%40fallguys-c4e9b.iam.gserviceaccount.com"
}

cred = credentials.Certificate(credjson)
firebase_admin.initialize_app(cred)

def login(email: str, password: str):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": True
    })

    r = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword',
        params={ "key": 'AIzaSyDj-SN1xtH1ubFSenXryImXQ69xHQFVJNg' },
        data=payload)

    return r.json()

def new(email: str, password: str):
    user = auth.create_user(email = email, password = password)
    return user

def passwordreset(email : str):
    link = auth.generate_password_reset_link(email)
    return link
