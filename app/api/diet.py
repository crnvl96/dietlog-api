import base64
from collections.abc import AsyncGenerator

import httpx
from anthropic import AsyncAnthropic
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

diet_router = APIRouter(prefix="/diet")
client = AsyncAnthropic()


def get_image() -> str:
    image1_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/NCI_Visuals_Food_Hamburger.jpg/230px-NCI_Visuals_Food_Hamburger.jpg"
    return base64.standard_b64encode(httpx.get(image1_url).content).decode("utf-8")


async def get_image_description(image_data: str) -> str:
    response = await client.messages.create(
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
                    {
                        "type": "text",
                        "text": "Describe the food in this image in detail, including all visible components and preparation methods.",
                    },
                ],
            }
        ],
    )
    return response.content[0].text


@diet_router.post("/process")
async def process() -> StreamingResponse:
    async def generate() -> AsyncGenerator[str, None]:
        image_data = get_image()
        image_description = await get_image_description(image_data)

        prompt_template = """
        You are an AI nutritionist with extensive knowledge of food, nutrition, and health.
        Your task is to analyze food descriptions and provide comprehensive, health-focused feedback.

        Here's the description of the food you need to analyze:

        <image_description>
        {{IMAGE_DESCRIPTION}}
        </image_description>

        Your analysis should follow these steps:

        1. Carefully read and understand the food description.
        2. Identify all food components and their preparation methods.
        3. Analyze the nutritional value of the meal, considering:
           a. Nutritional balance (proteins, carbohydrates, fats, vitamins, and minerals)
           b. Portion sizes
           c. Cooking methods (e.g., fried, baked, grilled, raw)
           d. Presence of processed vs. whole foods
           e. Estimated calorie density
           f. Fiber content
           g. Presence of added sugars or unhealthy fats
        4. Assess the overall healthiness of the meal.
        5. Determine a health score on a scale of 1 to 10 (1 being extremely unhealthy, 10 being very healthy).
        6. Provide reasoning for your score.
        7. Offer constructive feedback and suggestions for improvement.

        Before providing your final assessment, break down your thought process inside <nutritional_breakdown> tags.
        This will ensure a thorough interpretation of the food description. Include the following steps:

        1. List all food components and preparation methods
        2. Evaluate each component's nutritional value
        3. Assess cooking methods and their health implications
        4. Estimate overall nutritional balance and calorie density
        5. Consider portion sizes
        6. Identify any concerning ingredients (e.g., added sugars, unhealthy fats)

        It's OK for this section to be quite long.

        Your final output should be structured as follows:

        <nutritional_breakdown>
        [Detailed breakdown of the meal components and their health implications, following the steps above]
        </nutritional_breakdown>

        <reasoning>
        [Explanation of how you arrived at the health score]
        </reasoning>

        <score>
        [Health score between 1 and 10]
        </score>

        <feedback>
        [Constructive feedback about the meal's healthiness and specific suggestions for improvement]
        </feedback>

        Remember to:
        - Be objective and base your assessment solely on the information provided in the image description.
        - Consider both positive and negative health aspects of each food item and preparation method.
        - Provide specific, actionable suggestions for improving the nutritional value of the meal.
        - Explain your reasoning clearly, using your expertise as a nutritionist.

        Now, please proceed with your analysis of the described food.
        """

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
