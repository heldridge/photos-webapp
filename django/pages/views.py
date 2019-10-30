from django.shortcuts import render


# Create your views here.
def tailwind(request):
    return render(request, 'pages/index-tailwind.html.j2')

def index(request):
    return render(request, 'pages/index.html.j2')
