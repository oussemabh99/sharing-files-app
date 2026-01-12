from app.models.models import GroupRole,Role
import app.repository.grouprole_repo as group_role_repo
import app.repository.group_repo as group_repo
import app.repository.role_repo as role_repo
def create_group_role_service(**kwargs) -> str:
    group_name = kwargs.get("group_name")
    role_name = kwargs.get("role_name")
    group_uuid = group_repo.get_group_by_name(group_name)
    role_uuid = role_repo.get_role_by_name(role_name)
    if not group_uuid or not role_uuid:
        raise ValueError("Both group_uuid and role_uuid are required.")
    if group_role_repo.verify_group_role_exists(group_uuid, role_uuid):
        raise ValueError("Group-Role association already exists.")
    try :
     new_group_role = group_role_repo.create_group_role(
        group_uuid=group_uuid,
        role_uuid=role_uuid
     )
    except Exception as e:
        raise ValueError("Error creating group-role association: " + str(e))
    return new_group_role.uuid
def get_group_role_all_service() -> list[GroupRole]:
    group_roles = group_role_repo.get_group_role_all()
    group_roles_data = {"group_roles":[
        {
            "group_uuid": group_role.group_uuid,
            "role_uuid": group_role.role_uuid,
            "date_created": group_role.date_created.isoformat()
            
        }
        for group_role in group_roles
    ]}
    return group_roles_data
def delete_group_role_service(**kwargs) -> None:
    group_name = kwargs.get("group_name")
    role_name = kwargs.get("role_name")
    group_uuid = group_repo.get_group_by_name(group_name)
    role_uuid = role_repo.get_role_by_name(role_name)
    if not group_uuid or not role_uuid:
        raise ValueError("Both group_uuid and role_uuid are required.")
    if group_role_repo.verify_group_role_exists(group_uuid, role_uuid)==False:
        raise ValueError("Group-Role association doesent  exists.")
    try :
     group_role_repo.delete_group_role(
        group_uuid=group_uuid,
        role_uuid=role_uuid
     )
    except Exception as e:
        raise ValueError("Error deleting group-role association: " + str(e)) 
def get_group_role_inside_organisation_service(organisation_uuid: str) -> list[GroupRole]:
    group_roles = group_role_repo.get_group_role_inside_organisation(organisation_uuid)
    group_roles_data = {"group_roles":[
        {
            "group_uuid": group_role.group_uuid,
            "role_uuid": group_role.role_uuid,
            "date_created": group_role.date_created.isoformat()
            
        }
        for group_role in group_roles
    ]}
    return group_roles_data
def get_roles_of_group_service(group_name: str) -> list[Role]:
    group_uuid = group_repo.get_group_by_name(group_name)
    if not group_uuid:
        raise ValueError("group_uuid is required.")
    roles = group_role_repo.get_roles_of_group(group_uuid)
    roles_data = {"roles":[
        
            role.name    
        for role in roles
    ]}
    return roles_data
