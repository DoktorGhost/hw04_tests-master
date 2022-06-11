from django.forms import ModelForm

from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        labels = {'group': 'Группа', 'text': 'Текст'}
        fields = ["group", "text"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]