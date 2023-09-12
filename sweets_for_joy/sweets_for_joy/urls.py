"""
URL configuration for sweets_for_joy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from sweets import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),

    # Works
    path('', views.home, name='home'),
    path('current/', views.currentuser, name='currentuser'),
    path('create/', views.createorder, name='createorder'),
    path('home/<str:pk>/', views.work, name='work'),
    path('works/<str:pk>/', views.vieworder, name='vieworder'),
    path('add_work/', views.add_work, name='add_work'),
    # дальше пока не работает, разобраться
    # path('works/<int:catalog_pk>/complete', views.completeorder, name='completeorder'),
    # path('works/<int:catalog_pk>/delete', views.deleteorder, name='deleteorder'),
    # path('completed/', views.completedorders, name='completedorders'),
    #
]
