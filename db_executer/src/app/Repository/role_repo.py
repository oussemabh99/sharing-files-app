from app.Models.models import Role,Permission,RolePermission
from app.Extensions.db import SessionLocal
def get_permission_roles(name : str) -> list[Permission]:
    session = SessionLocal()
    roles = session.query(Permission.name).filter(Permission.uuid==RolePermission.permission_uuid).filter(RolePermission.role_uuid==Role.uuid).filter(Role.name==name).all()
    session.close()
    return(roles)
#print(get_permission_roles(name = "Administrator"))