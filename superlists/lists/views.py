from superlists import settings
from django.shortcuts import render


def home_page(request):
    if request.method == 'POST':
        settings.TODO_LIST.append(request.POST.get('item_text', ''))

    context = {
        'new_item_text': settings.TODO_LIST
    }
    return render(request, 'home.html', context)
