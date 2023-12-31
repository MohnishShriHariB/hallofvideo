"""
URL configuration for halofvid project.

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
from django.contrib import admin,auth
from django.contrib.auth import views as auth_views
from django.urls import path
from hall import views
from django.conf import settings

urlpatterns = [

    path('admin/', admin.site.urls),
    path("",views.home,name="home"),
    path("dashboard",views.dashboard,name="dashboard"),

    path("signup",views.Signup.as_view(),name="signup"),
    path("login",auth_views.LoginView.as_view(),name="login"),
    path("logout",auth_views.LogoutView.as_view(),name="logout"),

    path("hallofvid/create",views.Createhall.as_view(),name="createhall"),
    path("hallofvid/<int:pk>",views.Detailhall.as_view(),name="Detailhall"),
    path("hallofvid/<int:pk>/update",views.Updatehall.as_view(),name="Updatehall"),
    path("hallofvid/<int:pk>/delete",views.Deletehall.as_view(),name="deletehall"),

    path("hallofvid/<int:pk>/addvideo",views.Addvideo,name="addvideo"),
    path("video/search",views.searchvideo,name="searchvideo"),
    path("video/<int:pk>/delete",views.deletevideo.as_view(),name="deletevideo"),
]
