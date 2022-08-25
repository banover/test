from django.urls import path

from . import views
from . import util

#entries = util.list_entries()
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create, name="create"),
    path("update/<str:entry>", views.update, name="update")
]
