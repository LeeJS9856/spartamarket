from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash, get_user_model
from .forms import CustomUserChangeForm, CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from django.views.decorators.http import require_POST, require_http_methods
from django.shortcuts import get_object_or_404


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
    context = {
        "member": member,
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