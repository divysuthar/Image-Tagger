from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('images/', takeImages, name='takeimages'),
    path('assign_tags/', assignTags, name='assignTags'),
]
