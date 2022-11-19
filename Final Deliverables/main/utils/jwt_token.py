import jwt
from keys import SERVER_SECRET, AUTH_SERVER_URL,AUTH_SERVER_REDIRECT_URL
from flask import request, redirect, session
import requests

def generate_token(payload):    
  return jwt.encode(payload, SERVER_SECRET, algorithm="HS256")

def decode_token(token):    
    return jwt.decode(token, SERVER_SECRET, algorithms=["HS256"])

def validate_token(func):
    def wrapper(*args, **kwargs): 
        try:
            token = request.cookies.get('access-token')   
            if token == None:
              raise Exception()              
            
            res = requests.get(f'{AUTH_SERVER_URL}isvalid?token={token}&ss={SERVER_SECRET}').json()
            
            if res['status'] == True:
                session['user'] = res['user']
                return func(*args, **kwargs)
            else:
                raise res['error']

        except Exception as e:
            print(e)
            return redirect(AUTH_SERVER_REDIRECT_URL)
            
    wrapper.__name__ = func.__name__
    return wrapper