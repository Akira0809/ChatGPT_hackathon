from django.shortcuts import render
from .models import Data
import json

# Create your views here.
def game(request):
    data= Data.objects.order_by("-created_at").filter()
    data = json.loads(data)
    return render(request, "base.html", context={"data": data})
