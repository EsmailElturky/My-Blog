from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from blog import views

urlpatterns = [
                  path("", views.starting_page, name='starting_page'),
                  path("posts", views.posts, name='posts_page'),
                  path("posts/<slug:slug>", views.post_detail, name='post_detail_page'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
