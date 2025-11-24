from openai import OpenAI, NotGiven, Timeout
from config.base import settings

def ask_llm(system_prompt: str, user_prompt: str, model: str, temperature: float = 0, api_key: str = settings.LLM_API_KEY, timeout: float = NotGiven()):

    client = OpenAI(api_key=api_key, base_url=settings.LLM_BASE_URL, timeout=timeout)

    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = client.chat.completions.create(messages=messages, model=model, temperature=temperature, stream=False)

    return response.choices[0].message.content