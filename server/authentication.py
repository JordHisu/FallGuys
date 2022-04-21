import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
import json
import requests

cred = credentials.Certificate("key.json")
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