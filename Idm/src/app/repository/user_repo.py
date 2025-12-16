from app.extensions.db import SessionLocal
from app.models.models import User
import uuid
import hashlib
import datetime
def create_user(email: str, first_name: str,name:str,last_name: str, organisation_uuid: str,password: str) -> User:
    print("Creating user with email:", email)
    session = SessionLocal()
    new_user = User(
        uuid=str(uuid.uuid4()),
        username=name,
        email=email,
        first_name=first_name,
        last_name=last_name,
        date_created=datetime.datetime.now(),
        date_modified=datetime.datetime.now(),
        organisation_uuid=organisation_uuid,
        password_hash=hashlib.sha256(password.encode()).hexdigest()
    )
    try :
      session.add(new_user)
      session.commit()
      session.refresh(new_user)
      print("User created with UUID:", new_user.uuid)
      session.close()
    except Exception as e:
      session.rollback()
      session.close()
      raise e
    return new_user
def get_user_by_uuid(user_uuid: str) -> User | None:
    session = SessionLocal()
    user = session.query(User).filter(User.uuid == user_uuid).first()
    session.close()
    return user
def get_user_by_username(username: str) -> User | None:
    session = SessionLocal()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user.uuid if user else None
def get_user_all() -> list[User]:
    session = SessionLocal()
    users = session.query(User).all()
    session.close()
    return users
def update_user(user_uuid: str, **kwargs) -> User | None:
    session = SessionLocal()
    user = session.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        session.close()
        return None
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    user.date_modified = datetime.datetime.now()
    try:
        session.commit()
        session.refresh(user)
        session.close()
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    return user
def delete_user(user_uuid: str) -> bool:
    session = SessionLocal()
    user = session.query(User).filter(User.uuid == user_uuid).first()
    if not user:
        session.close()
        return False
    try:
        session.delete(user)
        session.commit()
        session.close()
        return True
    except Exception as e:
        session.rollback()
        session.close()
        raise e
def compare_password(user: str, password: str) -> bool | None:
    session = SessionLocal()
    existing_user = session.query(User).filter(User.username == user).first()
    if not existing_user:
        session.close()
        raise ValueError("User not found.")
    else:
        if existing_user.password_hash == hashlib.sha256(password.encode()).hexdigest():
            session.close()
            return True
        else:
            session.close()
            raise ValueError("Incorrect password.")
         
