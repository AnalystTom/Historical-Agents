from openai import AsyncOpenAI
from backend.config import Settings

class OpenAIService:
    def __init__(self):
        settings = Settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def get_completion(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "system",
                "content": prompt
            }]
        )
        return response.choices[0].message.content