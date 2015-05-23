from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# Create your views here.
from django.http import HttpResponse

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)

    # Construcnt a dictoinary to pass to pass to template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    # context_dict = {'boldmessage': "I am bold font from the context"}

    # return a rendered response to send to the client.
    # We make use of ht eshortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    # return render(request, 'rango/index.html', context_dict)
    #return HttpResponse("Welcome to Smartfitness! <br/> <a href = '/rango/about'>About</a>")

def about(request):
    context_dict = {'boldmessage': "I am bold font from the context"}
    return render(request, 'rango/about.html', context_dict)
    # return HttpResponse("This is the about Page. <br/> <a href = '/rango/'>Index</a>")


def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug = category_name_slug)
        context_dict['category_name'] = category.name

        pages = Page.objects.filter(category = category)

        context_dict['pages'] = pages

        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    return render(request, 'rango/category.html', context_dict)

def add_category(request):
    if(request.method == 'POST'):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            return index(request)
        else:
            print form.errors

    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form':form})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid()and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form':profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/rango/')



