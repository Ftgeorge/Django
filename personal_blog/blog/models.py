# Importing necessary modules from Django
from django.db import models  # Importing the models module to define database models
from django.contrib.auth.models import (
    User,
)  # Importing the User model for author reference
from django.utils.text import slugify  # Importing slugify to create slugs from titles
import uuid  # Importing uuid to generate unique identifiers


# Base Class: BasePost
class BasePost(models.Model):
    # Title of the post, with a maximum length of 200 characters
    title = models.CharField(max_length=200)

    # Content of the post, stored as text
    content = models.TextField()

    # Foreign key relationship to the User model, allowing null values and blank entries
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Slug field for URL-friendly representation of the post title, must be unique
    slug = models.SlugField(unique=True, blank=True, null=True)

    # Date and time when the post was created, automatically set on creation
    created_at = models.DateTimeField(auto_now_add=True)

    # Overriding the save method to generate a slug if it is not provided
    def save(self, *args, **kwargs):
        # Check if the slug is not already set
        if not self.slug:
            # Generate a unique slug using the title and a UUID
            self.slug = slugify(self.title) + "-" + str(uuid.uuid4())[:8]
        # Call the superclass's save method to save the instance
        super().save(*args, **kwargs)

    # Polymorphic method: Can be overridden by subclasses
    def display_summary(self):
        return f"{self.title} - {self.content[:50]}..."

    class Meta:
        abstract = True  # This makes BasePost an abstract class (not instantiated directly)


# Subclass: Post
class Post(BasePost):
    # Additional field specific to the Post class
    is_published = models.BooleanField(default=False)

    # Overriding the display_summary method for polymorphism
    def display_summary(self):
        return f"Published: {self.is_published} - {self.title} - {self.content[:50]}..."


# Subclass: DraftPost
class DraftPost(BasePost):
    # Additional field specific to the DraftPost class
    draft_notes = models.TextField(blank=True, null=True)

    # Overriding the display_summary method for polymorphism
    def display_summary(self):
        return f"Draft Notes: {self.draft_notes} - {self.title} - {self.content[:50]}..."