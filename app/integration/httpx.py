"""HTTPX-based image fetching and decoding service.

This module provides an implementation of the `ImageService` interface using the `httpx` library
to fetch image content from URLs and decode it into base64-encoded strings.
"""

import base64
from typing import override

import httpx

from app.interfaces.image import ImageService


class HTTPXService(ImageService):
    """Service for fetching and decoding images using HTTPX.

    Attributes
    ----------
    method : str
        The encoding method used for decoding image bytes into strings. Defaults to "utf-8".

    """

    def __init__(self) -> None:
        """Initialize the HTTPXService with default encoding method."""
        self.method: str = "utf-8"

    @override
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
        return httpx.get(url).content

    @override
    def decode_img_bytes(self, content: bytes) -> str:
        """Decode raw image bytes into a base64-encoded string.

        Parameters
        ----------
        content : bytes
            The raw image content as bytes.

        Returns
        -------
        str
            The base64-encoded string representation of the image.

        """
        return base64.standard_b64encode(content).decode(self.method)
