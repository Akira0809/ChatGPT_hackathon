from django.shortcuts import render
from .models import Data
import json

# Create your views here.
def game(request):
    data= Data.objects.get(id=19)
    data = json.loads(data)
    print(data)
    return render(request, "base.html", context={"data": data})
