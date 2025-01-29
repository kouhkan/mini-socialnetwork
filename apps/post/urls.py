from django.urls import path

from apps.post.api.v1 import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="list-posts"),
    path("send/", views.SendPostView.as_view(), name="create-post"),
    path("<int:post_id>/", views.PostDetailView.as_view(), name="detail-post"),
    path("<int:post_id>/react/", views.ReactToPostView.as_view(), name="react-post"),
    path("<int:post_id>/rate/", views.RateToPostView.as_view(), name="rete-post"),
]
