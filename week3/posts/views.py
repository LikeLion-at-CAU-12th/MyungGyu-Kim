from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Student

def hello_world(request) :
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-12th!!"
        })
    
def index(request):
    return render(request, 'index.html')

def introduction(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공 !', 
            'data' : [
                {
                    "name" : "김명규",
                    "age" : 24,
                    "major" : "CSE"
                },
                {
                    "name" : "이영주",
                    "age" : 24,
                    "major" : "Department of Chinese Language and Literature"
                }
            ]
        },
        json_dumps_params={'ensure_ascii': False})
    
def student_view(request):
    students = Student.objects.all()
    me = students[0]
    my_duo = students[1]
    return render(request, 'student.html', {'me' : me, 'my_duo' : my_duo})