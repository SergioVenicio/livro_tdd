from lists import models
from django.shortcuts import render, redirect


def home_page(request):
    if request.method == 'POST':
        new_item_text = request.POST.get('item_text', '')
        models.Item.objects.create(text=new_item_text)
        return redirect('/lists/the-only-list-in-the-world/')

    return render(request, 'home.html')


def view_list(request):
    context = {
        'items': models.Item.objects.all()
    }
    return render(request, 'list.html', context)
