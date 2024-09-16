from django.shortcuts import render, redirect   #added manually: redirect
#imported manually
#for forms
from .models import Post
from .forms import PostForm
#for user authentication
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout 
#for comments on post
from .models import Comment
from .forms import CommentForm


# Create your views here.
# views for blogs

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html',{'posts': posts})


# def post_detail(request, pk=None):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': posts})

#post_details after comments section added
def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    comments = post.comment_set.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'form': form})
    

#views for creating and editing blog posts

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


#changed from above view function
# def post_new(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_new.html', {'form': form})


def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


#login views
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')
    return render(request, 'blog/login.html', {})
    
#logout views
def logout_view(request):
    logout(request)
    return redirect('post_list')


#search request 
def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
    return render(request, 'blog/search.html', {'posts': posts, 'query': query})
