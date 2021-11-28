from django.contrib import admin
from django.urls import path
from . import views
from .views import Login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login', Login.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('forgot-password', views.forgotp, name='forgotp'),
    path('movie-detail', views.movielink, name='movielink'),
    path('changeuser', Login.changeuser, name='changeuser'), 
    path('changeuser1', Login.change_userdet, name='changeuser1'), 
    path('home', Login.user, name='home'),
    path('logout', Login.logout_view, name='logout'),
    path('contactus', views.send_email, name='contactus'),
    path('contactus1', views.send_email1, name='contactus1'),
    path('textanalysis', Login.text_analysis, name='textanalysis'),
    path('register_success', views.register_success, name='register_success'),
    path('movielink', views.movielink, name='movielink'),
    path('filter', views.index, name='filter'),
    path('filter2', Login.user, name='filter2'),
]
