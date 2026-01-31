import redis 
from dotenv import load_dotenv
import os
import json
import app.Services.user as user_service
load_dotenv()
REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PORT = os.getenv('REDIS_PORT')
redis_client = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, decode_responses=True)
def set_user_data_redis(username : str) -> None :
    try :
      user_data = user_service.get_user_data_service(username)
      redis_client.set(username,json.dumps(user_data))
    except Exception as e:
       raise e
set_user_data_redis("admin")