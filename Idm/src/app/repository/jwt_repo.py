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
       "permissions": option.get("permissions",[]),
       "org": "bo"
   }
   try :
    token = jwt.jwt_api.encode(payload, jwt.private_pem, algorithm="RS256")
   except Exception as e:
       print("Error generating JWT:", str(e))
       raise e
   return token
