from app.models.models import Organisation
import app.repository.org_repo as org
def get_organisation_service() -> Organisation:
    try:
     organisations = org.get_organisation_all()         
     organisations_data = [
                {
                    "uuid": organisation.uuid,
                    "name": organisation.name,
                }
                for organisation in organisations
            ]
    except Exception :
        raise ValueError("Error fetching organisations")
    return {"organisations": organisations_data}
def create_organisation_service(**kwargs) -> str:
    name = kwargs.get("name")
    if not name:
        raise ValueError("Organisation name is required.")
    if (org.get_organisation_uuid_by_name(name)!=None):
        raise ValueError(f"Organisation '{name}' already exists.")
    try :
     new_organisation = org.create_organisation(
        name=name
     )
    except Exception :
        raise ValueError("Error creating organisation")
    return new_organisation.name