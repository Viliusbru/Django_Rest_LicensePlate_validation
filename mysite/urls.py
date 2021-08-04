"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from myapi.views import index_view, PlateList, PlateDetail, UserCreate
from myapi import views

urlpatterns = [
    path('', index_view, name='index'),
    path('admin/', admin.site.urls),
    path('plates', PlateList.as_view()),
    path('plates/<int:pk>', PlateDetail.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('register', UserCreate.as_view()),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('plates/new', views.PlateByUserCreateView.as_view(), name='add_new'),
]
