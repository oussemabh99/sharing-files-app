from app.extensions.db import SessionLocal
from app.models.models import Group
import  uuid 
import datetime
def create_group(name: str, display_name: str, organisation_uuid: str) -> Group:
    print("Creating group with name:", name)
    session = SessionLocal()
    new_group = Group(
        uuid=str(uuid.uuid4()),
        name=name,
        display_name=display_name,
        organisation_uuid=organisation_uuid,
        date_created=datetime.datetime.utcnow(),
        date_modified=datetime.datetime.utcnow()
    )
    try :
      session.add(new_group)
      session.commit()
      session.refresh(new_group)
      print("Group created with UUID:", new_group.uuid)
      session.close()
    except Exception as e:
      session.rollback()
      session.close()
      raise e
    return new_group
def get_group_all() -> list[Group]:
    session = SessionLocal()
    groups = session.query(Group).all()
    session.close()
    return groups
def get_group_by_uuid(group_uuid: str) -> Group | None:
    session = SessionLocal()
    group = session.query(Group).filter(Group.uuid == group_uuid).first()
    session.close()
    return group
def get_group_by_name(name: str) -> Group | None:
    session = SessionLocal()
    group = session.query(Group).filter(Group.name == name).first()
    session.close()
    return group.uuid
def get_group_in_organisation(organisation_uuid: str) -> list[Group]:
    session = SessionLocal()
    groups = session.query(Group).filter(Group.organisation_uuid == organisation_uuid).all()
    session.close()
    return groups
def check_group_in_organisation(group_uuid: str, organisation_uuid: str) -> bool:
    session = SessionLocal()
    group = session.query(Group).filter(
        Group.uuid == group_uuid,
        Group.organisation_uuid == organisation_uuid
    ).first()
    session.close()
    return group is not None