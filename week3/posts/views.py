from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
# from .models import Student
from posts.models import *
import json, datetime

def hello_world(request) :
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello likelion-12th!!"
        })
    
def index(request):
    return render(request, 'index.html')

@require_http_methods(["GET"])
def get_post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "writer" : post.writer,
        "category" : post.category,
    }

    return JsonResponse({
        'status' : 200,
        'message' : '게시글 조회 성공', 
        'data' : post_detail_json
    })

@require_http_methods(["POST", "GET"])
def post_list(request):

    if request.method == "POST":
        
        new_post = Post.objects.create(
            writer = request.POST.get('writer'),
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            category = request.POST.get('category')
        )

        new_post_json = {
            "id" : new_post.id,
            "writer" : new_post.writer,
            "title" : new_post.title,
            "content" : new_post.content,
            "category" : new_post.category
        }

        image_file = request.FILES.get("image")
        new_image_json = {}
        if image_file is not None:
            new_image = Image.objects.create(
                post_id = new_post,
                image=image_file
                )

            new_image_json = {
                "post_id" : new_image.post_id.id,
                "image_url" : new_image.image.url
            }

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 생성 성공",
            "post_data" : new_post_json,
            "image_data" : new_image_json
        })
    
    if request.method == "GET":
        post_all = Post.objects.all()
        image_all = Image.objects.all()

        post_json_all = []

        for post in post_all:
            post_json = {
                "id" : post.id,
                "title" : post.title,
                "writer" : post.writer,
                "content" : post.content,
                "category" : post.category
            }

            # Post 게시글에 이미지가 있는 경우 함께 조회.
            i = 1
            images = Image.objects.filter(post_id=post)
            for image in images:
                post_json["image" + str(i)] = image.image.url
                i += 1
            
            post_json_all.append(post_json)
            
            
        
        return JsonResponse({
            "status" : 200,
            "message" : "게시글 목록 조회 성공",
            "data" : post_json_all
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)

        post_json = {
            "id" : post.id,
            "title" : post.title,
            "writer" : post.writer,
            "content" : post.content,
            "category" : post.category
        }

        i = 1
        images = Image.objects.filter(post_id=post)
        for image in images:
            post_json["image" + str(i)] = image.image.url
            i += 1

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 조회 성공",
            "data" : post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=id)

        update_post.title = body["title"]
        update_post.content = body["content"]
        update_post.category = body["category"]

        update_post.save()

        update_post_json = {
            "id" : update_post.id,
            "title" : update_post.title,
            "writer" : update_post.writer,
            "content" : update_post.content,
            "category" : update_post.category
        }

        return JsonResponse({
            "status" : 200,
            "message" : "게시물 수정 성공",
            "data" : update_post_json
        })

    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id) 

        delete_post.delete()

        return JsonResponse({
            "status" : 200,
            "message" : "게시글 삭제 성공",
            "data" : None
        })
    
@require_http_methods(["POST", "GET"])
def comment_list(request, id):
    
    # 댓글 작성 api
    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))

        post = get_object_or_404(Post, pk=id)

        new_comment = Comment.objects.create(
            # 외래키로 연결된 컬럼의 경우 객체를 생성할 때 참조하는 테이블의 객체를 넣어줘야 함.
            post_id = post,
            writer = body['writer'],
            content = body['content']
        )

        new_comment_json = {
            "id" : new_comment.id,
            # 외래키로 연결된 컬럼의 경우 객체가 저장되어 있음.
            "post_id" : new_comment.post_id.id,
            "writer" : new_comment.writer,
            "content" : new_comment.content
        }

        return JsonResponse({
            "status" : 200,
            "message" : "댓글 게시 성공!",
            "data" : new_comment_json
        })

    # 댓글 목록 조회 api.
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)
        comment_all = Comment.objects.filter(post_id=post)

        comment_all_json = []

        for comment in comment_all:
            comment_json = {
                "id" : comment.id,
                "post_id" : comment.post_id.id,
                "writer" : comment.writer,
                "content" : comment.content
            }

            comment_all_json.append(comment_json)
        
        return JsonResponse({
            "status" : 200,
            "message" : "게시글 댓글 목록 조회 성공!",
            "data" : comment_all_json
        })
    
@require_http_methods(["GET"])
def recent_post_list(request):

    if request.method == "GET":
        # 현재 시간 기준으로 일주일 전의 시간을 start_date로 지정.
        start_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
        # {컬럼명}__gte로 start_date보다 뒤에 만들어진 객체를 filter로 찾고 '-created_at'을 사용해서 정렬.
        post_all = Post.objects.filter(created_at__gte=start_date).order_by('-created_at')

        post_all_json = []

        for post in post_all:
            post_json = {
                "id" : post.id,
                "title" : post.title,
                "writer" : post.writer,
                "content" : post.content,
                "category" : post.category,
                "created_at" : post.created_at
            }

            post_all_json.append(post_json)

        return JsonResponse({
            "status" : 200,
            "message" : "최근 일주일 간 작성된 게시글 목록 조회 성공",
            "data" : post_all_json
        })

# 이미지 파일 업로드 테스트 용 임시 api.
@require_http_methods(["POST"])
def update_image(request):
    
    if request.method == "POST":
        image_file = request.FILES.get('image')

        new_image = Image.objects.create(
            # 항상 id가 1인 Post 객체를 참조하는 Image 객체를 생성함.
            post_id = Post.objects.get(id=1),
            image = image_file
        )

        new_image_json = {
            "post_id" : new_image.post_id.id,
            "image_url" : new_image.image.url
        }

        return JsonResponse({
            "status" : 200,
            "message" : "이미지 업로드 성공",
            "data" : new_image_json
        })