"""API endpoints related to diet and nutrition processing.

This module provides endpoints for processing diet-related data, such as analyzing
images of food and generating nutritional feedback using AI models.
"""

from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.providers.image import ImageProvider
from app.providers.llm import LLMProvider

if TYPE_CHECKING:
    from app.interfaces.image import ImageService
    from app.interfaces.llm import LLMService

diet_router = APIRouter(prefix="/diet")


class ImageRequest(BaseModel):
    """Represents an image request with a URL.

    Attributes
    ----------
    url : str
        The URL of the image to be processed. Must be a publicly accessible URL pointing to
        an image file in JPEG or PNG format. The image should be clear and focused on the food item.

    Examples
    --------
        - "https://example.com/path/to/image.jpg"
        - "https://storage.googleapis.com/bucket/image.png"

    """

    url: str = Body(
        example="https://example.com/path/to/image.jpg",
        description=(
            "Public URL of the food image to analyze. Supported formats: JPEG, PNG. "
            "Image should be clear and focused on the food item."
        ),
    )


@diet_router.post("/process")
async def process(body: Annotated[ImageRequest, Body(...)]) -> StreamingResponse:
    """Process an image of food and generate nutritional feedback.

    This endpoint fetches an image from a URL, processes it to generate a description,
    and then streams nutritional feedback based on the description.

    Important:
    ---------
        This endpoint cannot be tested using Swagger UI as it does not support streaming responses.
        To test this functionality, please visit http://localhost:8000/static/index.html
        and use the web interface provided there.

    """
    llm: LLMService = LLMProvider().llm()
    img: ImageService = ImageProvider().img()

    url = body.url
    bt = img.fetch_img_content(url)
    content = img.decode_img_bytes(bt)
    desc = await llm.get_image_description(content)

    return await llm.stream_nutritional_feedback(desc)
