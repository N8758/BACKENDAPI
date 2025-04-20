from openai import OpenAI, APIError
from .config import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

def rewrite_text(text: str, tone: str) -> str:
    try:
        prompt = f"Rewrite the following text in a {tone} tone:\n\n{text}"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        return response.choices[0].message.content.strip()

    except APIError as e:
        return f"[OpenAI API Error] {str(e)}"
    except Exception as e:
        return f"[Error] {str(e)}"
