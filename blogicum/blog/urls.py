from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.CategoryPostsView.as_view(),
         name='category_posts'),

    path('profile/<slug:username>/', views.ProfileView.as_view(),
         name='profile'),
    path('edit_profile/', views.ProfileViewEdit.as_view(),
         name='edit_profile'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostEditView.as_view(), name='edit_post'),
    path('posts/create/', views.PostCreateView.as_view(),name='create_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='delete_post'),
    path('posts/<int:pk>/comment/', views.CommentView.as_view(), name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:pk>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:pk>/', views.CommentDeleteView.as_view(), name='delete_comment'),

]
