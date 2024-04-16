from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from.models import Article
from .forms import ArticleForm

def home(request): 
    articles = Article.objects.all()
    context = {"articles" : articles}
    return render(request, 'products/home.html', context)

def article(request, id) :
    article = get_object_or_404(Article, id=id)
    context = {"article" : article}
    return render(request, 'products/article.html', context)

@login_required
def create(request) :
    if request.method == "POST" :
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid() :
            article = form.save(commit=False)
            article.author = request.user
            article.save() 
            return redirect("products:article", article.id)
    else :
        form = ArticleForm()
    context = {"form" : form}
    return render(request, 'products/create.html', context)

@login_required
@require_http_methods(["GET", "POST"])
def edit(request, id) :
    article = get_object_or_404(Article, id=id)
    if request.method == "POST" :
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid() :
            article = form.save(commit=False)
            article.author = request.user
            article.save() 
            return redirect("products:article", article.id)
    else :
        form = ArticleForm(instance=article)
    context = {
        "form" : form,
        "article" : article,
        }
    return render(request, 'products/edit.html', context)

@require_POST
def delete(request, id) :
    if request.user.is_authenticated:
        article = get_object_or_404(Article, id=id)
        if request.method == "POST" :
            article.image.delete()
            article.delete()
            return redirect("products:home")
        context = {"article" : article}
        return render(request, 'products/delete.html', context)
    

@require_POST
def like(request, id) :
    if request.user.is_authenticated:
        article = get_object_or_404(Article, id=id)
        if article.like_users.filter(id=request.user.id).exists() :
            article.like_users.remove(request.user)
        else :
            article.like_users.add(request.user)
        return redirect("products:article", article.id)
    return redirect("accounts:login")