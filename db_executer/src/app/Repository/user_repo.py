from app.Models.models import User,Role,UserRole,Group,UserGroup,Organisation
from app.Extensions.db import SessionLocal
def get_user_role(name : str) -> list[Role] :
    session = SessionLocal()
    roles = session.query(Role.name).filter(Role.uuid == UserRole.role_uuid).filter(User.uuid == UserRole.user_uuid).filter(User.username == name).all()
    session.close()
    return roles
def get_user_groups(name :str)-> list[Group] :
    session = SessionLocal()
    groups = session.query(Group.name).filter(Group.uuid == UserGroup.group_uuid).filter(User.uuid == UserGroup.user_uuid).filter(User.username == name).all()
    session.close()
    return groups
def get_user_organisation_name(name : str) -> str :
    session = SessionLocal()
    organisation = session.query(Organisation.name).filter(Organisation.uuid == User.organisation_uuid).filter(User.username == name).first()
    session.close()
    return organisation[0]
def get_all_users() -> list[str] :
    session = SessionLocal()
    users = session.query(User.username).all()
    session.close()
    return users