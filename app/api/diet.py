import io
from typing import Annotated, cast

from fastapi import APIRouter, Depends, Form, HTTPException, UploadFile
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import PromptTemplate
from PIL import Image
from pydantic import BaseModel, Field
from transformers import BlipForConditionalGeneration, BlipProcessor

from app.config.settings import Settings, load_env

diet_router = APIRouter(prefix="/diet")


class DietItem(BaseModel):
    item: str = Field(description="Name of the desired item.")
    present: str = Field(
        description="Presence of the desired item in the picture sent."
    )
    score: int = Field(
        description="Representation of how close the item in the picture is from the desired item."
    )
    note: str = Field(description="Quick explanation about the item score")


class DietReport(BaseModel):
    evaluation: list[DietItem] = Field(description="Diet items to be evaluated.")
    final_score: int = Field(
        description="Overall representation about how good is the current meal based on the target diet."
    )
    general_note: str = Field(
        description="Quick explanation about the meal final_score"
    )


async def process_image(image: UploadFile) -> str:
    try:
        img = Image.open(io.BytesIO(await image.read())).convert("RGB")

        processor: BlipProcessor = cast(
            BlipProcessor,
            BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base"),
        )

        model = BlipForConditionalGeneration.from_pretrained(
            "Salesforce/blip-image-captioning-base"
        )

        inputs = processor(img, return_tensors="pt")
        out = model.generate(**inputs, interpolate_pos_encoding=False)
        description = processor.decode(out[0], skip_special_tokens=True)

        print(description)

        return description

    except Exception as e:
        raise ValueError(f"Error processing image: {e}")


@diet_router.post("/process")
async def process(
    text: Annotated[str, Form()],
    image: UploadFile,
    settings: Annotated[Settings, Depends(load_env)],
):
    try:
        image_description = await process_image(image)

        llm = ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model_name="claude-3-5-haiku-latest",
            streaming=True,
            timeout=None,
            stop=None,
        )

        structured_llm = llm.with_structured_output(DietReport)

        print(text)

        prompt = PromptTemplate(
            input_variables=["text", "image_description"],
            template="""
              You are a nutritionist, specializing in food evaluation. You are really good at analyzing food descriptions
            and understanding the nutritional values of each ingredient present. I will send you a description of a meal,
            and your task is to evaluate each ingredient and provide feedback about it.
            The feedback should focus on how close the current ingredient is to what should be in a healthy meal.
            For example:
            - If there is meat in the meal, but it is fatty, you should point that out.
            - If there is rice, it is good, but it could be substituted for integral rice.
            - If there is no salad, you should suggest adding at least a little.
            - If there is something fried, it is not good; it could be substituted with something baked.
            Summarize each feedback with a score from 1 to 100.
            After evaluating each ingredient, provide a general evaluation of the dish. This should be a quick summary of your thoughts.
            Also, provide an overall score for the entire meal.

            Below is the meal description you must evaluate:

            {image_description}
            """,
        )

        chain = prompt | structured_llm

        response = chain.invoke({"image_description": image_description})

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
