"""Custom exceptions related to image processing.

This module defines exceptions that are raised when specific image-related
conditions are not met, such as exceeding the maximum allowed image size.
"""


class ImageTooLargeError(Exception):
    """Exception raised when an image exceeds the maximum allowed size.

    Attributes:
        max_size (int): The maximum allowed size for an image in bytes.
        actual_size (int): The actual size of the image in bytes.

    """

    def __init__(self, max_size: int, actual_size: int) -> None:
        """Initialize the ImageTooLargeError with size details.

        Parameters
        ----------
        max_size : int
            The maximum allowed size for an image in bytes.
        actual_size : int
            The actual size of the image in bytes.

        """
        self.max_size: int = max_size
        self.actual_size: int = actual_size
        super().__init__(f"Image size {actual_size} exceeds maximum allowed size of {max_size} bytes")
