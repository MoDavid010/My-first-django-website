from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DeleteView, UpdateView, DetailView

from .forms import PostCreateForm, CommentForm
from .models import Post, Comment


class IndexView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = "posts"
    queryset = Post.objects.annotate(likes_count=Count('likes')).order_by('-likes_count')[:10]


class FeedView(ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = "posts"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            queryset = Post.objects.filter(author__in=self.request.user.friends.all()).order_by('-date_pub')[:10]
        else:
            queryset = []
        return queryset


class PostDetail(DetailView):
    model = Post
    comment_form = CommentForm
    pk_url_kwarg = 'post_id'
    template_name = 'posts/post_detail.html'

    def get(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['comments'] = Comment.objects.filter(post__pk=post_id).order_by('-date_pub')[:5]
        context['comment_form'] = self.comment_form
        return self.render_to_response(context)

    def post(self, request, post_id, *args, **kwargs):
        self.object = self.get_object()
        form = self.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()

        context = self.get_context_data(object=self.object)
        context.update({
            'comments': Comment.objects.filter(post__pk=post_id).order_by('-date_pub')[:5],
            'comment_form': self.comment_form,
        })
        return self.render_to_response(context)


@login_required()
def post_create(request):
    template_name = 'posts/post_create.html'
    if request.method == 'GET':
        form = PostCreateForm()
        context = {'form': form}
        return render(request, template_name, context)
    elif request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('posts:post_detail', kwargs={'post_id': post.id}))
        else:
            context = {'form': form}
            return render(request, template_name, context)


class EditPostView(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'posts/post_edit.html'
    form_class = PostCreateForm

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        print(self.request.__dict__)
        if obj.author != self.request.user:
            raise Exception("You are not allowed!")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('posts:post_detail', args=(post_id,))


class DeletePostView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'posts/post_delete.html'

    def get_success_url(self):
        post_id = self.kwargs['post_id']
        return reverse('posts:delete-post-success', args=(post_id,))


def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user and request.user.is_authenticated:
        if request.user in post.likes.all():
            like = post.likes.get(pk=request.user.id)
            post.likes.remove(like)
        else:
            post.likes.add(request.user)
            post.save()
    return redirect(request.META.get('HTTP_REFERER'), request)
