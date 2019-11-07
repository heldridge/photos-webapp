from django.shortcuts import render

from pictures.models import Picture


def getLatestPictures():
    pictures = Picture.objects.order_by('-uploaded_at')[:16]

    max_width = 85
    expander_length = 5
    static_width_addition = 4
    updated_pictures = []
    for picture in pictures:
        data = {'original': picture, 'above_tags': [], 'below_tags': []}
        current_width = 0
        above = True
        for tag in picture.tags:
            current_width += static_width_addition + len(tag)
            if current_width + expander_length > max_width:
                above = False

            if above:
                data['above_tags'].append(tag)
            else:
                data['below_tags'].append(tag)

        updated_pictures.append(data)
    return updated_pictures


# Create your views here.
def index(request):
    context = {
        'pictures': getLatestPictures(),
        'grid_placeholders': [1, 2]
    }
    return render(request, 'pages/index.html.j2', context)


def search(request):
    context = {
        'pictures': getLatestPictures(),
        'searchedTags': [
            'forest', 'tag', 'ice-cream', 'sky', 'people', 'person'
        ]
    }
    return render(request, 'pages/search.html.j2', context)
