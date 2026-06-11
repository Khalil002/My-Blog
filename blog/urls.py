from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/<int:post_id>/", views.detail, name="detail"),
    path("archives/", views.archive_index, name="archive_index"),
    path("<int:year>/", views.archive_year, name="archive_year"),
    path("<int:year>/<int:month>/", views.archive_month, name="archive_month"),
    path("<int:year>/<int:month>/<int:day>/", views.archive_day, name="archive_day"),
]
