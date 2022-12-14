from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.models import OwnedBlog, Blog, LikeBlog, AccountUser, CookieCoin, History, Wallet, AccountOrganization, ReportBlog, ViewBlog
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse  # login
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseBadRequest 
from django.contrib.auth.models import User
from datetime import date as date_function
from random import randint
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import datetime
import time
import json

# Create your views here.

def index(request):
    try:
        user_id = request.user.id
        wallet = Wallet.objects.get(user_id=user_id)
    except Wallet.DoesNotExist:
        user_id = None

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return HttpResponseRedirect(reverse("homepage"))


def aboutUs(request):
    user_id = request.user.id
    wallet = Wallet.objects.get(user_id=user_id)

    return render(request, 'users/aboutUs.html', {
        'wallet' : wallet,
    })
# ----------------------------------------------------------------------#


def logoutFunc(request):
    logout(request)
    return render(request, 'users/loginUser.html', {
        'message': 'You are logged out.'
    })


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if not request.user.is_superuser:
        
        wallet = Wallet.objects.get(user_id=request.user.id)
        userId=1
        user = AccountUser.objects.filter(user_id=request.user.id).first()
        if user:
            blogs = Blog.objects.filter(user_id=request.user.id).all()
            like = LikeBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
            print(like)
            print(blogs)
            return render(request, 'users/myProfile.html',{
                'blogs': blogs,
                'user': user,
                'wallet' : wallet,
                'like': like
            })
        else:
            user = AccountOrganization.objects.filter(user_id=request.user.id).first()
            blogs = Blog.objects.filter(user_id=request.user.id).all()
            blog1 = [1,2,3]
            print(blogs)
            like = LikeBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
            return render(request, 'users/myProfile.html',{
                'blogs': blogs,
                'user': user,
                'wallet' : wallet,
                'like': like
            })
    return HttpResponseRedirect(reverse('homepageadmin'))
    

def viewProfile(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    wallet = Wallet.objects.get(user_id=request.user.id)

    userId=1
    print(request.user.id)
    
    user = AccountUser.objects.filter(user_id=id).first()
    if user:
        blogs = Blog.objects.filter(user_id=id, blogType=1).all()
        like = LikeBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
        print(like)
        print(blogs)
        return render(request, 'users/userProfile.html',{
            'blogs': blogs,
            'user': user,
            'wallet' : wallet,
            'like': like
        })
    else:
        user = AccountOrganization.objects.filter(user_id=id).first()
        blogs = Blog.objects.filter(user_id=id).all()
        blog1 = [1,2,3]
        print(blogs)
        like = LikeBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
        return render(request, 'users/userProfile.html',{
            'blogs': blogs,
            'user': user,
            'wallet' : wallet,
            'like': like
        })

def likeBlog(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            id = data.get('blogId')
            like = data.get('like')
            if like:
                blog = Blog.objects.filter(pk=id).first()
                blog.like += 1
                blog.save()
                likeBlog = LikeBlog.objects.create(user=request.user, blog=blog)
                return JsonResponse({'status': 'like'})
            else:
                blog = Blog.objects.filter(pk=id).first()
                blog.like -= 1
                blog.save()
                likeBlog = LikeBlog.objects.filter(user=request.user, blog=blog).delete()
                return JsonResponse({'status': 'unlike'})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest('Invalid request')
   
        


#Cookie coin - faiinarak
def cookieCoin(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    wallet = Wallet.objects.get(user_id=request.user.id)

    history = History.objects.filter(userID=request.user.id )
    cookieCoin = CookieCoin.objects.all()
    return render(request, 'users/cookieCoin.html',{
        'cookieCoin' : cookieCoin, 
        'wallet' : wallet,
        'history' : history, 
    })

def confirmCookie(request, cookie_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    global userID
    wallet = Wallet.objects.get(user_id=request.user.id)

    if request.method == "POST":
        userID=request.user.id
        time = request.POST['time']
        slip = request.POST["slip"]
        date = request.POST["date"]
        cookie = request.POST["cookie"]
        price = request.POST["price"]
        transactionCode = randint(1, 100000)

        account = History.objects.create(
            time=time, historyType=True, slip=slip, date=date, userID=userID, cookie=cookie, price=price, transactionCode=transactionCode)
        
        wallet = Wallet.objects.get(user_id=request.user.id)
        wallet.balanceCookie += int(cookie)
        wallet.save()


        return HttpResponseRedirect(reverse("confirmPayment"))
    cookieCoins = CookieCoin.objects.get(pk=cookie_id)
    return render(request, 'users/confirmCookie.html',{
        'cookieCoin' : cookieCoins, 
        'wallet' : wallet,
    })

def confirmPayment(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    wallet = Wallet.objects.get(user_id=request.user.id)

    return render(request, 'users/confirmPayment.html',{
        'wallet': wallet
    })
    # cookieCoins = CookieCoin.objects.get(pk=cookie_id)
    # return render(request, 'users/confirmCookie.html',{
    #     'cookieCoin': cookieCoins
    # })

    # if request.method == 'POST':
    #     cookieCoin = CookieCoin.objects.get(pk=cookie_id)
    #     user = User.objects.get(pk=request.user.id)
        
    #     check = History.objects.filter(user=user, cookieCoin=cookieCoin).first()
    #     if check is None:
    #         history = History.objects.create(user=user, cookieCoin=cookieCoin)
    #         return cookieCoin(request)

    #     else: 
    #         return render(request, 'course/cookieCoin.html', {
    #             'cookieCoin' : cookieCoin,
    #             'history': check is not None
    #         }, status=400)  
    # else:
    #     cookieCoin = CookieCoin.objects.get(pk=cookie_id)
    #     user = User.objects.get(pk=request.user.id)
    #     check = History.objects.filter(user=user, cookieCoin=cookieCoin).first()

    #     return render(request, 'course/cookieCoin.html', {
    #         'cookieCoin' : cookieCoin, 
    #         'history': check is not None
    #     }, status=400) 

# ------------------------------------------------------------
# ----------------------chom---------------------------------


def homepage(request):
    if not request.user.is_superuser:
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
    
        wallet = Wallet.objects.get(user_id=request.user.id)
        blog = Blog.objects.filter(blogType=1, recommended=True).all()
        like = LikeBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
        print(like)
        maxlen = len(blog)
        return render(request, 'users/homepage.html', {
            'blogs': blog,
            'like': like,
            'maxlen': maxlen,
            'wallet' : wallet,
        })
    else:
        return HttpResponseRedirect(reverse('homepageadmin'))


def members(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    wallet = Wallet.objects.get(user_id=request.user.id)

    return render(request,'users/members.html' , {
        'wallet':wallet
    })

def createblog(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    global userID
    try:
        user_id = request.user.id
        wallet = Wallet.objects.get(user_id=user_id)
    except Wallet.DoesNotExist:
        user_id = None

    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        title = request.POST['title']
        introduction = request.POST['introduction']
        detail = request.POST['detail']
        tag1 = request.POST.get("tag1", False)
        tag2 = request.POST.get("tag2", False)
        tag3 = request.POST.get("tag3", False)
        tag4 = request.POST.get("tag4", False)
        tag5 = request.POST.get("tag5", False)
        tag6 = request.POST.get("tag6", False)
        tag7 = request.POST.get("tag7", False)
        date1 = request.POST['date1']
        image = request.FILES['image']
        expectCookies = request.POST['expectCookies']

        blog = Blog.objects.create(user=user,title=title,
        introduction=introduction,detail=detail,
        tag1=tag1,tag2=tag2,tag3=tag3,tag4=tag4,tag5=tag5,tag6=tag6,tag7=tag7,date1=date1,image=image,donate=0,blogType=0,recommended=False,
        like=0,expectCookies=expectCookies)

        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'users/createBlog.html', {
        'wallet':wallet
    })

def homepageadmin(request):
    wallet = Wallet.objects.get(user_id=request.user.id)

    if not request.user.is_superuser:
        return loginPage(request)
    userId=1
    blogs = Blog.objects.filter().all()
    blog1 = [1,2,3]
    print(blogs)
    return render(request, 'users/homepageadmin.html',{
        'blogs': blogs,
    })

def detailadmin(request, detail_id):
    blog = Blog.objects.get(id = detail_id)
    viewed = ViewBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
    if detail_id not in viewed:
        views = ViewBlog.objects.create(user=request.user, blog=blog)
        blog.views += 1
        blog.save()
   
    return render(request,'users/detailadmin.html', {'blog':blog})

def verify(request, id):
    blog = Blog.objects.get(id = id)
    blog.blogType = 1
    blog.save()   
    return HttpResponseRedirect(reverse("homepageadmin"))
    
def recommended(request, id):
    blog = Blog.objects.get(id = id)
    blog.recommended = True
    blog.save()   
    return HttpResponseRedirect(reverse("homepageadmin"))
# ---------------------------------------------------------------
# -------------------------safe---------------------------------


def loginPage(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse('homepageadmin'))
            else:
                return homepage(request)
                #return HttpResponseRedirect(reverse('homepage'))
        else:
            return render(request, 'users/loginUser.html', {
                'message': 'Invalid credentials.'
            }, status=400)

    return render(request, 'users/loginUser.html')

# Create your views here.


def register(request):  # register
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmPassword = request.POST["cpassword"]
        userType = request.POST["userType"]
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        email = request.POST["email"]

        if (password == confirmPassword):
            user = User.objects.create_user(
                username=username, password=password, email=email, first_name=firstname, last_name=lastname)

            if (userType == "1"):
                orgName = request.POST["orgName"]
                fday = request.POST["fday"]
                country = request.POST["country"]
                address = request.POST["address"]
                phone = request.POST["phone"]
                image = request.FILES["image"]
                accountO = AccountOrganization.objects.create(
                    user=user, foundingDay=fday, phone=phone, address=address, orgName=orgName, country=country, image=image)

            elif (userType == "2"):
                bday = request.POST["bday"]
                country = request.POST["country"]
                address = request.POST["address"]
                phone = request.POST["phone"]
                image = request.FILES["image"]
                accountU = AccountUser.objects.create(
                    user=user, birthday=bday, phone=phone, address=address, country=country, image=image)


            wallet = Wallet.objects.create(user=user, balanceCookie=0)
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/registerUserPpl.html")



def reportBlog(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    try:
        user_id = request.user.id
        wallet = Wallet.objects.get(user_id=user_id)
    except Wallet.DoesNotExist:
        user_id = None

    blogID = id
    if request.method == "POST":
        user = User.objects.get(pk=request.user.id)
        blog = Blog.objects.get(pk=id)
        reason1 = request.POST.get("reason1", False)
        reason2 = request.POST.get("reason2", False)
        reason3 = request.POST.get("reason3", False)
        reason4 = request.POST.get("reason4", False)
        reason5 = request.POST.get("reason5", False)
        reason6 = request.POST.get("reason6", False)
        otherReason = request.POST.get("otherReason")
        reportBlog = ReportBlog.objects.create(reason1=reason1, reason2=reason2, reason3=reason3,
                                               reason4=reason4, reason5=reason5, reason6=reason6,
                                               otherReason=otherReason, user=user,
                                               blog=blog)

        reportCount = ReportBlog.objects.filter(blog_id=blogID).all()
        countReport = len(reportCount)
        if countReport >= 5:
            blog = Blog.objects.filter(pk=blogID).get()
            blog.blogType = 2
            blog.save()
        
        return HttpResponseRedirect(reverse("detail", args=[id]))
    return render(request, 'users/reportBlog.html', {
        'blogID': blogID, 
        'wallet': wallet, 
    })
#------------------------------------------------------------
#---------------------------fe-------------------------------


def donate(request, id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"), status=400)
    global userID
    wallet = Wallet.objects.get(user_id=request.user.id)

    blogs = Blog.objects.get(pk=id)
    if request.method == "POST":
        donate = request.POST["donate"]
        transactionCode = randint(1, 100000)
        if wallet.balanceCookie >= int(donate):
            account = History.objects.create(
                title=blogs.title, historyType=False, date=datetime.date.today(), time=time.strftime("%H:%M:%S", time.localtime()), price='0', userID=request.user.id, transactionCode=transactionCode, cookie=donate)
            
            # if wallet.balanceCookie >= int(donate):
            wallet = Wallet.objects.get(user_id=request.user.id)
            wallet.balanceCookie -= int(donate)
            wallet.save()

            blog = Blog.objects.get(pk=id)
            blog.donate += int(donate)
            blog.save()
        
        return HttpResponseRedirect(reverse("detail", args=[id]))
    return render(request, 'users/detail.html',{
        'wallet' : wallet,
        'blog' : blogs,
    })

def searchBar(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    user_id = request.user.id
    wallet = Wallet.objects.get(user_id=user_id)

    if request.method == "GET":
        searched = request.GET.get('searched')
        if searched:
            blogs = Blog.objects.filter(title__contains=searched)
            return render(request, 'users/searchfor.html', {'blogs': blogs})
        else:
            print("No information to show")
            return render(request, 'users/searchfor.html', {'wallet':wallet})

def BlogView(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    wallet = Wallet.objects.get(user_id=request.user.id)
    blogs = Blog.objects.filter(blogType = 1).all()
    like = LikeBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
    print(like)
    return render(request, 'users/blogpageUser.html', {'blogs':blogs, 'like':like, 'wallet':wallet})

def DetailView(request, detail_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    wallet = Wallet.objects.get(user_id=request.user.id)
    blog = Blog.objects.get(id = detail_id)
    viewed = ViewBlog.objects.filter(user_id=request.user.id).values_list('blog_id', flat=True)
    if detail_id not in viewed:
        views = ViewBlog.objects.create(user=request.user, blog=blog)
        blog.views += 1
        blog.save()
   
    return render(request,'users/detail.html', {'blog':blog, 'wallet':wallet})

def notVerifiedPageAdmin(request):

    if not request.user.is_superuser:
        return loginPage(request)
    if request.user.is_superuser:
        blogs = Blog.objects.filter(blogType=0).all()
        blog1 = [1, 2, 3]
        like = LikeBlog.objects.filter(
            user_id=request.user.id).values_list('blog_id', flat=True)
        print(like)
        print(blogs)
        return render(request, 'users/notVerifiedPageAdmin.html', {
            'blogs': blogs,
            'like': like
        })

def reportPageAdmin(request):

    if not request.user.is_superuser:
        return loginPage(request)
    if request.user.is_superuser:
        blogs = Blog.objects.filter(blogType=2).all()
        blog1 = [1, 2, 3]
        like = LikeBlog.objects.filter(
            user_id=request.user.id).values_list('blog_id', flat=True)
        print(like)
        print(blogs)
        return render(request, 'users/reportPageAdmin.html', {
            'blogs': blogs,
            'like': like
        })