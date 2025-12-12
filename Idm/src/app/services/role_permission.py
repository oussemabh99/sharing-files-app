from app.models.models import Permission, RolePermission,Role
import app.repository.rolePermission_repo as rp_perm
import app.repository.role_repo as role_repo
import app.repository.permission_repo as perm_repo
def create_role_permission_service(**kwargs) -> str:
    role_name = kwargs.get("role_name")
    permission_name = kwargs.get("permission_name")
    if not role_name or not permission_name:
        raise ValueError("Both role_uuid and permission_uuid are required.")
    try :
     new_role_permission = rp_perm.create_role_permission(
        role_uuid=role_repo.get_role_by_name(role_name), 
        permission_uuid=perm_repo.get_permission_by_name(permission_name)
     )
    except Exception as e:
        raise ValueError("Error creating role-permission: " + str(e))
    return new_role_permission.uuid
