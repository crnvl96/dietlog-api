from pydantic import BaseModel, Field, field_validator


class DietSchema(BaseModel):
    food_image_url: str = Field(
        examples=["data:image/jpeg;base64,some_valid_url=="],
        description="A valid URL or base64-encoded image data.",
        min_length=1,
    )

    food_description_expected: str = Field(
        examples=["100g de frango, 200g de arroz, 100g de feijão"],
        description="A description of the boof being analyzed.",
        min_length=1,
    )


@field_validator("food_image_url")
def validate_food_image_url(_, value: str):
    if not value.strip():
        raise ValueError("food_image_url cannot be empty")

    return value


@field_validator("food_description_expected")
def validate_food_description_expected(_, value: str):
    if not value.strip():
        raise ValueError("food_description_expected cannot be empty")

    return value
