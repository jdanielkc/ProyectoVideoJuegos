from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImagesServices
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    fonts_service = FontsService()
    images_service = ImagesServices()
    sounds_service = SoundsService()
