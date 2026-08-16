from django.urls import path
from . import views

urlpatterns = [
    path("userhome", views.userhome, name='userhome'),
    path('caption', views.caption, name='caption'),
    path('history', views.history, name='history'),
    path("logout", views.logout, name='logout')
    
]