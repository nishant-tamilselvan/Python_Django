from django.shortcuts import render, get_object_or_404, redirect
from django.http import *
#from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from .models import profiles
from .forms import Profileregister,Profileupdate


def register(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        messages.error(request, "Please logout and try again!")
        return HttpResponseRedirect('/profiles/myprofile')
    else:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                messages.add_message(request,messages.SUCCESS,"Successfully created an User!")
                return HttpResponseRedirect("/profiles/")
        else:
            form = UserCreationForm()

    return render(request, "registration/register.html", {
        'form': form,
    })





def login_user(request):
    if request.user.is_authenticated():
        messages.add_message(request,messages.SUCCESS,"You are already logged in!")
        return HttpResponseRedirect("/profiles/")
    username = password = ''
    context = RequestContext(request)
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request,messages.SUCCESS,"Logged in successfully!")
                return HttpResponseRedirect('/profiles/')
            else: return HttpResponse("You're account is disabled.")
        else:
            messages.error(request,"username or Password invalid. Please try again!")
            return render_to_response('login.html', {}, context)

    return render_to_response('login.html', context_instance=context)


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect("/profiles/")

def profile_list(request):

    queryset = profiles.objects.all().order_by('-timestamp')[:10]
    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    content = {
        "objectset": queryset,
        "title": "list"
    }
    return render(request,"index.html", content)
    #return HttpResponse("<h1>Hello World</h1>")

def profile_list_all(request):

    queryset = profiles.objects.all().order_by('-timestamp')
    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()
    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)
    content = {
        "objectset": queryset1,
        "title": "list"
    }
    return render(request,"profiles.html", content)

def profile_search_list(request):

    queryset = profiles.objects.all().order_by('-timestamp')

    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()

    query1 = request.GET.get('religion')
    query2 = request.GET.get('gender')
    query3 = request.GET.get('maritalstatus')
    query4 = request.GET.get('min_age')
    query5 = request.GET.get('max_age')

    if query1 :#and query2 and query3 and query4 and query5 :
        queryset = queryset.filter(religion__icontains=query1)#.filter( p_age_max__lte=query5)
        queryset = queryset.filter(age__gte=int(query4))
        queryset = queryset.filter(age__lte=int(query5))
        queryset = queryset.filter(gender=query2)
        queryset = queryset.filter(maritalStatus__icontains=query3)

    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)

    content = {
        "page_list": queryset1,
        "objectset": queryset1,
        "title": "list"
    }
    return render(request, "profile_search.html", content)
    #return HttpResponse("<h1>Hello World</h1>")





def profile_search_id(request):

    queryset = profiles.objects.all().order_by('-timestamp')
    for object in queryset:
        if object.pId == "TMG":
            object.pId = "TMG00" + str(object.tmId)
            object.save()

    query = request.GET.get('pid')

    if query:
        instance = get_object_or_404(profiles,pId=str(query))
        return HttpResponseRedirect(instance.get_absolute_url())

    paginator = Paginator(queryset, 5)  # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        queryset1 = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset1 = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset1 = paginator.page(paginator.num_pages)

    content = {
        "objectset": queryset1,
        "title": "list"
    }
    return render(request, "profile_search_id.html", content)
    #return HttpResponse("<h1>Hello World</h1>")



@login_required(login_url="/login/")
def profile_create(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        userid = int(request.user.id)
        queryset = profiles.objects.filter(user=userid)

        if queryset:
            messages.error(request, "You have already created a profile!")
            return HttpResponseRedirect('/profiles/myprofile/')

        form = Profileregister(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            if instance.pId == "TMG":
                instance.pId = "TMG" + "00" + str(instance.tmId)
                instance.save()
            messages.add_message(request,messages.SUCCESS,"Successfully created a profile!")
            return HttpResponseRedirect("/profiles/myprofile")
        else:
            form = Profileregister(request.POST or None, request.FILES or None)
    content = {
        "form": form,
        "title": "Create/Register"
    }

    return render(request, "register.html", content)


def profile_detail(request, slug=None):
    instance = get_object_or_404(profiles, slug=slug)

    def create_pid():
        if instance.pId == "TMG" :
            instance.pId = "TMG"+"00" + str(instance.tmId)
            instance.save()

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_age():
        dob = calculate_age(instance.dateOfBirth)
        if instance.age == 0 :
            instance.age = dob
            instance.save()
        elif instance.age != dob :
            instance.age = dob
            instance.save()

    create_pid()
    update_age()

    content = {
        "detail_object": instance,
        "title": "Detail",

    }
    return render(request, "view_profile.html", content)

@login_required(login_url='/login/')
def my_profile(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        username = request.user.id
        instance1 = profiles.objects.filter(user = int(username))#get_object_or_404(profiles, user = int(username))
        if not instance1:
            messages.add_message(request,messages.ERROR,"Please create an Profile!")
            return HttpResponseRedirect("/profiles/create/")
        instance = get_object_or_404(profiles, user = int(username))

    else:
        messages.error(request, "Please login to view your profile!")
        return render_to_response('login.html', {}, context)

    def create_pid():
        if instance.pId == "TMG" :
            instance.pId = "TMG"+"00" + str(instance.tmId)
            instance.save()

    def calculate_age(born):
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def update_age():
        dob = calculate_age(instance.dateOfBirth)
        if instance.age == 0 :
            instance.age = dob
            instance.save()
        elif instance.age != dob :
            instance.age = dob
            instance.save()

    create_pid()
    update_age()

    content = {
        "detail_object": instance,
        "title": "my_Detail",

    }
    return render(request, "view_profile.html", content)


@login_required(login_url="/login/")
def myprofile_update(request):
    context = RequestContext(request)
    if request.user.is_authenticated():
        username = request.user.id
        instance = get_object_or_404(profiles, user=int(username))
        form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()
            messages.add_message(request,messages.SUCCESS,"Successfully updated your profile!")
            return HttpResponseRedirect("/profiles/myprofile/")
        else:
            form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
    else:
        messages.add_message(request,messages.ERROR,"Please login to edit your profile!")
        return HttpResponseRedirect("/login/")

    content = {
        "detail_object": instance,
        "title": "My Update Profile",
        "form":form,
    }
    return render(request, "profileupdate.html", content)


def profile_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(profiles, slug=slug)
    form = Profileupdate(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "successfully updated!")
        return HttpResponseRedirect(instance.get_absolute_url())
    else:
        messages.error(request,"Not updated!")

    content = {
        "detail_object": instance,
        "title": "Update Profile",
        "form":form,
    }
    return render(request, "profileupdate.html", content)



def profile_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(profiles, slug=slug)
    instance.delete()
    messages.success(request, "succesfully Deleted!")
    return redirect("profiles:list")