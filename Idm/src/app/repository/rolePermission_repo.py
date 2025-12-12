from app.extensions.db import SessionLocal
from app.models.models import RolePermission
import uuid
def get_role_permission_all() -> list[RolePermission]:
    session = SessionLocal()
    role_permissions = session.query(RolePermission).all()
    session.close()
    return role_permissions
def check_role_permission_exists(role_uuid: str, permission_uuid: str) -> bool:
    session = SessionLocal()
    role_permission = session.query(RolePermission).filter(
        RolePermission.role_uuid == role_uuid,
        RolePermission.permission_uuid == permission_uuid
    ).first()
    session.close()
    return role_permission is not None
def create_role_permission(role_uuid: str, permission_uuid: str) -> RolePermission:
    print("Creating role-permission with role UUID:", role_uuid, "and permission UUID:", permission_uuid)
    session = SessionLocal()
    if check_role_permission_exists(role_uuid, permission_uuid):
        session.close()
        raise Exception("Role-Permission association already exists")
    new_role_permission = RolePermission(
        uuid=str(uuid.uuid4()),
        role_uuid=role_uuid,
        permission_uuid=permission_uuid
    )
    try :
      session.add(new_role_permission)
      session.commit()
      session.refresh(new_role_permission)
      session.close()
    except Exception as e:
      session.rollback()
      session.close()
      raise e
    return new_role_permission