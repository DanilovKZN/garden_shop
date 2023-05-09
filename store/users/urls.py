from django.urls import path

from users.views import (
    login_enter, registration, profile,
    logout
)


app_name = 'users'

urlpatterns = [
    path('login/', login_enter, name='login_enter'),
    path('registration/', registration, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name= 'logout')
]
