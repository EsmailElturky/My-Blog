from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from .forms import CommentForm
from .models import Post, Author, Tag


# Create your views here.


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by('-date')[0:3]
#     return render(request, 'blog/home.html', {"posts": latest_posts})

class StartingPageView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().order_by('-date')[0:3]
        return context


# def posts(request):
#     all_posts = Post.objects.all().order_by('-date')
#     return render(request, 'blog/all-posts.html', {"all_posts": all_posts})


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ['-date']
    context_object_name = "all_posts"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["has_read_later_posts"] = True
        return context


# def post_detail(request, slug):
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(request, 'blog/post-detail.html', {'post': identified_post, 'post_tags': identified_post.tags.all()})
class SinglePostView(View):
    def get(self, request, slug):
        identified_post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm()
        comments = identified_post.comments.all().order_by('-id')
        context = {'post': identified_post, 'post_tags': identified_post.tags.all(), 'comment_form': comment_form,
                   'comments': comments}
        if self.request.session.get('saved_posts', []) is not None:
            context["has_read_later_posts"] = str(identified_post.id) in self.request.session.get('saved_posts', [])
        else:
            context["has_read_later_posts"] = True
        return render(request, 'blog/post-detail.html',
                      context)

    def post(self, request, slug):
        identified_post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = identified_post
            new_comment.save()
            return redirect('post_detail_page', slug=slug)
        return render(request, 'blog/post-detail.html',
                      {'post': identified_post, 'post_tags': identified_post.tags.all(), 'comment_form': comment_form})

    def get_context_data(self, **kwargs):
        comment_form = CommentForm()
        context = super().get_context_data(**kwargs)
        context["post_tags"] = self.object.tags.all()
        context["comment_form"] = comment_form
        if self.request.session.get('saved_posts', []) is not None:
            context["has_read_later_posts"] = self.object.id in self.request.session['saved_posts']
        else:
            context["has_read_later_posts"] = False
        return context


class AddToReadLaterPostsView(View):

    def post(self, request):
        post_id = request.POST['post_id']
        stored_posts = request.session.get('saved_posts')
        if stored_posts is None:
            stored_posts = []

        if request.POST['post_id'] not in stored_posts:
            stored_posts.append(post_id)
            request.session['saved_posts'] = stored_posts
        else:
            stored_posts.remove(post_id)
            request.session['saved_posts'] = stored_posts
        return redirect('read_later_posts')


class ReadLaterPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ['-date']
    context_object_name = "all_posts"

    def get_queryset(self):
        return Post.objects.filter(id__in=self.request.session.get('saved_posts'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if len(self.get_queryset()) == 0:
            context["has_read_later_posts"] = False
        else:
            context["has_read_later_posts"] = True
        return context
