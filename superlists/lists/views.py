from lists import models
from django.shortcuts import render, redirect

from . import forms


def home_page(request):
    context = {
        'form': forms.ItemForm()
    }
    return render(request, 'home.html', context)


def view_list(request, id):
    list_ = models.List.objects.get(pk=id)
    form = forms.ItemForm()

    if request.method == 'POST':
        form = forms.ItemForm(request.POST)
        if form.is_valid():
            form.save(for_list=list_)
            return redirect(list_)

    context = {
        'list': list_,
        'form': form
    }
    return render(request, 'list.html', context)


def new_list(request):
    form = forms.ItemForm(request.POST)
    if form.is_valid():
        list_ = models.List.objects.create()
        form.save(for_list=list_)
        return redirect(list_)
    else:
        context = {
            'form': form
        }
        return render(request, 'home.html', context)
