import datetime
import uuid
import app.extensions.jwt  as jwt
def create_jwt(user : str , option : dict = {}) -> str:
   payload = {
       "iss": "IDM_Service",
       "sub": f"{user}",
       "iat": datetime.datetime.now() - datetime.timedelta(hours=1),
       "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
       "jti": str(uuid.uuid4()),
       "permissions": option.get("permissions", []),
       "org": option.get("org","none"),
   }
   try :
    token = jwt.jwt_api.encode(payload, jwt.private_key1, algorithm="RS256")
   except Exception as e:
       print("Error generating JWT:", str(e))
       raise e
   return token
def decode_jwt(token: str) -> dict:
    try :
        decoded_payload = jwt.jwt_api.decode(token, jwt.public_key1, algorithms=["RS256"])
        return decoded_payload
    except Exception as e:
        print("Error decoding JWT:", str(e))
        raise e