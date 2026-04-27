from src.engine.services.images_service import ImagesServices
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    images_service = ImagesServices()
    sounds_service = SoundsService()
