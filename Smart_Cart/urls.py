"""
URL configuration for Smart_Cart project.

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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from website.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('register/',register,name='register'),
    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),
    path('mobiles/',mobiles,name='mobiles'),
    path('laptops/',laptops,name='laptops'),
    path('headphones/',headphones,name='headphones'),
    path('tv/',tv,name='tv'),
    path('ac/',ac,name='ac'),
    path('washing_mc/',washing_mc,name='washing_mc'),
    path('menswear/',menswear,name='menswear'),
    path('womenswear/',womenswear,name='womenswear'),
    path('kidswear/',kidswear,name='kidswear'),
    path('watches/',watches,name='watches'),
    path('shoes/',shoes,name='shoes'),
    path('books/',books,name='books'),
    path('bags/',bags,name='bags'),
    path('cart/',cart,name='cart'),
    path('checkout/',checkout,name='checkout'),
    path('update_item/',updateItem,name='update_item'),
    path('process_order/',processOrder,name='process_order'),
    path('about/',about,name='about'),
    path('support/',support,name='support'),
    path('consumer_policy/',consumer_policy,name='consumer_policy'),
    path('connect/',connect,name='connect'),
    path('contact/',contact,name='contact'),
]



urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)