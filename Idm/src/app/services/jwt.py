import app.repository.jwt_repo as jwt_repo
import app.services.redis as redis_service
def get_user_data_from_redis_service(username: str) -> dict:
    try:
        user_data = redis_service.get_user_data(username)
    except Exception as e:
        print("Error in get_user_data_from_redis_service:", str(e))
        raise e
    return user_data
def create_jwt_service(user,options: dict = {}) -> str:
   try :
    jwt_token = jwt_repo.create_jwt(user,options)
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