import app.repository.jwt_repo as jwt_repo
def create_jwt_service(user,options: dict = {}) -> str:
   try :
    jwt_token = jwt_repo.create_jwt(user)
   except Exception as e:
       print("Error in create_jwt_service:", str(e))
       raise e
   return jwt_token
def decode_jwt_service(token: str) -> dict:
    try :
        decoded_payload = jwt_repo.decode_jwt(token)
    except Exception as e:
        print("Error in decode_jwt_service:", str(e))
        raise e
    return decoded_payload