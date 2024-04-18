from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import User
import sys, os

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from products.models import Article

def change_datetime(date_time_obj):
    date_obj = datetime.strptime(str(date_time_obj), "%Y-%m-%d %H:%M:%S.%f%z")
    return date_obj.strftime("%Y년 %m월 %d일")

def time_difference_in_words(time_str):
    input_time = datetime.strptime(str(time_str), "%Y-%m-%d %H:%M:%S.%f%z")
    now = datetime.now(input_time.tzinfo)
    time_diff = now - input_time
    minutes_diff = time_diff.total_seconds() / 60

    if minutes_diff < 10:
        return '방금'
    elif minutes_diff < 30:
        return '10분 전'
    elif minutes_diff < 60:
        return '30분 전'
    elif time_diff.days == 0:
        return f'{int(minutes_diff / 60)}시간 전'
    else:
        return f'{time_diff.days}일 전'

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_path = request.GET.get('next') or 'products:home'
            return redirect(next_path)
    else:
        form = CustomAuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('products:home')


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('products:home')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def profile(request, id):
    
    member = get_object_or_404(get_user_model(), id=id)
    articles = Article.objects.filter(author=member).order_by('-created_at')
    articles_id = [i.id for i in articles[:20]]
    articles_title = [i.title for i in articles[:20]]
    articles_created_at = [time_difference_in_words(i.created_at) for i in articles]
    
    like_count = Article.objects.filter(like_users=member).count()
    followers_count = User.objects.filter(followings=member).count()
    following_count = User.objects.filter(followers=member).count()
    context = {
        "member": member,
        "date_joined": change_datetime(member.date_joined),
        "articles": zip(articles_id, articles_title, articles_created_at),
        "like_count": like_count,
        "followers_count": followers_count,
        "following_count": following_count,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def update_profile(request):
    if request.method == "POST":
        form_password = CustomPasswordChangeForm(request.user, request.POST)
        form_name = CustomUserChangeForm(instance=request.user)
        if form_password.is_valid():
            form_password.save()
            update_session_auth_hash(request, form_password.user)
            return redirect('accounts:profile')
    else:
        form_password = CustomPasswordChangeForm(request.user)
        form_name = CustomUserChangeForm(instance=request.user)
    context = {
        'form_name': form_name,
        'form_password': form_password,
    }
    return render(request, 'accounts/update_profile.html', context)


@require_POST
def update_nickname(request):
    form_name = CustomUserChangeForm(request.POST, instance=request.user)
    if form_name.is_valid():
        form_name.save()
        return redirect('accounts:update_profile')

@require_POST
def follow(request, id):
    if request.user.is_authenticated:
        user = get_object_or_404(get_user_model(), id=id)
        if user != request.user :
            if user.followers.filter(id=request.user.id).exists() :
                user.followers.remove(request.user)
            else :
                user.followers.add(request.user)
        return redirect('accounts:profile', id = user.id)
    
    else :
        return redirect('accounts:login')