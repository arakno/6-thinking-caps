"""Factory for creating LLM clients."""
from backend.services.llm_client import LLMClient
from backend.services.gemini_client import GeminiClient
from backend.services.lmstudio_client import LMStudioClient
from backend.config import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


def create_llm_client() -> LLMClient:
    """Create and return the appropriate LLM client based on configuration.
    
    Returns:
        Configured LLM client instance
        
    Raises:
        ValueError: If provider is not supported or required config is missing
    """
    provider = settings.llm_provider.lower()
    
    logger.info(f"Creating LLM client for provider: {provider}")
    
    if provider == "gemini":
        if not settings.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY environment variable must be set when using Gemini provider"
            )
        return GeminiClient()
    
    elif provider == "lmstudio":
        if not settings.lmstudio_base_url:
            raise ValueError(
                "LMSTUDIO_BASE_URL environment variable must be set when using LM Studio provider"
            )
        if not settings.lmstudio_model:
            raise ValueError(
                "LMSTUDIO_MODEL environment variable must be set when using LM Studio provider"
            )
        return LMStudioClient()
    
    else:
        raise ValueError(
            f"Unsupported LLM provider: {provider}. "
            f"Supported providers are: gemini, lmstudio"
        )
