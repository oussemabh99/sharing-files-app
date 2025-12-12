from sqlalchemy import  Column, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
Base = declarative_base()
class Organisation(Base):
    __tablename__ = 'organisation'
    uuid = Column(String(128), primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    groups = relationship("Group", back_populates="organisation")
    users = relationship("User", back_populates="organisation")
class Group(Base):
    __tablename__ = 'group'
    uuid = Column(String(128), primary_key=True)
    name = Column(String(128), nullable=False, unique=True)
    display_name = Column(String(64), nullable=False)
    organisation_uuid = Column(String(128), ForeignKey('organisation.uuid'), nullable=False)
    organisation = relationship("Organisation", back_populates="groups")
    date_created = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False)
class User(Base):
    __tablename__ = 'user'
    uuid = Column(String(128), primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    email = Column(String(512), nullable=False, unique=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    organisation_uuid = Column(String(128), ForeignKey('organisation.uuid'), nullable=False)
    organisation = relationship("Organisation", back_populates="users")
    date_created = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False)
    password_hash = Column(String(256), nullable=False)
class Role(Base):
    __tablename__ = 'role'
    uuid = Column(String(128), primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(256))
    date_created = Column(DateTime, nullable=False)
    date_modified = Column(DateTime, nullable=False)
class GroupRole(Base):
    __tablename__ = 'group_role'
    uuid = Column(String(128), primary_key=True)
    group_uuid = Column(String(128), ForeignKey('group.uuid'), nullable=False)
    role_uuid = Column(String(128), ForeignKey('role.uuid'), nullable=False)
    date_created = Column(DateTime, nullable=False)
class UserRole(Base):
    __tablename__ = 'user_role'
    uuid = Column(String(128), primary_key=True)
    user_uuid = Column(String(128), ForeignKey('user.uuid'), nullable=False)
    role_uuid = Column(String(128), ForeignKey('role.uuid'), nullable=False)
class UserGroup(Base):
    __tablename__ = 'user_group'
    uuid = Column(String(128), primary_key=True)
    user_uuid = Column(String(128), ForeignKey('user.uuid'), nullable=False)
    group_uuid = Column(String(128), ForeignKey('group.uuid'), nullable=False)
    date_created = Column(DateTime, nullable=False)
class Permission(Base):
    __tablename__ = 'permission'
    uuid = Column(String(128), primary_key=True)
    name = Column(String(32), nullable=False, unique=True)
    description = Column(String(256))
class RolePermission(Base):
    __tablename__ = 'role_permission'
    uuid = Column(String(128), primary_key=True)
    role_uuid = Column(String(128), ForeignKey('role.uuid'), nullable=False)
    permission_uuid = Column(String(128), ForeignKey('permission.uuid'), nullable=False)


