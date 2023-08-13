from django.shortcuts import render

def result(request):
    point = 1
    return render(request, "result.html", context={"point": point})