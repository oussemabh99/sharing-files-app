import redis
from dotenv import load_dotenv
import os
import json
load_dotenv()
REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PORT = os.getenv('REDIS_PORT')
def get_user_data(username: str) -> dict:
    try:
        r = redis.Redis(host=REDIS_SERVER, port=REDIS_PORT, decode_responses=True)
        user_data = r.get(username)
        if user_data:
            user_data = json.loads(user_data)
        if not user_data:
            raise ValueError("User not found in Redis")
        return user_data
    except Exception as e:
        print(f"Error retrieving user data from Redis: {str(e)}")
        raise e