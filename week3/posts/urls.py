from django.urls import path
from posts.views import *

urlpatterns = [
    # path('', hello_world, name = 'hello_world'),
    # path('page', student_view, name = 'student_view'),
    # path('introduction', introduction, name = 'introduction'),
    # path('<int:id>', get_post_detail, name='게시글 조회'),

    # path('', post_list, name = 'post_list'),
    # path('<int:id>', post_detail, name = 'post_detail'),
    # path('<int:id>/comment', comment_list, name='comment_list'),
    # path('recent', recent_post_list, name='recent_pos-t_list'),
    # path('image', update_image, name='update_image'),
    path('', PostList.as_view()),
    path('<int:id>/', PostDetail.as_view()),
    path('comment/', CommentDetail.as_view()),
    path('comment/<int:id>/', CommentDetail.as_view()),
]