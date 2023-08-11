from django.shortcuts import render
from .models import Data

# Create your views here.
def game(request):
    data= Data.objects.order_by("-created_at").filter()
    questions = []
    answer = []
    hints = []
    commentary = []
    for i in range(5):
        questions.append(data[i]["question"])
        answer.append(data[i]["answer"])
        hints.append(data[i]["hints"])
        commentary.append(data[i]["commentary"])
    return render(request, "base.html")