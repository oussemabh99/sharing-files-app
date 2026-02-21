def get_path_service(org:str) -> dict:
    data = {
     f"/tenant/api/v1/{org}/users":{"GET":"get_users","POST":"edit_users","PUT":"edit_users","DELETE":"edit_users"},
     f"/tenant/api/v1/{org}/roles":{},
     f"/tenant/api/v1/{org}/permissions":{},
     f"/tenant/api/v1/{org}/roles/assign":{},
     f"/tenant/api/v1/{org}/groups":{"GET":"get_groups","POST":"edit_groups"},
     f"/tenant/api/v1/{org}/groups/assign":{},
     f"/tenant/api/v1/{org}/groupuser":{}
     } 
    return data

def compare_permission_service(path : str, request : str , permissions : list[str], org : str) -> bool:
    d = get_path_service(org)
    if d[path] =={} :
       return False 
    try :
            authorization=d[path][request]
            if authorization in permissions :
              return True
    except :
           return False
    return False