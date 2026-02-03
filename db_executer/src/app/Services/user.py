import app.Repository.user_repo as user_repo
import app.Repository.role_repo as role_repo
import app.Services.group as grp
from concurrent.futures import ThreadPoolExecutor
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
def user_update_service(name : str)-> list :
    try :
     user_permission = get_user_permission_service(name)
     user_group = get_user_groups_permissions(name)
     return list(user_permission.union(user_group))
    except Exception as e:
       raise e
def get_user_organisation_name_service(name : str) -> str :
    try :
     organisation_name = user_repo.get_user_organisation_name(name)
     return organisation_name
    except Exception as e:
       raise e
def get_user_data_service(name : str)-> dict :
  with ThreadPoolExecutor(max_workers=2) as executor:
    try :
      permission_future = executor.submit(user_update_service, name)
      organisation_future = executor.submit(get_user_organisation_name_service, name)
      return ({"permissions" : permission_future.result(),"org" : organisation_future.result()})
    except Exception as e:
       raise e
def get_all_users_service() -> list :
    try :
      users = user_repo.get_all_users()
      return users
    except Exception as e:
       raise e

