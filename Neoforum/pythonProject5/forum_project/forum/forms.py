from django import forms
from .models import Post, Comment, Category


class PostForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
        label="Ваше имя"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'author_name', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок поста'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Содержание поста'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    author_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}),
        label="Ваше имя"
    )

    class Meta:
        model = Comment
        fields = ['author_name', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш комментарий'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }