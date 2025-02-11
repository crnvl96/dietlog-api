"""Image service interface module.

This module defines the abstract base class `ImageService`, which provides the interface
for fetching and decoding image content. Implementations of this class are responsible
for handling specific logic for retrieving and processing images.
"""

from abc import ABC, abstractmethod


class ImageService(ABC):
    """Abstract base class for image services.

    This class defines the interface for fetching image content from a URL and decoding
    raw image bytes into a usable format, such as a base64-encoded string.
    """

    @abstractmethod
    def fetch_img_content(self, url: str) -> bytes:
        """Fetch raw image content from a given URL.

        Parameters
        ----------
        url : str
            The URL of the image to fetch.

        Returns
        -------
        bytes
            The raw image content as bytes.

        """

    @abstractmethod
    def decode_img_bytes(self, content: bytes) -> str:
        """Decode raw image bytes into a usable format.

        Parameters
        ----------
        content : bytes
            The raw image content as bytes.

        Returns
        -------
        str
            The decoded image content, typically as a base64-encoded string.

        """
