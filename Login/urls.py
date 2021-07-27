"""Login URL Configuration

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
from django.urls import path
from pages.views import home_view,signup_view, storage_view,file_list_view,file_rendering,dashboard_view_new,userdetails_view,trash_view,user_detail_update,log_out
from users.views import user_detail_view,signupcreation
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name='home'),
    path('user/',user_detail_view),
    path('signup/',signup_view),
    path('user_signup/',signupcreation),
    path('upload_file/',storage_view),
    path('file_view/',file_list_view),
    path('download/<str:username_from_url>/<str:filename_from_url>',file_rendering),
    path('dashboard/',dashboard_view_new),
    path('userdet/',userdetails_view),
    path('delete/<str:trash_file>',trash_view),
    path('update_user_detail/',user_detail_update),
    path('logout/',log_out)
]
