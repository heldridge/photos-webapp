from django.shortcuts import render


# Create your views here.
def picture(request, picture_public_id):
    return render(request, "picture.html.j2")
