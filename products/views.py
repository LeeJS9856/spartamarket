from datetime import datetime
from .forms import ArticleForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods, require_POST
from .models import Article


def time_difference_in_words(time_str):
    input_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f%z")
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

def format_price(price):
    if price >= 10000:
        return f"{round(price / 10000)}만원"
    elif price >= 1000:
        thousands = round(price / 1000)
        if thousands >= 10:
            return f"{thousands}천원"
        else:
            hundreds = round((price % 10000) / 100)
            return f"{thousands}천 {hundreds}백원"
    else:
        return f"{price}원"

def home(request):
    articles = Article.objects.all()
    for article in articles :
        article.price = format_price(article.price) 
    context = {"articles": articles}
    return render(request, 'products/home.html', context)


def article(request, id):
    article = get_object_or_404(Article, id=id)
    article_time = time_difference_in_words(str(article.created_at))
    context = {
        "article": article,
        "article_time": article_time,
    }
    return render(request, 'products/article.html', context)


@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("products:article", article.id)
        context = {"form": form}
        return render(request, 'products/create.html', context)
    else:
        form = ArticleForm()
    context = {"form": form}
    return render(request, 'products/create.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("products:article", article.id)
    else:
        form = ArticleForm(instance=article)
    context = {
        "form": form,
        "article": article,
    }
    return render(request, 'products/edit.html', context)


@require_POST
def delete(request, id):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, id=id)
        if request.method == "POST":
            article.image.delete()
            article.delete()
            return redirect("products:home")
        context = {"article": article}
        return render(request, 'products/delete.html', context)


@require_POST
def like(request, id):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, id=id)
        if article.like_users.filter(id=request.user.id).exists():
            article.like_users.remove(request.user)
        else:
            article.like_users.add(request.user)
        return redirect("products:article", article.id)
    return redirect("accounts:login")
