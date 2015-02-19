from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category

def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}
    #Return a rendered response to send to the client.
    return render(request, 'rango/index.html', context_dict)

def about(request):
    context_dict = {}
    return render(request, 'rango/about.html', context_dict)

