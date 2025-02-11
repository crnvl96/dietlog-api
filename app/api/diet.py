import base64
from collections.abc import AsyncGenerator
from typing import TYPE_CHECKING

import httpx
from anthropic import AsyncAnthropic
from anthropic.types.text_block import TextBlock

from app.prompts import food_image_description, food_nutritional_feedback

if TYPE_CHECKING:
    from anthropic.types.message import Message

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

diet_router = APIRouter(prefix="/diet")
client = AsyncAnthropic()


def get_image() -> str:
    image1_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/NCI_Visuals_Food_Hamburger.jpg/230px-NCI_Visuals_Food_Hamburger.jpg"
    return base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")


async def get_image_description(image_data: str) -> str:
    response: Message = await client.messages.create(
        model="claude-3-5-sonnet-latest",
        max_tokens=480,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {"type": "text", "text": food_image_description.prompt},
                ],
            }
        ],
    )

    if response and response.content and len(response.content) > 0:
        content = response.content[0]

        if isinstance(content, TextBlock):
            return content.text

        return ""

    return ""


@diet_router.post("/process")
async def process() -> StreamingResponse:
    async def generate() -> AsyncGenerator[str, None]:
        image_description = await get_image_description(get_image())
        prompt_template = food_nutritional_feedback.prompt
        prompt = prompt_template.replace("{{IMAGE_DESCRIPTION}}", image_description)

        async with client.messages.stream(
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                    ],
                }
            ],
            model="claude-3-5-sonnet-latest",
        ) as stream:
            async for text in stream.text_stream:
                yield f"{text}"

    return StreamingResponse(generate(), media_type="text/event-stream")
