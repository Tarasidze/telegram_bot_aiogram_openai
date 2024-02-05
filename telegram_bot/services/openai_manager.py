import os
from dotenv import load_dotenv
from openai import AsyncOpenAI


load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPEN_AI_KEY"))


async def send_request_to_ai(location: str, message: str) -> str:

    prompt = (
        f"Request may be in english or ukrainian language. "        
        f"Imagine that you are the administrator of certain locations, "
        f"and the user left you feedback. "
        f"Analyze the feedback and send an answer, "
        f"the answer should be strict, but not too official."
        f"Location: {location}."
        f"Feedback: {message}"
        f"Answer in the language in which they were asked"
    )

    response = await client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.9,
    )

    return response.choices[0].text
