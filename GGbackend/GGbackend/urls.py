"""
URL configuration for GGbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from myapp.views import Pyro,Bsfl,Admin,user,plastic_collect,get_user_ids,bsfl_collect,get_Bsflweight,get_Pyroweight,scan_weight,update_weight,update_user_weight,get_current_user

urlpatterns = [
    path('admin/', admin.site.urls),
   path('pyro/', Pyro, name='pyro'),
   path('bsfl/',Bsfl,name='Bsfl'),
   path('machineadmin/',Admin,name='Admin'),
   path('user/',user,name='user'),
   path('plastic_collect/',plastic_collect,name='plastic_collect'),
   path('get_user_ids/',get_user_ids,name='get_user_ids'),
#    path('weight/',weight,name='weight'),
   path('bsfl_collect/',bsfl_collect,name='bsfl_collect'),
   path('get_Pyroweight/',get_Pyroweight,name='get_Pyroweight'),
   path('get_Bsflweight/',get_Bsflweight,name='get_Bsflweight'),
   path('scan_weight/',scan_weight,name='scan_weight'),
   path('update_weight/',update_weight,name='update_weight'),
   path('update_user_weight/',update_user_weight,name='update_user_weight'),
   path('get_current_user/',get_current_user,name='get_current_user'),

   
]
