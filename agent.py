import json
from pathlib import Path

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
MEMORY = Path("memory.json")

if MEMORY.exists() and MEMORY.read_text():
    processed = json.loads(MEMORY.read_text())
else:
    processed = []

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"Please triage my inbox. Skip these emails with id {', '.join(processed)}"}
]
    
print(messages)

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
        
        if name in ("move_to_folder", "flag_for_review", "draft_reply"):
            processed.append(args["email_id"])
        print(result)

        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": str(result)})
        
print(set(processed))

MEMORY.write_text(json.dumps(sorted(set(processed))))

