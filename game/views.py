from django.shortcuts import render
import openai

# Create your views here.
def game(request):
    with open("../api.text", "r") as f:
        openai.api_key = f.read().strip()

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "ChatGPTについて"},
        ]
    )
    text = response.choices[0]["message"]["content"].strip()
    return render(request, "base.html", context={"text": text})