from app.models.models import Role
from app.repository.role_repo import create_role, get_role_all
def create_role_service(**kwargs) -> str:
    name = kwargs.get("name")
    description = kwargs.get("description", "")
    if not name:
        raise ValueError("Role name is required.")
    try :
     new_role = create_role(
        name=name,
        description=description
        
     )
    except Exception as e :
        raise ValueError(f"Error creating role{e}")
    return new_role.name
def get_role_all_service() -> list[Role]:
    roles = get_role_all()
    roles_data = {"roles":[
        {
            "uuid": role.uuid,
            "name": role.name,
            "description": role.description
        }
        for role in roles
    ]}
    return roles_data
