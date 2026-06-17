from models.profile import Profile
from schemas.profile import ProfileCreate, ProfileUpdate
from services.base import BaseCRUDService, service_dependency


class ProfileService(BaseCRUDService[Profile, ProfileCreate, ProfileUpdate]):
    model = Profile


get_profile_service = service_dependency(ProfileService)
