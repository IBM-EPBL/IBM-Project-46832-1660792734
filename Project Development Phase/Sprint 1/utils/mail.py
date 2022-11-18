from trycourier import Courier
from keys import COURIER_AUTH_KEY

client = Courier(auth_token=COURIER_AUTH_KEY)

def send_mail(to_email, vlink):
  try:
    client.send_message(
      message={
        "to": {
          "email": to_email,
        },
        "template": "GAK0QGGS43MFF6GZ4MB3MHT8NKG8",
        "data": {
          "vlink": vlink,
        },
      }
    )
  except:
    pass
  finally:
    print(vlink)