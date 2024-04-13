from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST, require_http_methods

@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            next_path = request.GET.get('next') or 'products:home'
            return redirect(next_path)
    else:
        form = AuthenticationForm()
    context = {
            'form': form,
    }
    return render(request, 'accounts/login.html', context)

@require_POST
def logout(request):
    pass
# Create your views here.

def signup(request):
    return render(request, 'accounts/signup.html')