from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .models import Post, Likes, Comments
from account.models import Profile
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib import messages
from django.views.decorators.cache import cache_page

@login_required(redirect_field_name='login')
def home_view(request) :
    posts = Post.objects.all().order_by('?')
    profile = request.user.profile

    return render(request, 'main/home.html', {'posts': posts, 'profile': profile,'emoji': ['&#128515;', '&#128513;', '&#128522;', '&#128524;']})

@csrf_exempt
def like_view(request) :
    data = json.loads(request.body)
    id = data['id']
    post_id = data['post_id']
    profile = Profile.objects.get(id=id)
    post = Post.objects.get(id=post_id)

    if Likes.objects.filter(profile=profile, post=post) :
        like = Likes.objects.get(profile=profile, post=post)
        like.delete()
        print('dislike')
        return JsonResponse({'stat': 'dislike'}, status=200)
    else :
        like = Likes.objects.create(profile=profile, post=post)
        like.save()
        print('like')
        return JsonResponse({'stat': 'like'}, status=200)

@login_required(redirect_field_name='login')
def post(request) :
    if request.method == 'POST' :
        cd = request.POST
        file = request.FILES
        content = cd.get('content')
        image = file.get('image')
        user = request.user.profile
        if image :
            post = Post.objects.create(
                profile=user,
                content=content,
                image=image
            )
            post.save()
            messages.success(request, 'Post created')
            return HttpResponseRedirect(reverse('home'))

        post = Post.objects.create(
                profile=user,
                content=content,
                image=image
            )
        post.save()
        messages.success(request, 'Post created')
        return HttpResponseRedirect(reverse('home'))
        
    else:
        return render(request, 'main/post.html')

@login_required(redirect_field_name='login')
def edit_post(request, id) :
    post = Post.objects.get(id=id)
    return render(request, 'main/edit.html', {'post': post})

@login_required(redirect_field_name='login')
def edit(request, id) :
    post = Post.objects.get(id=id)
    if request.method == 'POST' :
        cd = request.POST
        file = request.FILES
        content = cd.get('content')
        image = file.get('image')
        if image :
            post.content = content
            post.image=image
            post.save()
            messages.success(request, 'Post Edited')
            return HttpResponseRedirect(reverse('home'))

        post.content = content
        post.save()
        messages.info(request, 'Post Edited')
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponse('Invalid method')

def edit_profile(request) :
    if request.method == 'POST' :
        file = request.FILES
        image = file.get('image')
        profile = request.user.profile

        profile.profile_image = image
        profile.save()

        messages.success(request, 'Profile edited successfully!')
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponse('Invalid HTTP verb')
    
def retrieve_comment(request, id) :
    comments = Comments.objects.filter(post__id=id)
    comments_json = []
    for txt in comments :
        dict_compose = {
            'username': txt.profile.user.username,
            'content': txt.content,
            'profile_image': txt.profile.profile_image.url
        }
        comments_json.append(dict_compose)

    return JsonResponse({'comments': comments_json})

@csrf_exempt
def post_comment(request) :
    if request.method == 'POST' :
        body = json.loads(request.body)
        print(body)
        content = body['comment']
        profile = request.user.profile
        post_id = body['id']
        post = Post.objects.get(id=post_id)

        comment = Comments.objects.create(profile=profile, post=post, content=content)
        comment.save()

        return JsonResponse({'added': True}, status=200)

    else :
        return HttpResponse('Invalid HTTP verb')

def delete_post(request, id) :
    try:
        post = Post.objects.get(id=id)
        post.delete()
        messages.info(request, 'Post deleted successfully')
        return HttpResponseRedirect(reverse('home'))
    except :
        messages.error(request, 'A error occured')
        return HttpResponse(reverse('edit', args=[id]))