from django.shortcuts import render

def index(request):
	return HttpResponse("<h1>Rango says hey there, world!</h1><a href='/rango/about/>About</a>")

def about(request):
	return HttpResponse("This is the about page.<a href='/rango'>Home</a>")


