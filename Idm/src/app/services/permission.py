from app.models.models import Permission
import app.repository.permission_repo as perm
def create_permission_service(**kwargs) -> str:
    name = kwargs.get("name")
    description = kwargs.get("description", "")
    if not name:
        raise ValueError("Permission name is required.")
    try :
     new_permission = perm.create_permission(
        name=name,
        description=description
     )
    except Exception :
        raise ValueError("Error creating permission")
    return new_permission.name
def get_permission_by_uuid_service(permission_uuid: str) -> Permission | None:
    new_permission = perm.get_permission_by_uuid(permission_uuid)
    if not new_permission:
        raise ValueError(f"Permission not found.")
    permission_data = {
        "name": new_permission.name,
        "description": new_permission.description,
        "date_created": new_permission.date_created.isoformat(),
        "date_modified": new_permission.date_modified.isoformat()
    }
    return permission_data
def get_permission_service() -> Permission:
    try:
     permissions = perm.get_permission_all()         
     permissions_data = [
                {
                    "uuid": permission.uuid,
                    "name": permission.name,
                    "description": permission.description,
                    "date_created": permission.date_created.isoformat()
                }
                for permission in permissions
            ]
    except Exception :
        raise ValueError("Error fetching permissions")
    return {"permissions": permissions_data}
def get_permission_by_name_service(name: str) -> Permission | None:
    new_permission = perm.get_permission_by_name(name)
    if not new_permission:
        raise ValueError(f"Permission not found.")
    permission_data = {
        "name": new_permission.name,
        "description": new_permission.description,
        "date_created": new_permission.date_created.isoformat(),
        "date_modified": new_permission.date_modified.isoformat()
    }
    return permission_data
def get_permission_all_service() -> list[Permission]:
    permissions = perm.get_permission_all()
    permissions_data = {"permissions":[
        {
            "uuid": permission.uuid,
            "name": permission.name,
            "description": permission.description
        }
        for permission in permissions
    ]
    }
    return permissions_data