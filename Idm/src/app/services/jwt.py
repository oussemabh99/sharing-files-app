import app.repository.jwt_repo as jwt_repo
import datetime
import uuid
def create_jwt_service(user,options: dict = {}) -> str:
   try :
    jwt_token = jwt_repo.create_jwt(user)
   except Exception as e:
       print("Error in create_jwt_service:", str(e))
       raise e
   return jwt_token