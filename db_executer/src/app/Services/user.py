import app.Repository.user_repo as user_repo
import app.Repository.role_repo as role_repo
import app.Services.group as grp
def get_user_permission_service(name : str) -> set :
    all_permissions = set()
    try :
     roles = user_repo.get_user_role(name)
     all_permissions = { permission[0] for role in roles for permission in role_repo.get_permission_roles(role[0])}
     return all_permissions
    except Exception as e:
       raise e
def get_user_groups_permissions(name : str) -> set :
    all_permissions = set()
    try :
     groups = user_repo.get_user_groups(name)
     for group in groups :
       all_permissions=grp.get_permission_from_group_service(group[0]).union(all_permissions)
     return all_permissions
    except Exception as e:
       raise e
def user_update_service(name : str)-> set :
    try :
     user_permission = get_user_permission_service(name)
     user_group = get_user_groups_permissions(name)
     return user_permission.union(user_group)
    except Exception as e:
       raise e

