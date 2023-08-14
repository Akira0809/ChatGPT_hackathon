from django.shortcuts import render

def result(request):
    point = request.GET.get("point", "")
    if point == "0":
        image_url = "img/stamp_english5.png"
    elif point == "10":
        image_url = "img/stamp_english5.png"
    elif point == "20":
        image_url = "img/stamp_english4.png"
    elif point == "30":
        image_url = "img/stamp_english3.png"
    elif point == "40":
        image_url = "img/stamp_english2.png"
    elif point == "50":
        image_url = "img/stamp_english1.png"
    else:
        image_url = "img/stamp_english1.png"

    return render(request, "result.html", context={"point": point, "image_url": image_url})
