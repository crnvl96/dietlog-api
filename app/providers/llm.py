"""LLM (Large Language Model) provider module.

This module provides a factory class for creating instances of LLM services.
It abstracts the creation of specific LLM service implementations, such as AnthropicService.
"""

from app.integration.anthropic import AnthropicService
from app.interfaces.llm import LLMService


class LLMProvider:
    """Factory class for providing LLM service instances.

    This class is responsible for creating and returning instances of LLM services,
    such as AnthropicService, which implement the `LLMService` interface.
    """

    def llm(self) -> LLMService:
        """Create and return an instance of an LLM service.

        Returns
        -------
        LLMService
            An instance of an LLM service, specifically AnthropicService.

        """
        return AnthropicService()
