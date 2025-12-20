d = {
     "/idm/api/v1/users":{"GET":"get_users","POST":"edit_users","PUT":"edit_users","DELETE":"edit_users"},
     "/idm/api/v1/roles":{"GET":"get_roles","POST":"edit_roles"},
     "/idm/api/v1/permissions":{},
     "/idm/api/v1/roles/assign":{},
     "/idm/api/v1/groups":{"GET":"get_groups","POST":"edit_groups"},
     "/idm/api/v1/groups/assign":{},
     "/idm/api/v1/groupuser":{}
     }
def compare_permission_service(path : str, request : str , permissions : list[str]) -> bool:
    if d[path] =={} :
       return True 
    try :
            authorization=d[path][request]
            if authorization in permissions :
              return True
    except :
           return False
    return False