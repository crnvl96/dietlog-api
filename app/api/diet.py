import asyncio
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from app.config.settings import Settings, load_env

diet_router = APIRouter(prefix="/diet")


def process_image(_: UploadFile):
    return """The image shows a traditional Brazilian breakfast setup.
        A cup of strong black coffee or café com leite (coffee with milk) is prominently placed.
        A basket contains freshly baked pão francês (crusty French-style rolls) and a few pieces of pão de queijo (cheese bread).
        A plate holds slices of fresh fruit, such as papaya, mango, or banana.
        A small dish includes butter and slices of queijo minas (soft cheese) or ham.
        A glass of orange juice or another fruit juice is visible. Optionally, a slice of bolo (cake), such as corn or coconut cake, or a yogurt bowl may be present.
        The arrangement is simple, fresh, and balanced, reflecting typical Brazilian breakfast elements."""


@diet_router.post("/process")
async def process(
    text: Annotated[str, Form()],
    image: UploadFile,
    settings: Annotated[Settings, Depends(load_env)],
):
    image_description = process_image(image)

    llm = ChatAnthropic(
        api_key=settings.ANTHROPIC_API_KEY,
        model="claude-3-opus-20240229",  # pyright: ignore[reportCallIssue]
        streaming=True,
    )

    prompt = PromptTemplate(
        input_variables=["text", "image_description"],
        template="You are a helpful AI. The user said: {text}. The image contains: {image_description}. Respond accordingly.",
    )

    chain = prompt | llm | StrOutputParser()  # pyright: ignore[reportUnknownVariableType]

    try:

        async def generate():
            async for chunk in chain.astream(  # pyright: ignore[reportUnknownMemberType]
                {"text": text, "image_description": image_description}
            ):
                yield chunk
                await asyncio.sleep(0.1)  # Simulate a slight delay for realism

        return StreamingResponse(generate(), media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# from transformers import BlipProcessor, BlipForConditionalGeneration
#
# # Load BLIP model and processor
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
#
# def process_image(image: UploadFile):
#     # Open the image
#     img = Image.open(io.BytesIO(image.file.read())).convert("RGB")
#
#     # Generate a description using BLIP
#     inputs = processor(img, return_tensors="pt")
#     out = model.generate(**inputs)
#     description = processor.decode(out[0], skip_special_tokens=True)
#
#     return description
