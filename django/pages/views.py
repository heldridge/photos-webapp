from django.shortcuts import render

from pictures.models import Picture


# Create your views here.
def tailwind(request):
    pictures = Picture.objects.order_by('uploaded_at')[:16]
    context = {
        'pictures': pictures,
        'grid_placeholders': [1, 2]
    }
    return render(request, 'pages/index-tailwind.html.j2', context)


def index(request):
    return render(request, 'pages/index.html.j2')
