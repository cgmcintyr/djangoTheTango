from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render

from rango.forms import CategoryForm, PageForm
from rango.models import Category, Page, User, UserProfile
import rango.bing_search as bing_search
 
from registration import signals
from registration.users import UserModel 
from registration.backends.simple.views import RegistrationView


def index(request):
    # Add list of top 5 categorys and top 5 pages to context dictionary.
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'top_pages': page_list}

    context_dict = {'categories': category_list, 'top_pages': page_list}
    visits = request.session.get('visits')

    if not visits:
        visits = 1
    reset_last_visit_time = False


    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        
        # If it has been more than a day since user last visited the site.
        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it as current date/time. 
        reset_last_visit_time = True


    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] =  visits
    context_dict['visits'] = visits

    response = render(request, 'rango/index.html', context_dict)

    return response    

def about(request):
    if request.session.get('visits'):
        visits = request.session.get('visits')
    else:
        visits = 0

    return render(request, 'rango/about.html', {'visits': visits})


# --- Category/Page Views --- #
@login_required
def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        # Have we provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - print them to terminal
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any)
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None   

    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                
                return HttpResponseRedirect(reverse('rango:category', args=(category_name_slug,)))

        else:
            print form.errors
    else:
        form = PageForm()
    
    context_dict = {'form':form, 'category': cat,  'category_name_slug': category_name_slug}

    return render(request, 'rango/add_page.html', context_dict)           

def category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}
    
    try:
        # Can we find a category slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception
        # So the .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        # Retrieve all of the associated pages.
        # Note that filter returns >= 1 model instance.
        pages = Page.objects.filter(category=category)
        
        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify the category exists.
        context_dict['category'] = category

        context_dict['category_name_slug'] = category_name_slug

    except Category.DoesNotExist:
        # We get here if we didn't find the specified category
        # Don't do anything - the template displays the "no category" message for us
        pass
    
    # Go render the response and return it to the client
    return render(request, 'rango/category.html', context_dict)
    
def track_url(request):
    """
    View used to increment Page.views when user visits a page through a rango category page.
    """
    if request.method == 'GET':
        page_id = request.GET.get('page_id')

        if (page_id == None):
            return HttpResponseBadRequest('<h1>Bad Request (400)</h1>', content_type='text/html')

        try:
            page = Page.objects.get(id=page_id)
            print("Page = {0}".format(page))
            page.views += 1
            page.save()
            return HttpResponseRedirect(page.url)
        except Page.DoesNotExist:
            return HttpResponseNotFound('<h1>Page not found (404)</h1>', content_type='text/html')

    return HttpResponseRedirect('/rango/')

# --- USER RELATED VIEWS --- #
class MyRegistrationView(RegistrationView):
    """ 
    Custom registration-redux class  which creates a UserProfile object when a User is registered.
    """

    def register(self, request, **cleaned_data):
        # Create a new User 
        username, email, password = cleaned_data['username'], cleaned_data['email'], cleaned_data['password1']
        new_user_object = UserModel().objects.create_user(username, email, password)

        # And links that user to a new (empty) UserProfile
        profile = UserProfile(user=new_user_object)
        profile.save()
        
        new_user = authenticate(username=username, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
        
    def get_success_url(self, request, user):
        return('/rango/', (), {})

# --- BING --- # 
def search(request):
    
    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        print "--- BING QUERY ---"
        print query
        print "--- Stripped ---"
        print query.strip()
        print "--- Running query... ---"
        
        if query:
            result_list = bing_search.run_query(query)

    return(render(request, 'rango/search.html', {'result_list': result_list}))

# --- Other --- #
@login_required    
def restricted(request):
    return render(request, 'rango/restricted.html', {})    


