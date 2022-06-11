from django.shortcuts import redirect, render, get_object_or_404
from .forms import CommentForm, PostForm
from .models import Post, Group, User
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
            'index.html',
            {'page': page, 'paginator': paginator}
       )

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'group.html', {'group':group, 'page':page, 'paginator':paginator})

@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
    form = PostForm()
    return render(request, 'new.html', {'form':form})

def year(request):
    year = dt.datetime.now().year
    return {'year':year}

def profile(request, username):
    author = get_object_or_404(User, username=username)
    last_post = Post.objects.all().filter(author__username=username).order_by("-pub_date")[0]
    post_list = Post.objects.all().filter(author__username=username)
    counter = post_list.count()
    paginator = Paginator(post_list, 5)  # показывать по 5 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(request, 'profile.html', {'page': page, 'author': author, 'counter': counter, 'last_post': last_post})
 
 
def post_view(request, username, post_id):
    author = get_object_or_404(User, username=username)
    post = get_object_or_404(Post, id=post_id)
    post_list = Post.objects.all().filter(author__username=username)
    counter = post_list.count()
    form = CommentForm(request.POST or None)
    comments = post.comments.all()
    return render(request, 'post.html', {'author': author, 'counter': counter, 'form': form, 
    'comments': comments, 'post': post})

@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, username=username)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)

    # if request.method == 'POST':
    if request.user != post.author:
        return redirect('post', username=post.author, post_id=post.id)
    if form.is_valid():
        form.save()
        return redirect('post', username=post.author, post_id=post.id)
    # form = PostForm(instance=post)
    return render(request, 'new.html',
                  {'form': form, 'post': post, 'author': author})

@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, id=post_id, author__username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        comment.save()
    return redirect('post', username=post.author, post_id=post.id)