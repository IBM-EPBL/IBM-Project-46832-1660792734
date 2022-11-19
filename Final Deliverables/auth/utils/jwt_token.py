import jwt
from keys import SERVER_SECRET

def generate_token(payload):    
  return jwt.encode(payload, SERVER_SECRET, algorithm="HS256")

def decode_token(token):    
    return jwt.decode(token, SERVER_SECRET, algorithms=["HS256"])