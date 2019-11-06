from django.shortcuts import render

from pictures.models import Picture


# Create your views here.
def index(request):
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

    context = {
        'pictures': updated_pictures,
        'grid_placeholders': [1, 2]
    }
    return render(request, 'pages/index.html.j2', context)
