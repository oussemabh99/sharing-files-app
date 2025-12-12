from app.models.models import Group
from app.repository.group_repo import create_group, get_group_all
def create_group_service(**kwargs) -> str:
    name = kwargs.get("name")
    display_name = kwargs.get("display_name", "")
    organisation_uuid = kwargs.get("organisation_uuid")
    if not name or not organisation_uuid:
        raise ValueError("Group name and organisation_uuid are required.")
    try :
     new_group = create_group(
        name=name,
        display_name=display_name,
        organisation_uuid=organisation_uuid
     )
    except Exception as e :
        raise ValueError(f"Error creating group: {e}")
    return new_group.uuid
def get_group_all_service() -> list[Group]:
    groups = get_group_all()
    groups_data = {"groups":[
        {
            "uuid": group.uuid,
            "name": group.name,
            "display_name": group.display_name,
            "organisation_uuid": group.organisation_uuid,
            "date_created": group.date_created.isoformat(),
            "date_modified": group.date_modified.isoformat()
        }
        for group in groups
    ]}
    return groups_data