from app.extensions.db import SessionLocal
from app.models.models import GroupRole,Group,Role
import uuid
import datetime
def verify_group_role_exists(group_uuid: str, role_uuid: str) -> bool:
    session = SessionLocal()
    group_role = session.query(GroupRole).filter(
        GroupRole.group_uuid == group_uuid,
        GroupRole.role_uuid == role_uuid
    ).first()
    session.close()
    return group_role is not None
def create_group_role(group_uuid: str, role_uuid: str) -> GroupRole:
    if verify_group_role_exists(group_uuid, role_uuid):
        raise Exception("Group-Role association already exists")
    session = SessionLocal()
    new_group_role = GroupRole(
        uuid=str(uuid.uuid4()),
        group_uuid=group_uuid,
        role_uuid=role_uuid,
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
def get_group_role_all() -> list[GroupRole]:
    session = SessionLocal()
    group_roles = session.query(GroupRole).all()
    session.close()
    return group_roles
def delete_group_role(group_uuid: str, role_uuid: str) -> None:
    session = SessionLocal()
    group_role = session.query(GroupRole).filter(
        GroupRole.group_uuid == group_uuid,
        GroupRole.role_uuid == role_uuid
    ).first()
    if not group_role:
        session.close()
        raise Exception("Group-Role association does not exist")
    try:
        session.delete(group_role)
        session.commit()
        session.close()
    except Exception as e:
        session.rollback()
        session.close()
        raise e
def get_group_role_inside_organisation(organisation_uuid: str) -> list[GroupRole]:
    session = SessionLocal()
    group_roles = session.query(GroupRole).join(
        Group, GroupRole.group_uuid == Group.uuid
    ).filter(
        Group.organisation_uuid == organisation_uuid
    ).all()
    session.close()
    return group_roles
def get_roles_of_group(group_uuid: str) -> list[Role]:
    session = SessionLocal()
    roles = session.query(Role).join(
        GroupRole, Role.uuid == GroupRole.role_uuid
    ).filter(
        GroupRole.group_uuid == group_uuid
    ).all()
    session.close()
    return roles