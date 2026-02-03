import redis 
from dotenv import load_dotenv
import os
import json
import app.Services.user as user_service
load_dotenv()
REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PORT = os.getenv('REDIS_PORT')
def delete_user_data_redis(username : str) -> None :
  with redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, decode_responses=True) as redis_client:
    try :
      redis_client.delete(username)
    except Exception as e:
       raise e
def set_user_data_redis(username : str) -> None :
  with redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, decode_responses=True) as redis_client:
    try :
      user_data = user_service.get_user_data_service(username)
      redis_client.set(username,json.dumps(user_data))
    except Exception as e:
       raise e
users = user_service.get_all_users_service()
for user in users :
    set_user_data_redis(user[0])