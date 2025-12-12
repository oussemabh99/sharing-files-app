from app.extensions.db import SessionLocal
from app.models.models import Permission
import uuid
def create_permission(name: str, description: str) -> Permission:
    print("Creating permission with name:", name)
    session = SessionLocal()
    new_permission = Permission(
        uuid=str(uuid.uuid4()),
        name=name,
        description=description
    )
    try :
      session.add(new_permission)
      session.commit()
      session.refresh(new_permission)
      print("Permission created with UUID:", new_permission.uuid)
      session.close()
    except Exception as e:
      session.rollback()
      session.close()
      raise e
    return new_permission
def get_permission_by_uuid(permission_uuid: str) -> Permission | None:
    session = SessionLocal()
    permission = session.query(Permission).filter(Permission.uuid == permission_uuid).first()
    session.close()
    return permission
def get_permission_all() -> list[Permission]:
    session = SessionLocal()
    permissions = session.query(Permission).all()
    session.close()
    return permissions
def get_permission_by_name(name: str) -> Permission | None:
    session = SessionLocal()
    permission = session.query(Permission).filter(Permission.name == name).first()
    session.close()
    return permission.uuid if permission else None