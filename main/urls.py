from django.urls import path
from . import views

urlpatterns = [
    path('',views.welcome,name='welcome'),
    path('mainfunction/',views.mainfunction,name='mainfunction'),
]