from django.shortcuts import render

def result(request):
    point = request.GET.get("point", "")
    return render(request, "result.html", context={"point": point})