from random import randint
from flask import request
import utils.jwt_token as jwt_token
import utils.mail as mail_helper

def gen_access_token(user):
  return jwt_token.generate_token(user.as_dict())

def decode_token(vcode):
  return jwt_token.decode_token(vcode)

# generating and sending verification link to the respective user's email

def send_verification_mail(user):  
  vlink = _gen_verication_link(user)
  mail_helper.send_mail(user.email, vlink)
  
def _gen_verication_link(user):
  nonce = str(randint(1000, 100000))

  vcode = jwt_token.generate_token({
    'email': user.email,
    'nonce': nonce
  })

  vlink = request.url_root + "auth/verify" + "?vcode=" + vcode + "&nonce=" + nonce

  return vlink

