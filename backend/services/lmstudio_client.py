"""LM Studio API client."""
import httpx
from backend.services.llm_client import LLMClient
from backend.config import settings
from backend.utils.logger import setup_logger

logger = setup_logger(__name__)


class LMStudioClient(LLMClient):
    """Client for interacting with LM Studio local API."""

    def __init__(self):
        """Initialize LM Studio client."""
        self.base_url = settings.lmstudio_base_url
        self.model = settings.lmstudio_model
        self.timeout = 300.0  # 5 minutes timeout for local models (they can be slow)
        logger.info(f"Initialized LM Studio client with model: {self.model}")
        logger.info(f"LM Studio URL: {self.base_url}")

    async def generate(self, prompt: str) -> str:
        """Generate response from LM Studio API.
        
        Args:
            prompt: The prompt to send to LM Studio
            
        Returns:
            Generated text response
        """
        try:
            logger.debug(f"Sending prompt to LM Studio (first 200 chars): {prompt[:200]}")
            
            # LM Studio provides OpenAI-compatible API
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/v1/chat/completions",
                    json={
                        "model": self.model,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        "temperature": 0.7,
                        "max_tokens": -1,  # -1 means no limit in LM Studio
                        "stream": False
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Extract the generated text from OpenAI-compatible response
                generated_text = data["choices"][0]["message"]["content"]
                
                logger.debug("Received response from LM Studio")
                return generated_text
                
        except httpx.ConnectError:
            error_msg = f"Could not connect to LM Studio at {self.base_url}. Make sure LM Studio is running."
            logger.error(error_msg)
            raise ConnectionError(error_msg)
        except httpx.TimeoutException:
            error_msg = "LM Studio request timed out. The model might be too slow or overloaded."
            logger.error(error_msg)
            raise TimeoutError(error_msg)
        except Exception as e:
            logger.error(f"Error calling LM Studio API: {str(e)}")
            raise
