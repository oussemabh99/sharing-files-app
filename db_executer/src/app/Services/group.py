import app.Repository.group_repo as grp_repo
import app.Repository.role_repo as role_repo
def get_permission_from_group_service(name : str) -> set: 
    try :      
     roles = grp_repo.get_group_roles(name)
     all_permissions = { permission[0] for role in roles for permission in role_repo.get_permission_roles(role[0])}
     return all_permissions
    except Exception as e:
       raise e
    

