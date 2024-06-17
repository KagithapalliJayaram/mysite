from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Tutorial,TutorialCategory,TutorialSeries
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages

# Create your views here.
def single_slug(request,single_slug):
    category_slugs=[c.category_slug for c in TutorialCategory.objects.all()]
    # tutorial_slugs=[[c.tutorial_slug for c in Tutorial.objects.all()]]
    if single_slug in category_slugs:
        matching_series=TutorialSeries.objects.filter(tutorial_category__category_slug=single_slug)
        matching_tutorials=[]
        for m in matching_series.all():
            tut=Tutorial.objects.filter(tutorial_series__tutorial_series=m.tutorial_series)
            matching_tutorials.extend(tut)
        return render(request,'main/home.html',{'tutorials':matching_tutorials})
    else:
        tut_match=Tutorial.objects.get(tutorial_slug=single_slug)
        url='https://'+tut_match.tutorial_url
        return redirect(url)

def homepage(request):
    return render(request=request,
                  template_name='main/categories.html',
                  context={'categories':TutorialCategory.objects.all})

def register(request):
    if request.method == 'POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'New Account created for {username}')
            login(request,user)
            return redirect('main:homepage')
        else:
            for msg in form.error_messages:
                messages.error(request,f'{msg}:{form.error_messages[msg]}')
            
            return render(request,'main/register.html',{'form':form})


    form=UserCreationForm
    return render(request,'main/register.html',{'form':form})

def logout_request(request):
    logout(request)
    messages.info(request,'Logged out successfully')
    return redirect('main:homepage')

def login_request(request):
    if request.method == 'POST':
        form=AuthenticationForm(request,request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Logged in as {username}')
                return redirect('main:homepage')
        else:
            messages.error(request,'Invalid credentials')
    form=AuthenticationForm
    return render(request,'main/login.html',{'form':form})