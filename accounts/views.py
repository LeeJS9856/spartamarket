from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_http_methods

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == 'POST':
        pass
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