from lists import models
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect


def home_page(request):
    return render(request, 'home.html')


def view_list(request, id):
    list_ = models.List.objects.get(pk=id)
    error = None

    if request.method == 'POST':
        item = models.Item(text=request.POST['item_text'], list=list_)
        try:
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    context = {
        'list': list_,
        'error': error
    }
    return render(request, 'list.html', context)


def new_list(request):
    list_ = models.List.objects.create()
    item = models.Item(text=request.POST.get('item_text'), list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can&#39;t have an empty list item"
        context = {
            'error': error
        }
        return render(request, 'home.html', context)

    return redirect(list_)
