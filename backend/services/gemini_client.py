"""Google Gemini API client."""
import google.generativeai as genai
from backend.services.llm_client import LLMClient
from backend.config import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class GeminiClient(LLMClient):
    """Client for interacting with Google Gemini API."""

    def __init__(self):
        """Initialize Gemini client with API key."""
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        genai.configure(api_key=settings.google_api_key)
        # v1beta expects fully qualified model names (e.g., models/gemini-1.5-flash-latest)
        self.model = genai.GenerativeModel(settings.gemini_model)
        logger.info(f"Initialized Gemini client with model: {settings.gemini_model}")

    async def generate(self, prompt: str) -> str:
        """Generate response from Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Sending prompt to Gemini (first 200 chars): {prompt[:200]}")
            response = self.model.generate_content(prompt)
            logger.debug("Received response from Gemini")
            return response.text
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")
            raise
