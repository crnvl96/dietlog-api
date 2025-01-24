from fastapi import APIRouter

from app.schemas.diet import DietSchema

diet_router = APIRouter(prefix="/diet", tags=["diet"])


@diet_router.post(
    "",
    summary="Create an entry for diet avaliation",
    description="Processes food image and diet description",
    response_description="Feedback about diet provided information",
    responses={
        200: {
            "description": "Successful Response",
            "content": {
                "application/json": {
                    "example": {
                        "message": "Nice! You're eating 100g de frango, 200g de arroz, 100g de feijão"
                    }
                }
            },
        },
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "type": "value_error",
                                "loc": ["body", "food_image_url"],
                                "msg": "food_image_url cannot be empty",
                                "input": "some valid input here",
                            }
                        ]
                    }
                }
            },
        },
    },
)
async def generate_diet_log(req: DietSchema):
    return {"message": f"Nice! You're eating {req.food_image_url}"}
