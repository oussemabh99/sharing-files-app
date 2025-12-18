from flask import Blueprint,request
from app.services.users import get_user_service, create_user_service ,get_user_by_username_service,update_user_service,delete_user_service
from app.services.org import get_organisation_service,create_organisation_service
from app.services.permission import create_permission_service,get_permission_all_service 
from app.services.role import create_role_service,get_role_all_service
from app.services.role_permission import create_role_permission_service
from app.services.group import create_group_service, get_group_all_service
from app.services.groupeRole import get_group_role_all_service,create_group_role_service,delete_group_role_service
from app.services.groupeuser import add_user_to_group_service,get_users_in_group_service,get_all_users_in_groups_service
from app.services.jwt import decode_jwt_service
auth_bp = Blueprint("auth_bp", __name__)
@auth_bp.before_request
def check_jwt_key():
   try :
     cookie = request.cookies.get("idm-token")
     decoded = decode_jwt_service(cookie)
   except Exception as e:
         return {"error": "Not Authorized"}, 402   
@auth_bp.route("/users", methods=["POST", "GET"])
def users(request=request):
    if request.method == "GET":
       try:
              users = get_user_service()
              return users, 200
       except Exception as e:
              return {"error": str(e)}, 500     
    elif request.method == "POST":
        body = request.get_json()
        try:
             new_user = create_user_service(**body)
             return {"message": f"User {new_user}created successfully"}, 201
        except ValueError as e:
             return {"error": str(e)}, 400        
@auth_bp.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def user_detail(id,request=request):
   if request.method == "GET":
        try:
             user = get_user_by_username_service(id)
             return user, 200
        except ValueError as e:
             return {"error": str(e)}, 404
   if request.method == "PUT":
        body = request.get_json()
        try:
                updated_username = update_user_service(id, **body)
                return {"message": "User updated successfully"}, 200
        except ValueError as e:
                return {"error": str(e)}, 400
   if request.method == "DELETE":
        try:
            delete_user_service(id)
            return {"message": "User deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400       
@auth_bp.route("/orgs", methods=["GET","POST"])
def orgs(request=request):
    if request.method == "GET":
        try:
             orgs = get_organisation_service()
             return orgs, 200
        except Exception as e:
             return {"error": str(e)}, 400
    elif request.method == "POST":        
        try:
            body = request.get_json()
            new_org = create_organisation_service(**body)
            return {"message": f"Organisation {new_org} created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
@auth_bp.route("/permissions", methods=["GET","POST"])
def permissions(request=request):
    if request.method == "GET":
        try:
             permissions = get_permission_all_service()
             return permissions, 200
        except Exception as e:
             return {"error": str(e)}, 400
    elif request.method == "POST":        
        try:
            body = request.get_json()
            new_permission = create_permission_service(**body)
            return {"message": f"Permission {new_permission}  created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
@auth_bp.route("/roles", methods=["GET","POST"])
def roles():
    if request.method == "POST":
       body = request.get_json()
       try:
            new_role = create_role_service(**body)
            return {"message": f"Role  created successfully"}, 201 
       except Exception as e:
            return {"error": str(e)}, 400
    if request.method == "GET":
         try:
                roles = get_role_all_service()
                return roles, 200
         except Exception as e:
                return {"error": str(e)}, 400     
@auth_bp.route("/roles/assign", methods=["POST"])
def assign_role_permission(request=request):
       body = request.get_json()
       role_name = body.get("role_name")
       permission_name = body.get("permission_name")
       try:
            create_role_permission_service(
                role_name=role_name,
                permission_name=permission_name
            )
            return {"message": f"Role-Permission assigned successfully"}, 201 
       except Exception as e:
            return {"error": str(e)}, 400       
@auth_bp.route("/groups", methods=["GET","POST"])
def groups():
    if request.method == "POST":
       body = request.get_json()
       try:
            create_group_service(**body)
            return {"message": f"Group  created successfully"}, 201 
       except Exception as e:
            return {"error": "error creating groups"}, 400 
    if request.method == "GET":
         try:
                groups = get_group_all_service()
                return groups, 200
         except Exception as e:
                return {"error": "error"}, 400
@auth_bp.route("/groups/assign", methods=["GET","POST","DELETE"])
def assign_group_role(request=request):
    if request.method == "GET":
        try:
         get_group_roles = get_group_role_all_service()
         return get_group_roles, 200
        except Exception as e:
         return {"error": str(e)}, 400
    if request.method == "POST":
       body = request.get_json()
       try:
            create_group_role_service(**body)
            return {"message": f"Group-Role assigned successfully"}, 201 
       except Exception as e:
            return {"error": str(e)}, 400

    if request.method == "DELETE":
       body = request.get_json()
       try:
           
            delete_group_role_service(**body)
            return {"message": f"Group-Role deleted successfully"}, 200 
       except Exception as e:
            return {"error": str(e)}, 400
@auth_bp.route("/groupuser", methods=["GET","POST","DELETE"])
def assign_user_group(request=request):
    if request.method == "POST":
       body = request.get_json()
       try:
            add_user_to_group_service(**body)
            return {"message": f"User added to group successfully"}, 201 
       except Exception as e:
            return {"error": str(e)}, 400

    if request.method == "GET":
       try:
            users_in_group = get_all_users_in_groups_service()
            return users_in_group, 200 
       except Exception as e:
            return {"error": str(e)}, 400