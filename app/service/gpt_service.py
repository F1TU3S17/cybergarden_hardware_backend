import httpx
from app.core.config import settings

class GptModel:
    def __init__(self, name, base_url, api_key, provider):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key
        self.provider = provider


class GptService:
    def __init__(self):
        self.models = [
            GptModel(
                name='mistral-small-2506',
                base_url='https://api.mistral.ai/v1/chat/completions',
                api_key=settings.AI_API_KEY,
                provider='mistral'
            ),
            GptModel(
                name='mistral-small-2501',
                base_url='https://api.mistral.ai/v1/chat/completions',
                api_key=settings.AI_API_KEY,
                provider='mistral'
            ),
            GptModel(
                name='mistral-small-2501', 
                base_url='https://api.mistral.ai/v1/chat/completions', 
                api_key=settings.AI_API_KEY,
                provider='mistral'
            ),
        ]
    async def analyze_monitoring_data(self, data):
         for model in self.models:
            async with httpx.AsyncClient() as client:

                print
                response = await client.post(
                    url=model.base_url,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {model.api_key}'
                    },
                    json={
                        "model": model.name,
                        "temperature": 1,
                        "messages": [
                            {
                                "role": "system",
                                "content": settings.system_prompt + "Уточнение: Данные пожара(F - это не форенгейты, а просто обозначение Fire, данные аналоговые просто)"
                            },
                            {
                                "role": "user",
                                "content": "Info from sensors: " + str(data)
                            }
                        ]
                    }
                )
                if response.status_code != 200:
                    continue
                data = response.json()
                print("Response from GPT model:", data)
                return data['choices'][0]['message']['content']
        

    