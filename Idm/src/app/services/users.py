from app.models.models import User
import app.repository.user_repo as user
import app.repository.org_repo as org
def get_user_service() -> User:
    
   
    users = user.get_user_all()         
    users_data = [
                {
                    "uuid": user.uuid,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "organisation_uuid": org.get_organisation_by_uuid(user.organisation_uuid),
                    "date_created": user.date_created.isoformat()
                    
                }
                for user in users
            ]
    return {"users": users_data}
def create_user_service(**kwargs) -> str:
    email = kwargs.get("email")
    username = kwargs.get("username")
    organisation= kwargs.get("organisation")
    first_name = kwargs.get("first_name", "")
    last_name = kwargs.get("last_name", "")
    password = kwargs.get("password")
    organisation_uuid = org.get_organisation_uuid_by_name(organisation)
    if not organisation_uuid:
        raise ValueError(f"Organisation '{organisation}' does not exist.")
    if not password:
        raise ValueError("Password is required.")
    if not username:
        raise ValueError("Username is required.")
    if (user.get_user_by_username(username)!=None):
        raise ValueError(f"Username '{username}' is already taken.")
    try :
     new_user = user.create_user(
        email=email,
        first_name=first_name,
        name=username,
        last_name=last_name,
        organisation_uuid=organisation_uuid,
        password=password
     )
    except Exception :
        raise ValueError("Error creating user")
    return new_user.username 
def get_user_by_username_service(username: str) -> User | None:
    new_user = user.get_user_by_uuid(username)
    if not new_user:
        raise ValueError(f"User not found.")
    user_data = {
        "name": new_user.username,
        "email": new_user.email,
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "date_created": new_user.date_created.isoformat(),
        "date_modified": new_user.date_modified.isoformat()
        }
    return user_data
def update_user_service(uuid :str,**kwargs) -> str:
    dict = {}
    if user.get_user_by_uuid(uuid) is None :
        raise ValueError("User not found")
    if kwargs.get("first_name") :
      dict["first_name"] = kwargs.get("first_name")
    if kwargs.get("last_name") :
      dict["last_name"] = kwargs.get("last_name")
    if kwargs.get("email") :
      dict["email"] = kwargs.get("email")
    try :
     new_user = user.update_user(
        user_uuid=uuid,
        **dict
     )
    except Exception :
        raise ValueError("Error updating user")
    return new_user.uuid
def delete_user_service(uuid: str) -> None:
    if user.get_user_by_uuid(uuid) is None :
        raise ValueError("User not found")
    try :
     result = user.delete_user(
        user_uuid=uuid
     )
    except Exception :
        raise ValueError("Error deleting user")
    return True