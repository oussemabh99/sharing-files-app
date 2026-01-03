import app.repository.group_repo as group_repo
import app.repository.user_repo as user_repo
import app.repository.userGroup_repo as user_group_repo
from app.models.models import UserGroup
def add_user_to_group_service(**kwargs) -> str:
    try:
        user_name = kwargs.get("user_name")
        group_name = kwargs.get("group_name")
    except KeyError as e:
        raise ValueError(f"Missing required parameter: {e}")
    group_uuid = group_repo.get_group_by_name(group_name)
    user_uuid = user_repo.get_user_by_username(user_name)
    if not user_uuid or not group_uuid:
        raise ValueError("Both user_uuid and group_uuid are required.")
    if user_group_repo.verify_group_role_exists(user_uuid, group_uuid)==True:
        raise ValueError("User is already in the group.")
    try:
        new_group_user = user_group_repo.create_user_group(
            user_uuid=user_uuid,
            group_uuid=group_uuid
        )
    except Exception as e:
        raise ValueError("Error adding user to group: " + str(e))
    return new_group_user.uuid
def get_users_in_group_service(**kwargs) -> list:
    try:
        group_name = kwargs.get("group_name")
    except KeyError as e:
        raise ValueError(f"Missing required parameter: {e}")
    group_uuid = group_repo.get_group_by_name(group_name)
    if not group_uuid:
        raise ValueError("group_uuid is required.")
    group_users = user_group_repo.get_user_group_from_group(group_uuid)
    group_users_data = {"group_users":[
        {
            "user_uuid": group_user.user_uuid,
            "group_uuid": group_user.group_uuid,
            "date_created": group_user.date_created.isoformat()
        }
        for group_user in group_users
    ]}
    return group_users_data
def get_all_users_in_groups_service() -> list:
    group_users = user_group_repo.get_group_role_all()
    group_users_data = {"group_users":[
        {
            "user_uuid": group_user.user_uuid,
            "group_uuid": group_user.group_uuid,
            "date_created": group_user.date_created.isoformat()
        }
        for group_user in group_users
    ]}
    return group_users_data
def delete_user_from_group_service(**kwargs) -> None:
    try:
        user_name = kwargs.get("user_name")
        group_name = kwargs.get("group_name")
    except KeyError as e:
        raise ValueError(f"Missing required parameter: {e}")
    group_uuid = group_repo.get_group_by_name(group_name)
    user_uuid = user_repo.get_user_by_username(user_name)
    if not user_uuid or not group_uuid:
        raise ValueError("Both user_uuid and group_uuid are required.")
    if user_group_repo.verify_group_role_exists(user_uuid, group_uuid)==True:
        raise ValueError("User is not in the group.")
    try:
        user_group_repo.delete_user_from_group(
            user_uuid=user_uuid,
            group_uuid=group_uuid
        )
    except Exception as e:
        raise ValueError("Error deleting user from group: " + str(e))