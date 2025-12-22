from app.Models.models import Role,Group,GroupRole
from app.Extensions.db import SessionLocal
def group_roles(name : str) -> list[Role]:
    session = SessionLocal()
    roles = session.query(Role.name).filter(Role.uuid==GroupRole.role_uuid).filter(Group.uuid==GroupRole.group_uuid).filter(Group.name==name).all()
    session.close()
    return roles
