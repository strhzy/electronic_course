from django.contrib import admin
from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('catalog/', catalog, name='catalog'),
    path('<int:product_id>/', about, name='about'),
    path('profile/',profile_page, name="profile_page"),

    path('login/', login_user, name='login_page'),
    path('registration/', registration_user, name='registration_page'),
    path('logout/', logout_user, name='logout_page'),
]