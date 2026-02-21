from flask import Blueprint,request
from app.services.users import get_user_in_organisation_service,create_user_service,check_user_in_organisation_service,get_user_by_username_service,update_user_service,delete_user_service,get_user_from_username_service
from app.services.org import get_organisation_uuid_by_name_service
from app.services.groupeuser import add_user_to_group_service,get_users_in_group_service,get_all_users_in_groups_service,delete_user_from_group_service,verify_user_in_group_service,get_groups_of_user_service
from app.services.groupeRole import create_group_role_service,delete_group_role_service,get_group_role_inside_organisation_service,get_roles_of_group_service
from app.services.group import get_group_in_organisation_service,create_group_service,check_group_in_organisation_service,get_group_by_name_service
from app.services.jwt import decode_jwt_service
from app.services.check_permission_for_tenant import compare_permission_service
tenant_bp = Blueprint("tenant_bp", __name__)
@tenant_bp.before_request
def check_org(request=request):
    cookie_org = request.cookies.get("org")
    if not cookie_org:
        return {"error": "Organization information is missing in the request."}, 400
    try :
      org= request.path.split("/")[4]
      if org != cookie_org:
        return {"error": "Organization information in the request does not match the authenticated user's organization."}, 403
    except Exception as e:
        return {"error": "Invalid request path. Organization information is missing."}, 400
def check_jwt_key(request=request):
    try :
     org = request.path.split("/")[4]
     cookie = request.cookies.get("idm-token")
     decoded = decode_jwt_service(cookie)
     print(decoded["permissions"])   
     if (compare_permission_service(request = request.method,path = request.path,permissions=decoded["permissions"],org=org)==False):
         return {"error": "No permission to access"}, 402 
    except Exception as e:
         return {"error": "Not Authorized"}, 402 
@tenant_bp.route("/example", methods=["GET"])
def example_route(org):
    return {"message": f"This is an example route for tenant-specific {org}"}, 200
@tenant_bp.route("/users", methods=["POST", "GET"])
def tenant_users(org):
    if request.method == "GET":
        try:
            users = get_user_in_organisation_service(get_organisation_uuid_by_name_service(org))
            return users, 200
        except Exception as e:
            return {"error": str(e)}, 400
    if request.method == "POST":
        try:
            data = request.json
            data["organisation"] = org
            new_user = create_user_service(**data)
            return {"message": "User created succesfully "}, 201
        except Exception as e:
            return {"error": str(e)}, 400
@tenant_bp.route("/users/<id>", methods=["GET", "PUT", "DELETE"])
def tenant_user_detail(org, id):
    if request.method == "GET":
        try:
          checking = check_user_in_organisation_service(id, org)
          if not checking:
            return {"error": "User not found in this organisation."}, 404
          user = get_user_by_username_service(id)
          return user, 200
        except ValueError as e:
             return {"error": str(e)}, 404 
    if request.method == "PUT":
        try:
          checking = check_user_in_organisation_service(id, org)
          if not checking:      
            return {"error": "User not found in this organisation."}, 404
          body = request.get_json()
          updated_username = update_user_service(id, **body)
          return {"message": "User updated successfully"}, 200
        except ValueError as e:
                return {"error": str(e)}, 400
    if request.method == "DELETE":
        try:
          checking = check_user_in_organisation_service(id, org)
          if not checking:      
            return {"error": "User not found in this organisation."}, 404
          delete_user_service(id)
          return {"message": "User deleted successfully"}, 200
        except ValueError as e:
            return {"error": str(e)}, 400
@tenant_bp.route("/groups", methods=["GET","POST"])
def tenant_groups(org):
    if request.method == "GET":
        try:
            groups = get_group_in_organisation_service(get_organisation_uuid_by_name_service(org))
            return groups, 200
        except Exception as e:
            return {"error": str(e)}, 400
    elif request.method == "POST":
        try:
            body = request.get_json()
            body["organisation_uuid"] = get_organisation_uuid_by_name_service(org)
            new_group = create_group_service(**body)
            return {"message": f"Group {new_group} created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
@tenant_bp.route("/groups/assign", methods=["GET","POST","DELETE"])
def tenant_group_roles(org):
    if request.method == "GET":
        try:
            roles = get_group_role_inside_organisation_service(get_organisation_uuid_by_name_service(org))
            if not roles:
                return {"message": "No group roles found in this organisation."}, 200
            return roles, 200
        except Exception as e:
            return {"error": str(e)}, 400
    if request.method == "POST":
        try:
            body = request.get_json()
            group_uuid = get_group_by_name_service(body.get("group_name"))
            checking = check_group_in_organisation_service(group_uuid, get_organisation_uuid_by_name_service(org))
            if not checking:
                return {"error": "Group not found in this organisation."}, 404
            body["organisation_uuid"] = get_organisation_uuid_by_name_service(org)
            print(body)
            new_group_role = create_group_role_service(**body)
            return {"message": f"Group role created successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 400
    if request.method == "DELETE":
        try:
            body = request.get_json()
            group_uuid = get_group_by_name_service(body.get("group_name"))
            checking = check_group_in_organisation_service(group_uuid, get_organisation_uuid_by_name_service(org))
            if not checking:
                return {"error": "Group not found in this organisation."}, 404
            delete_group_role_service(**body)
            return {"message": f"Group role deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400    
@tenant_bp.route("/groupuser", methods=["POST","DELETE"])
def tenant_group_users(org):
    if request.method == "POST":
        try:
            body = request.get_json()
            verify = verify_user_in_group_service(**body)
            if verify:
                return {"error": "User is already in the group."}, 400
            user_uuid = get_user_from_username_service(body.get("user_name"))
            group_uuid = get_group_by_name_service(body.get("group_name"))
            checking_group = check_group_in_organisation_service(group_uuid, get_organisation_uuid_by_name_service(org))
            if not checking_group:
                return {"error": "Group not found in this organisation."}, 404
            checking_user = check_user_in_organisation_service(user_uuid, org)
            if not checking_user:
                return {"error": "User not found in this organisation."}, 404
            new_group_user = add_user_to_group_service(**body)
            return {"message": f"User added to group successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 400  
    if request.method == "DELETE":
        try:
            body = request.get_json()
            user_uuid = get_user_from_username_service(body.get("user_name"))
            group_uuid = get_group_by_name_service(body.get("group_name"))
            checking_group = check_group_in_organisation_service(group_uuid, get_organisation_uuid_by_name_service(org))
            if not checking_group:
                return {"error": "Group not found in this organisation."}, 404
            checking_user = check_user_in_organisation_service(user_uuid, org)
            if not checking_user:
                return {"error": "User not found in this organisation."}, 404
            delete_user_from_group_service(**body)
            return {"message": f"User deleted from group successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 400  
@tenant_bp.route("/user/<user_name>/groups", methods=["GET"])
def tenant_get_group_users(org, user_name):
    if request.method == "GET":
        try:
            user_uuid = get_user_from_username_service(user_name)
            checking_user = check_user_in_organisation_service(user_uuid, org)
            if not checking_user:
                return {"error": "User not found in this organisation."}, 404
            groups = get_groups_of_user_service(**{"user_name": user_name})
            if not groups:
                return {"message": "User is not in any groups."}, 200
            return groups, 200
        except Exception as e:
            return {"error": str(e)}, 400
@tenant_bp.route("/group/<group_name>/roles", methods=["GET"])
def tenant_get_roles_of_group(org, group_name):
    if request.method == "GET":
        try:
            group_uuid = get_group_by_name_service(group_name)
            checking_group = check_group_in_organisation_service(group_uuid, get_organisation_uuid_by_name_service(org))
            if not checking_group:
                return {"error": "Group not found in this organisation."}, 404
            roles = get_roles_of_group_service(group_name)
            if not roles:
                return {"message": "No roles found for this group."}, 200
            return roles, 200
        except Exception as e:
            return {"error": str(e)}, 400
  


    