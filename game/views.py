from django.shortcuts import render
from .models import Data
import openai

# Create your views here.
def game(request):
    
    return render(request, "base.html", context={"text": text})

def difficulty(request):
    with open("../api.text", "r") as f:
        openai.api_key = f.read().strip()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "ChatGPTについて"},
        ]
    )
    text = response.choices[0]["message"]["content"].strip()
    Data.objects.create(text)