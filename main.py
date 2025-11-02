
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

BANNED_WORDS = ["kill", "hack", "bomb"]

def check_moderation(text):
    """
    Checks if the given text contains banned words.
    Returns True if it violates the moderation policy.
    """
    for word in BANNED_WORDS:
        if word.lower() in text.lower():
            return True
    return False

user_prompt = input("Enter your prompt: ")

if check_moderation(user_prompt):
    print("Your input violated the moderation policy. Please try again with safe content.")
    exit()

system_prompt = (
    "You are a friendly and helpful AI assistant. "
    "Always reply in a positive, clear, and concise way."
)

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    ai_reply = response.choices[0].message.content

    if check_moderation(ai_reply):
        for word in BANNED_WORDS:
            ai_reply = ai_reply.replace(word, "[REDACTED]")
            ai_reply = ai_reply.replace(word.capitalize(), "[REDACTED]")
    print("\n Response:\n")
    print(ai_reply)

except Exception as e:
    print("Something went wrong.")
    print("Error details:", e)
