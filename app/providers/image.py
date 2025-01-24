"""Image provider module.

This module provides a factory class for creating instances of image services.
It abstracts the creation of specific image service implementations, such as HTTPXService.
"""

from app.integration.httpx import HTTPXService
from app.interfaces.image import ImageService


class ImageProvider:
    """Factory class for providing image service instances.

    This class is responsible for creating and returning instances of image services,
    such as HTTPXService, which implement the `ImageService` interface.
    """

    def img(self) -> ImageService:
        """Create and return an instance of an image service.

        Returns
        -------
        ImageService
            An instance of an image service, specifically HTTPXService.

        """
        return HTTPXService()
