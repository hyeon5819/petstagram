from django.shortcuts import render, redirect
from board.models import Post, PostComment
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, TemplateView

### 중간 생략 #############


@login_required
def detail_post(request, id):
    post = Post.objects.get(id=id)
    post_comments = PostComment.objects.filter(post=post)
    # num_comments = len(post_comments)

    return render(request, 'detailpost/post_detail.html',
                  {'post': post, 'post_comments': post_comments,
                   # 'num_comments': num_comments,
                   })


@login_required()
def delete_post(request, id):
    my_tweet = Post.objects.get(id=id)
    my_tweet.delete()
    return redirect('/')


def update_post(request, id):
    post = Post.objects.get(id=id)

    if request.method == "POST":
        post.title = request.POST['title']
        post.content = request.POST['content']

        post.save()
        return render(request, 'detailpost/post_detail.html', {'post': post})
    else:
        return render(request, 'detailpost/update.html', {'post': post})


# # 댓글 좋아요 기능 미구현
# def post_comment_like(request, id):
#     post = Post.objects.get(id=id)
#     post_comments = PostComment.objects.filter(post=post)
#     num_comments = len(post_comments)
#     if request.method == 'POST':
#         post_comment = PostComment.objects.get(id=post_coment.id)
#         post_comment.like += 1
#         return render(request, 'detailpost/post_detail.html',
#                       {'post': post, 'post_comments': post_comments, 'num_comments': num_comments})
