from django.http import HttpResponse

def index(request):
	return HttpResponse("<html><body><h1>Rango says hey there, world!</h1><a href='/rango/about/>About</a></body></html>")

def about(request):
	return HttpResponse("<html><body><h1>This is the about page.</h1><a href='/rango/'>Home</a></body></html>")


