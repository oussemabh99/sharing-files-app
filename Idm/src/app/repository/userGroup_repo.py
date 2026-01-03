from app.extensions.db import SessionLocal
from app.models.models import UserGroup
import uuid
import datetime
def verify_group_role_exists(group_uuid: str, user_uuid: str) -> bool:
    session = SessionLocal()
    group_role = session.query(UserGroup).filter(
        UserGroup.group_uuid == group_uuid,
        UserGroup.user_uuid == user_uuid
    ).first()
    session.close()
    return group_role is not None
def create_user_group(group_uuid: str, user_uuid: str) -> UserGroup:
    session = SessionLocal()
    new_group_role = UserGroup(
        uuid=str(uuid.uuid4()),
        group_uuid=group_uuid,
        user_uuid=user_uuid,
        date_created=datetime.datetime.utcnow()
    )
    try:
        session.add(new_group_role)
        session.commit()
        session.refresh(new_group_role)
        session.close()
    except Exception as e:
        session.rollback()
        session.close()
        raise e
    return new_group_role
def get_group_role_from_user(group_uuid: str) -> list[UserGroup]:
    session = SessionLocal()
    group_roles = session.query(UserGroup).filter(
        UserGroup.group_uuid == group_uuid
    ).all()
    session.close()
    return group_roles
def get_group_role_all() -> list[UserGroup]:
    session = SessionLocal()
    group_roles = session.query(UserGroup).all()
    session.close()
    return group_roles
def delete_group_role(group_uuid: str, role_uuid: str) -> None:
    session = SessionLocal()
    group_role = session.query(UserGroup).filter(
        UserGroup.group_uuid == group_uuid,
        UserGroup.role_uuid == role_uuid
    ).first()
    if not group_role:
        session.close()
        raise ValueError("Group-Role association does not exist")
    try:
        session.delete(group_role)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        session.close()
        raise e
def delete_user_from_group(group_uuid: str, user_uuid: str) -> None:
    session = SessionLocal()
    user_group = session.query(UserGroup).filter(
        UserGroup.group_uuid == group_uuid,
        UserGroup.user_uuid == user_uuid
    ).first()
    if not user_group:
        session.close()
        raise ValueError("User-Group association does not exist")
    try:
        session.delete(user_group)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        session.close()
        raise e