import json

from dotenv import load_dotenv
from openai import OpenAI
from tools import TOOLS
from functions import FUNCTIONS

SYSTEM_PROMPT = """
You are an email triage assistant. Your goal is to process this email inbox to zero.

Work through the inbox one email at a time. 

When every email is handled, stop calling tools and summarize what you did.
"""

load_dotenv()
client = OpenAI()

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Please triage my inbox"}
]

while True:
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
    message = response.choices[0].message
    
    messages.append(message)
    
    if not message.tool_calls:
        print(message.content)
        break

    for tool_call in message.tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        print(name, args)

        result = FUNCTIONS[name](**args)

        print(result)

        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})

