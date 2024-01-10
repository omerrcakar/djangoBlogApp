from django.urls import path
from . import views
from .views import UserProfileView

app_name = "accounts"

urlpatterns = [
    path("signup/",views.signup_view, name="signup"),
    path("login/",views.login_view, name="login"),
    path("logout/",views.logout_view, name="logout"),
    path('user_profile/', UserProfileView.as_view(), name='user_profile'),

]