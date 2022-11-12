from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from users.models import OwnedBlog, Blog, LikeBlog, AccountUser
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse  # login
from django.http import HttpResponseRedirect 
from .forms import RegisterForm
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return loginPage(request)
    return render(request, 'users/homepage.html')

def aboutUs(request):
    return render(request, 'users/aboutUs.html')
#----------------------------------------------------------------------#

def logoutFunc(request):
    logout(request)
    return render(request, 'users/loginUser.html', {
        'message': 'You are logged out.'
    })

def profile(request):
    if not request.user.is_authenticated:
        return loginPage(request)
    userId=1
    user = AccountUser.objects.filter(user_id=request.user.id).first()
    blogs = Blog.objects.filter(user_id=request.user.id).all()
    blog1 = [1,2,3]
    print(blogs)
    return render(request, 'users/myProfile.html',{
        'blogs': blogs,
        'user': user
    })

def viewProfile(request):
    userId=1
    print(request.user.id)
    
    blogs = Blog.objects.filter(user_id=request.user.id).values_list('pk', flat=True)
    blog1 = [1,2,3]
    
 
    return render(request, 'users/userProfile.html',{
        'blogs': blog1,
        
    })

def createBlogPage(request):
    return render(request, 'users/createBlogPage.html',{
        
    })


def createBlog(request):
    return homepage(request)

def likeBlog(request):
    id = request.POST['id']
    
    blog = Blog.objects.filter(pk=id).first()
    like = True
    if like:
        blog.like += 1
        blog.save()
        likeBlog = LikeBlog(user=request.user, blog=blog)
    return

#Cookie coin - faii

all_cookie = [
    {'id': 1, 'cookies': 20 , 'price' : '2$'},
    {'id': 2, 'cookies': 50 , 'price' : '5$'},
    {'id': 3, 'cookies': 100, 'price' : '10$'},
    {'id': 4, 'cookies': 500, 'price' : '50$'},
    {'id': 5, 'cookies': 1000, 'price' : '100$'},
    {'id': 6, 'cookies': 5000, 'price' : '500$'},
]

def cookieCoin(request):
    context={'cookies': all_cookie}
    return render(request, 'users/cookieCoin.html', context)

def confirmCookie(request, cookie_id):
    oneCookie = [c for c in all_cookie if c['id'] == cookie_id][0]
    context = {'cookies': oneCookie}
    return render(request, 'users/confirmCookie.html', context)

#------------------------------------------------------------
#----------------------chom---------------------------------

def homepage(request):
    blog1 = [1,2,3,4]
    maxlen = len(blog1)
    return render(request, 'users/homepage.html',{
        'blogs': blog1,
        'maxlen':maxlen
    })

def members(request):
    return render(request,'users/members.html' )
#---------------------------------------------------------------
#-------------------------safe---------------------------------
def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'users/loginUser.html', {
                'message': 'Invalid credentials.'
            })

    return render(request, 'users/loginUser.html')

# Create your views here.


def register(response):  # register
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect(reverse("login"))
    else:
        form = RegisterForm()

    return render(response, "users/registerUserPpl.html", {"form": form})

#---------------------------fe-------------------------------
def detail(request):
    return render(request, 'users/detail.html')

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # title_tag = Blog.objects.filter(title_tag_icontains = searched)
        return render(request, 'users/blogpageUser.html', {'searched':searched})
    else:
        return render(request, 'users/blogpageUser.html')