from app.extensions.db import SessionLocal
from app.models.models import Role
import uuid
import datetime
def create_role(name: str, description: str) -> Role:
    print("Creating role with name:", name)
    session = SessionLocal()
    new_role = Role(
        uuid=str(uuid.uuid4()),
        name=name,
        description=description,
        date_created=datetime.datetime.utcnow(),
        date_modified=datetime.datetime.utcnow()
    )
    try :
      session.add(new_role)
      session.commit()
      session.refresh(new_role)
      print("Role created with UUID:", new_role.uuid)
      session.close()
    except Exception as e:
      session.rollback()
      session.close()
      raise e
    return new_role
def get_role_by_uuid(role_uuid: str) -> Role | None:
    session = SessionLocal()
    role = session.query(Role).filter(Role.uuid == role_uuid).first()
    session.close()
    return role
def get_role_all() -> list[Role]:
    session = SessionLocal()
    roles = session.query(Role).all()
    session.close()
    return roles
def get_role_by_name(name: str) -> Role | None:
    session = SessionLocal()
    role = session.query(Role).filter(Role.name == name).first()
    session.close()
    return role.uuid if role else None
