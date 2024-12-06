# Importing necessary modules from Django
from django import forms  # Importing the forms module to create forms
from .models import Post  # Importing the Post model from the current app's models


# Defining a form class for creating and editing blog posts
class PostForm(forms.ModelForm):
    # Meta class to define metadata for the form
    class Meta:
        model = Post  # Specify the model that this form is associated with
        fields = ["title", "content"]  # Specify the fields to include in the form
