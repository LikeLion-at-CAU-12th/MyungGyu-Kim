from django.urls import path
from posts.views import *

urlpatterns = [
    path('', hello_world, name = 'hello_world'),
    path('page', student_view, name = 'student_view'),
    path('introduction', introduction, name = 'introduction'),
]