from google import genai
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

client=genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

msg=[]

while True:
    print("Type 'Exit' To Leave Code.........\n")
    user=input('Enter Your Query :- \n' )
    if (user == 'Exit'):
        break

    msg.append({
    'role':'user',
    'content':user
        })

    res=client.models.generate_content(
        model='gemini-2.5-flash',
        contents=list(map(lambda mess:mess['role'] + ':' + mess['content'],msg))
        )

    msg.append({
        'role':'AI',
        'content':res.text
    })

    print(res.text)
