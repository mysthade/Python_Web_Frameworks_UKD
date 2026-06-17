from models.bot_feature import BotFeature
from schemas.bot_feature import BotFeatureCreate, BotFeatureUpdate
from services.base import BaseCRUDService, service_dependency


class BotFeatureService(
    BaseCRUDService[BotFeature, BotFeatureCreate, BotFeatureUpdate]
):
    model = BotFeature


get_bot_feature_service = service_dependency(BotFeatureService)
