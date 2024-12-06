# Importing necessary modules from Django
from django.urls import path  # Importing the path function to define URL patterns
from . import views  # Importing views from the current application

# Defining URL patterns for the blog application
urlpatterns = [
    # Route for the homepage that lists all posts
    path("", views.post_list, name="post_list"),
    # Route for creating a new post
    path("post/new/", views.post_new, name="post_new"),  # New route for creating a post
    # Route for viewing a specific post by its slug
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    # Duplicate route for creating a new post (this should be removed)
    path("post/new/", views.post_create, name="post_create"),
    # Route for editing a specific post by its ID
    path("post/<int:post_id>/edit/", views.post_edit, name="post_edit"),
    # Route for deleting a specific post by its ID
    path("post/<int:post_id>/delete/", views.post_delete, name="post_delete"),
]
