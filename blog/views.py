from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import BlogPost, Category
from .forms import BlogPostForm
from users.models import CustomUser

@login_required
def create_blog_post(request):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('my_blog_posts')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/create_post.html', {'form': form})

@login_required
def edit_blog_post(request, post_id):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_blog_posts')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

@login_required
def delete_blog_post(request, post_id):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    
    if request.method == 'POST':
        post.delete()
        return redirect('my_blog_posts')
    
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def my_blog_posts(request):
    if request.user.user_type != 'doctor':
        return redirect('patient_dashboard')
    
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})

@login_required
def view_blog_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # If it's a draft, only the author can view it
    if post.is_draft and post.author != request.user:
        return redirect('blog_list')
    
    return render(request, 'blog/view_post.html', {'post': post})

@login_required
def blog_list(request):
    if request.user.user_type == 'doctor':
        return redirect('my_blog_posts')
    
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    
    if selected_category:
        try:
            selected_category = int(selected_category)
            posts = BlogPost.objects.filter(
                category_id=selected_category,
                is_draft=False
            ).order_by('-created_at')
        except ValueError:
            posts = BlogPost.objects.filter(is_draft=False).order_by('-created_at')
    else:
        posts = BlogPost.objects.filter(is_draft=False).order_by('-created_at')
    
    return render(request, 'blog/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'selected_category': selected_category
    })

@login_required
def category_list(request):
    if request.user.user_type == 'doctor':
        return redirect('my_blog_posts')
    
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})