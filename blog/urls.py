from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
                  path("", views.StartingPageView.as_view(), name='starting_page'),
                  path("posts", views.AllPostsView.as_view(), name='posts_page'),
                  path('posts/read_later', views.AddToReadLaterPostsView.as_view(), name='read_later'),
                  path('read_later_posts', views.ReadLaterPostsView.as_view(), name='read_later_posts'),
                  path("posts/<slug:slug>", views.SinglePostView.as_view(), name='post_detail_page'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
