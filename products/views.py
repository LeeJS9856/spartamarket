from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
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