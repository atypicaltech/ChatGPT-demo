import openai
import os
import sys


GPT_MODEL = "gpt-3.5-turbo"

try:
    openai.api_key = os.environ['OPENAI_API_KEY']
except KeyError:
    sys.stderr.write(""" You haven't set up your API key yet. If you don't have an API key yet, visit: https://platform.openai.com/signup 1. Make an account or sign in 2. Click "View API Keys" from the top right menu. 3. Click "Create new secret key" Then, open the Secrets Tool and add OPENAI_API_KEY as a secret. """)
    exit(1)

topic = input("What do you want to learn about?\n> ")
system_prompt = f"""
I want to do some interactive instruction.
I want you to start explaining the concept of {topic} to me at a 7th grade level.
Then stop and give me a multiple choice quiz, grade the quiz, and resume the explanation.
If I get the quiz wrong, reduce the grade level by 1 for the explanation and the language you use, making the language simpler.
If do not get any quiz questions wrong, increase the grade level by 1 and make the language more complex.
Then quiz me again and repeat the process.
Do not talk about the changing of the grade level.
Don’t give away the answer to the quiz before the user has a chance to respond.
Provide positive feedback to the user to encourage them to continue learning.
Make jokes periodically, as appropriate.
"""

all_messages = [
    {"role": "system", "content": system_prompt},
]

convo_started = False
while True:
    if convo_started:
        user_message = input("\n> ")
        all_messages.append({"role": "user", "content": user_message})

    convo_started = True
    response = openai.ChatCompletion.create(
        model=GPT_MODEL, messages=all_messages)
    gpt_response = response['choices'][0]['message']['content'].strip()
    print(f"{gpt_response}\n")

    all_messages.append({"role": "assistant", "content": gpt_response})
