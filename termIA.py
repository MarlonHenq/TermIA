#!/usr/bin/env python3

from openai import OpenAI
import sys
import webbrowser
from dotenv import load_dotenv
import os

client = OpenAI(api_key='YOUR_API_KEY') # Replace YOUR_API_KEY with your OpenAI API key

len = len(sys.argv)

if len == 1:
    print("No input parameter")
    sys.exit()

#Open chatGPT on chrome
if sys.argv[1] == "-o":
    print("Opening ChatGPT on Chrome")
    webbrowser.open('https://chat.openai.com/')
    sys.exit()

content = ""

for i in range(1, len):
    content = content + sys.argv[i] + " "

# Send request to the OpenAI API
response = client.chat.completions.create(
    model="gpt-3.5-turbo-1106", # gpt-3.5-turbo-1106
    messages=[
        {"role": "system", "content": "You are an AI that is running a CLI application on a user's terminal. Return short texts, separate the commands and add tags to make it colorful. (Dont use markdown) (Available colors tags:to NORMALTEXT=\033[92m,ALERT=\033[93m,COMMANDS=\033[94m,RESET=\033[0m) Example: \033[92m Hello, World! \033[0m"},
        {"role": "user", "content": content},
    ]
)

for choice in response.choices:
    print(choice.message.content)
    