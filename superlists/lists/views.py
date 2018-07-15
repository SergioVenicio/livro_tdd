from lists import models
from django.shortcuts import render, redirect


def home_page(request):
    return render(request, 'home.html')


def view_list(request, id):
    list_ = models.List.objects.get(pk=id)
    context = {
        'list': list_
    }
    return render(request, 'list.html', context)


def new_list(request):
    list_ = models.List.objects.create()
    models.Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/lists/{list_.id}/')


def add_item(request, id):
    list_ = models.List.objects.get(pk=id)
    models.Item.objects.create(text=request.POST.get('item_text'), list=list_)
    return redirect(f'/lists/{list_.id}/')
