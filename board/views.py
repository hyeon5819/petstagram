from django.shortcuts import render, redirect
from .models import Post, PostComment
from user.models import UserModel
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def create_feed_view(request):
    # 게시글 작성
    if request.method == 'GET':
        user = request.user.is_authenticated
        # 유저가 로그인 됐는지 확인
        if user:
            # 유저가 로그인 했을 때
            return render(request, 'board/post.html')
        else:
            # 유저가 로그인 하지 않았을 때
            return redirect('/login')
    elif request.method == 'POST':      # 사용자가 post 버튼을 눌러 게시를 했을지 실행됨
        user = request.user  # 게시글 작성시 필요해서 추가
        post = Post()

        post.author = user  # 게시글 작성시 필요해서 추가
        # 작성자 입력 란
        post.title = request.POST.get('title', '')
        post.content = request.POST.get('user-content', '')
        post.save()

        # return HttpResponse('create_feed_view_POST')

        # 작성 후 main으로 이동
        return redirect('/')

#           DEAD_CODE
# def delete_feed_view(request, id):
#     #게시글 삭제
#     feed = Post.objects.get(id=id)
#     feed.delete()
#     return  HttpResponse('delete_ok')
#     # working on it
#     # pass
#
# def update_feed_view(request):
#     #게시글 수정
#     pass
# def read_feed_view(request):
#     #게시글 조회
#     pass
#           DEAD_CODE_END


# 메인페이지 게시글 피드
def mainpage_feed(request):
    if request.method == 'GET':
        post_feeds = Post.objects.all().order_by('-create_at')
        # post_comments = PostComment.objects.filter(post=post)
        # num_comments = len(post_comments)

        return render(request, 'board/petstagram.html', {'post_fedds': post_feeds,
                                                         # 'num_comments': num_comments,
                                                         })


# 게시글 댓글기능 추가
@login_required
def post_comment(request, id):
    if request.method == 'POST':
        post_comment_content = request.POST.get('post_comment_content')
        user_id = request.user.id
        post = Post.objects.get(id=id)
        author = UserModel.objects.get(id=user_id)

        post_comment = PostComment(
            post=post, author=author, content=post_comment_content)
        post_comment.save()

        # 댓글개수
        # 댓글이 생성되면
        # post.comment_count += 1
        # post.save()

        post_comments = Post.objects.get(id=id).comments.all()
        post.comment_count = len(post_comments)
        post.save()
        print(PostComment.objects.get(id=22))
        print(PostComment.objects.get(id=22).post)
        print(post_comment.post)

        return render(request, 'detailpost/post_detail.html', {'post': post,
                                                               'post_comments': post_comments,
                                                               })


# 댓글 삭제
@login_required
def post_comment_delete(request, id):
    post_comment = PostComment.objects.get(id=id)
    post = Post.objects.get(id=post_comment.post.id)
    post_comments = PostComment.objects.filter(post=post)

    if request.user == post_comment.author or request.user == post_comment.post.author:
        post_comment.delete()
        post.comment_count = len(post_comments)
        post.save()

    return render(request, 'detailpost/post_detail.html',
                  {'post': post, 'post_comments': post_comments,
                   })


# 댓글 수정
@login_required
def post_comment_update(request, id):
    if request.method == 'GET':
        post_comment = PostComment.objects.get(id=id)
        post = Post.objects.get(id=post_comment.post.id)
        return render(request, 'board/post_comment_update.html', {'post': post, 'post_comment': post_comment})

    elif request.method == 'POST':
        post_comment = PostComment.objects.get(id=id)
        post = Post.objects.get(id=post_comment.post.id)
        post_comment.content = request.POST.get('post_comment_content')
        post_comment.save()
        post_comments = PostComment.objects.filter(post=post)
        return render(request, 'detailpost/post_detail.html',
                      {'post': post, 'post_comments': post_comments,
                       })


# # 좋아요기능 미구현
# def post_comment_like(request, id):
#     post = Post.objects.get(id=id)
#     post_comments = PostComment.objects.filter(post=post)
#     num_comments = len(post_comments)
#     post_comment_num = request.POST['like']
#     post_comment = PostComment.objects.get(id=post_comment_num)
#     if request.method == 'POST':
#         post_comment.like += 1
#         return render(request, 'detailpost/post_detail.html',
#                       {'post': post, 'post_comments': post_comments, 'num_comments': num_comments})
