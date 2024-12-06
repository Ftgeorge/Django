# Importing necessary modules from Django
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)  # Importing functions for rendering views and handling redirects
from django.contrib.auth.decorators import (
    login_required,
)  # Importing the login_required decorator to restrict access to certain views
from .models import Post  # Importing the Post model from the current app's models
from .forms import PostForm  # Importing the PostForm for creating and editing posts


# View to list all blog posts
def post_list(request):
    # Fetch all posts from the database, ordered by creation date in descending order
    posts = Post.objects.all().order_by("-created_at")
    # Render the post_list.html template with the fetched posts
    return render(request, "blog/post_list.html", {"posts": posts})


# View to display the details of a specific post
def post_detail(request, slug):
    # Retrieve the post by its slug or return a 404 error if not found
    post = get_object_or_404(Post, slug=slug)
    # Render the post_detail.html template with the retrieved post
    return render(request, "blog/post_detail.html", {"post": post})


# View to create a new post (not restricted to logged-in users)
def post_new(request):
    if request.method == "POST":  # Check if the request method is POST
        title = request.POST.get("title")  # Get the title from the form data
        content = request.POST.get("content")  # Get the content from the form data

        # Use the logged-in user as the author or set `author` to None if the user is anonymous
        author = request.user if request.user.is_authenticated else None

        # Create a new Post object with the provided title, content, and author
        Post.objects.create(title=title, content=content, author=author)

        # Redirect to the post list view after creating the post
        return redirect("post_list")

    # Render the post_form.html template for GET requests
    return render(request, "blog/post_form.html")


# View to create a new post (restricted to logged-in users)
@login_required
def post_create(request):
    if request.method == "POST":  # Check if the request method is POST
        form = PostForm(
            request.POST
        )  # Create a PostForm instance with the submitted data
        if form.is_valid():  # Check if the form is valid
            post = form.save(commit=False)  # Create a Post object but don't save it yet
            post.author = request.user  # Set the author to the logged-in user
            post.save()  # Save the Post object to the database
            return redirect("post_list")  # Redirect to the post list view
    else:
        form = PostForm()  # Create a new empty PostForm instance for GET requests
    # Render the post_form.html template with the form
    return render(request, "blog/post_form.html", {"form": form})


# View to edit an existing post (restricted to logged-in users)
@login_required
def post_edit(request, slug):
    # Retrieve the post by its slug or return a 404 error if not found
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":  # Check if the request method is POST
        form = PostForm(
            request.POST, instance=post
        )  # Create a PostForm instance with the submitted data and the existing post
        if form.is_valid():  # Check if the form is valid
            form.save()  # Save the changes to the post
            return redirect("post_list")  # Redirect to the post list view
    else:
        form = PostForm(
            instance=post
        )  # Create a PostForm instance pre-filled with the existing post data
    # Render the post_form.html template with the form
    return render(request, "blog/post_form.html", {"form": form})


# View to delete a post (restricted to logged-in users)
@login_required
def post_delete(request, slug):
    # Retrieve the post by its slug or return a 404 error if not found
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":  # Check if the request method is POST
        post.delete()  # Delete the post from the database
        return redirect("post_list")  # Redirect to the post list view
    # Render the post_confirm_delete.html template with the post to confirm deletion
    return render(request, "blog/post_confirm_delete.html", {"post": post})


# View to edit an existing post by post ID (not restricted to logged-in users)
def post_edit(request, post_id):
    # Retrieve the post by its ID or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":  # Check if the request method is POST
        post.title = request.POST.get(
            "title"
        )  # Update the post title with the submitted data
        post.content = request.POST.get(
            "content"
        )  # Update the post content with the submitted data
        post.save()  # Save the changes to the post
        return redirect("post_list")  # Redirect to the post list view
    # Render the post_edit.html template with the post to edit
    return render(request, "blog/post_edit.html", {"post": post})


# View to delete a post by post ID (not restricted to logged-in users)
def post_delete(request, post_id):
    # Retrieve the post by its ID or return a 404 error if not found
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":  # Check if the request method is POST
        post.delete()  # Delete the post from the database
        return redirect("post_list")  # Redirect to the post list view
    # Render the post_delete.html template with the post to confirm deletion
    return render(request, "blog/post_delete.html", {"post": post})
