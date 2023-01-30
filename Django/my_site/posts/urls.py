from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views


app_name = 'posts'

urlpatterns = [
    re_path(r'^$', views.IndexView.as_view(), name="index"),
    path('posts/create/', views.post_create, name="post_create"),
    path('posts/<int:post_id>/delete/', views.DeletePostView.as_view(), name="post_delete"),
    path('posts/<int:post_id>/delete-post-success/', TemplateView.as_view(template_name='posts/delete_success.html'), name="delete-post-success"),
    path('posts/<int:post_id>/edit/', views.EditPostView.as_view(), name="post_edit"),
    path('posts/<int:post_id>/like/', views.post_like, name="post_like"),
    re_path(r'^posts/(?P<post_id>\w+)/$', views.PostDetail.as_view(), name="post_detail"),
    path('feed/', views.FeedView.as_view(), name="feed"),

]