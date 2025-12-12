from app.extensions.db import SessionLocal
from app.models.models import Organisation
import uuid
def create_organisation(name: str) -> Organisation:
    print("Creating organisation with name:", name)
    session = SessionLocal()
    new_organisation = Organisation(
        uuid=str(uuid.uuid4()),
        name=name
    )
    try :
      session.add(new_organisation)
      session.commit()
      session.refresh(new_organisation)
      print("Organisation created with UUID:", new_organisation.uuid)
      session.close()
    except Exception as e:
      session.rollback()
      session.close()
      raise e
    return new_organisation
def get_organisation_all() -> list[Organisation]:
    session = SessionLocal()
    organisations = session.query(Organisation).all()
    session.close()
    return organisations
def get_organisation_by_uuid(organisation_uuid: str) -> str | None:
    session = SessionLocal()
    organisation = session.query(Organisation).filter(Organisation.uuid == organisation_uuid).first()
    session.close()
    return organisation.name if organisation else None
def get_organisation_uuid_by_name(name: str) -> str | None:
    session = SessionLocal()
    organisation = session.query(Organisation).filter(Organisation.name == name).first()
    session.close()
    return organisation.uuid if organisation else None