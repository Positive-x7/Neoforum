from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm, CategoryForm


class PostListView(ListView):
    model = Post
    template_name = 'forum/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('category')


class PostDetailView(DetailView):
    model = Post
    template_name = 'forum/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = self.object.comments.filter(is_active=True)
        return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        messages.success(self.request, 'Пост успешно создан!')
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'forum/post_form.html'

    def form_valid(self, form):
        messages.success(self.request, 'Пост успешно обновлен!')
        return super().form_valid(form)


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'forum/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Пост успешно удален!')
        return super().delete(request, *args, **kwargs)


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('post_detail', pk=post.pk)
    return redirect('post_detail', pk=post.pk)


class CategoryListView(ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'forum/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(category=self.object, is_published=True)
        return context


def home(request):
    categories = Category.objects.all()[:5]
    recent_posts = Post.objects.filter(is_published=True).select_related('category')[:5]
    return render(request, 'forum/home.html', {
        'categories': categories,
        'recent_posts': recent_posts
    })