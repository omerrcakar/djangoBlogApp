
from django.urls import path
from . import views
from .views import BlogDetailView, CommentCreateView

app_name = "blogs"

urlpatterns = [
    path("",views.blog_list, name="list"),
    path("create/",views.blog_create,name="create"),
    path("<slug:slug>/",views.blog_detail,name="detail"),
    path('<slug:slug>/edit/', views.blog_edit, name='edit'),  # Yeni eklendi
    path('<slug:slug>/delete/', views.blog_delete, name='delete'),  # Yeni eklendi
    path('<slug:slug>/', BlogDetailView.as_view(), name='detail'),
    path('<slug:slug>/comment_create/', CommentCreateView.as_view(), name='comment_create'),

]