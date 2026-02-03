from flask import Blueprint,request,make_response
from app.services.users import authenticate_user_service
from app.services.jwt import create_jwt_service,decode_jwt_service,get_user_data_from_redis_service
idm_bp = Blueprint("idm_bp", __name__)
@idm_bp.route("/token", methods=["POST","GET"])
def manage_token(request=request):
  if request.method == "POST":  
    body = request.get_json()
    try:
        is_authenticated = authenticate_user_service(**body)
        if is_authenticated:
            data = get_user_data_from_redis_service(body.get("username"))
            token = create_jwt_service(body.get("username"),options= data) 
            responce = make_response({"message": f"{token}"}, 200)
            responce.set_cookie(key = "idm-token", value = token, max_age = 3600, expires = None, path = '/', domain = None,  secure = None, httponly = False)
            responce.set_cookie(key = "org", value = data.get("org"), max_age = 3600, expires = None, path = '/', domain = None,  secure = None, httponly = False)
            return responce
        else:
            return {"error": "Invalid credentials"}, 401
    except ValueError as e:
        return {"error": str(e)}, 400
  if request.method == "GET":
     cookie = request.cookies.get("idm-token")
     try :
        decoded = decode_jwt_service(cookie)
        return decoded, 200  
     except Exception as e:
         return {"error": str(e)}, 400   
