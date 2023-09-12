from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TodoForm, WorkForm, ViewForm
from .models import Catalog
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    works = Catalog.objects.all()
    return render(request, 'userpage/home.html', {"works": works})


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'userpage/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('currentuser')
            except IntegrityError:
                return render(request, 'userpage/signupuser.html',
                              {'form': UserCreationForm(),
                               'error': 'Такое имя пользователя уже существует! Попробуйте другое'})
        else:
            return render(request, 'userpage/signupuser.html',
                          {'form': UserCreationForm(),
                           'error': 'Пароли не совпали!'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'userpage/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'userpage/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Неверные данные для входа'})
        else:
            login(request, user)
            return redirect('currentuser')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currentuser(request):
    works = Catalog.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'userpage/currentuser.html', {'works': works})

@login_required
def createorder(request):
    if request.method == 'GET':
        return render(request, 'todo/createorder.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('currentuser')
        except ValueError:
            return render(request, 'todo/createorder.html',
                          {'form': TodoForm(),
                           'error': 'Переданы неверные данные, попробуйте ещё раз'})


def work(request, pk):
    work_obj = Catalog.objects.get(id=pk)
    context = {'work': work_obj}
    return render(request, 'userpage/single-work.html', context)

@login_required
def vieworder(request):
    work_obj = Catalog.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'userpage/vieworder.html', {'work': work_obj})

@login_required
def completeorder(request, catalog_pk):
    work = get_object_or_404(Catalog, pk=catalog_pk, user=request.user)
    if request.method == 'POST':
        work.date_completed = timezone.now()
        work.save()
        return redirect('currentuser')


@login_required
def deleteorder(request, catalog_pk):
    work = get_object_or_404(Catalog, pk=catalog_pk, user=request.user)
    if request.method == 'POST':
        work.delete()
        return redirect('currentuser')

@login_required
def completedorders(request):
    works = Catalog.objects.filter(user=request.user,
                                date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'userpage/completedorders.html', {'works': works})


def add_work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('currentuser')
    else:
        form = WorkForm()
    return render(request, 'userpage/add_work.html', {'form': form})
