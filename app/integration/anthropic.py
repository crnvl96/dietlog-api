"""Integration module for Anthropic's LLM service.

This module provides an implementation of the `LLMService` interface using Anthropic's API.
It includes functionality for generating image descriptions and streaming nutritional feedback
based on structured prompts. The prompts are designed to guide the AI in analyzing food images
and providing detailed, health-focused feedback.
"""

from collections.abc import AsyncGenerator
from typing import override

from anthropic import AsyncAnthropic
from anthropic.types.text_block import TextBlock
from fastapi.responses import StreamingResponse

from app.interfaces.llm import LLMService


class AnthropicService(LLMService):
    """Service for interacting with Anthropic's LLM API.

    This class implements the `LLMService` interface, providing methods for generating
    image descriptions and streaming nutritional feedback. It includes structured prompts
    to guide the AI in analyzing food images and providing health-focused feedback.

    Attributes
    ----------
    client : AsyncAnthropic
        The Anthropic API client used for making requests.
    food_image_description_prompt : str
        A prompt template for generating detailed descriptions of food images.
    food_nutritional_feedback_prompt : str
        A prompt template for generating nutritional feedback based on food descriptions.

    """

    def __init__(self) -> None:
        """Initialize the AnthropicService with the API client and prompts."""
        self.client: AsyncAnthropic = AsyncAnthropic()
        self.food_image_description_prompt: str = """
            You are an AI assistant tasked with analyzing a food image and providing a detailed description of
            the meal and its ingredients. Your goal is to accurately describe what you can see in the image
            without making assumptions about ingredients or dishes that are not clearly visible or identifiable.

            Carefully examine the image and focus on the following aspects:

            1. Overall appearance of the dish
            2. Identifiable ingredients
            3. Cooking methods (if apparent)
            4. Presentation and plating
            5. Portion size
            6. Any notable textures or colors

            When describing the meal and ingredients:
            - Be as specific as possible about what you can clearly see
            - Use descriptive language to convey the appearance, texture, and perceived freshness of ingredients
            - Comment on the cooking methods or preparation techniques if they are evident
            - Describe the presentation and plating style

            It is crucial that you do not make assumptions about ingredients or dishes that you cannot clearly
            identify. If you are unsure about any element in the image:
            - State that you are uncertain or unable to identify it
            - Describe its appearance, color, or texture without specifying what it might be
            - Use phrases like "what appears to be" or "a substance that looks like" when describing ambiguous
            elements

            If the entire dish is unfamiliar or you cannot determine what it is, focus on describing its
            components and appearance without trying to name or categorize it.

            Provide your analysis in the following format:
            <analysis>
            1. Overall dish description:
            [Describe the general appearance and composition of the dish]

            2. Identifiable ingredients:
            [List and describe the ingredients you can clearly identify]

            3. Uncertain elements:
            [Describe any components you're unsure about, focusing on their appearance without specifying what
            they might be]

            4. Cooking and preparation:
            [Describe any evident cooking methods or preparation techniques]

            5. Presentation and plating:
            [Describe how the dish is presented and plated]

            6. Additional observations:
            [Include any other relevant details about the dish's appearance, portion size, or notable features]
            </analysis>

            Remember, accuracy and honesty about what you can and cannot identify are more important than making
            guesses. If you're unsure about something, it's better to describe its appearance without naming it.
        """
        self.food_nutritional_feedback_prompt: str = """
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

    @override
    async def get_image_description(self, image_data: str) -> str:
        """Generate a description for an image using a large language model.

        Parameters
        ----------
        image_data : str
            The base64-encoded string representation of the image.

        Returns
        -------
        str
            A textual description of the image generated by the LLM.

        """
        response = await self.client.messages.create(
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
                        {"type": "text", "text": self.food_image_description_prompt},
                    ],
                }
            ],
        )

        if response and response.content and len(response.content) > 0:
            content = response.content[0]
            if isinstance(content, TextBlock):
                return content.text

        return ""

    @override
    async def stream_nutritional_feedback(self, img_description: str) -> StreamingResponse:
        """Stream nutritional feedback based on a user prompt using a large language model.

        Parameters
        ----------
        img_description : str
            The user's input prompt, typically related to nutritional information or queries.

        Returns
        -------
        StreamingResponse
            A streaming response containing the LLM-generated feedback in real-time.

        """

        async def generate() -> AsyncGenerator[str, None]:
            async with self.client.messages.stream(
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": self.food_nutritional_feedback_prompt.replace(
                                    "{{IMAGE_DESCRIPTION}}", img_description
                                ),
                            },
                        ],
                    }
                ],
                model="claude-3-5-sonnet-latest",
            ) as stream:
                async for text in stream.text_stream:
                    yield f"{text}"

        return StreamingResponse(generate(), media_type="text/event-stream")
