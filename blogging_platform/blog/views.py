
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm
from django.core.mail import send_mail



''' API function to create a new blog post.
    and Method using POST
    this Requires authentication (login_required).
    and Expects a JSON object containing 'title' and 'content' fields.''' 
    
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('blog_detail', pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog_detail', pk=post.pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('blog_list')
import requests

def fetch_blog_posts():
    url = 'http://localhost:8000/api/posts/'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def blog_list(request):
    posts = fetch_blog_posts()

    return render(request, 'blog_list.html', {'posts': posts})




def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            send_mail_notification(post, comment)
            return redirect('blog_detail', pk=post.id)  # Use pk=post.id instead of pk=post.pk
    else:
        form = CommentForm()
    return render(request, 'blog/blog_detail.html', {'post': post, 'comments': comments, 'form': form})
 
def send_mail_notification(post, comment):
    subject = f'New comment on blog post "{post.title}"'
    message = f'Hi {post.author.username},\n\nA new comment added to your blog post "{post.title}".\n\nComment by {comment.author.username}: {comment.text}\n\nYou can view the comment at: http://localhost:8000/blog/post/{post.pk}/'
    send_mail(subject, message, 'noreply@example.com', [post.author.email], fail_silently=False)




