from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("post/new/", views.new_post, name="new_post"),
    path("post/<int:post_id>/", views.detail, name="detail"),
    path("archives/", views.archive_index, name="archive_index"),
    path("<int:year>/", views.archive_year, name="archive_year"),
    path("<int:year>/<int:month>/", views.archive_month, name="archive_month"),
    path("<int:year>/<int:month>/<int:day>/", views.archive_day, name="archive_day"),
]
