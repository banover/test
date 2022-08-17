from django.urls import path

from . import views
from . import util

entries = util.list_entries()
urlpatterns = [
    path("", views.index, name="index"),
    path("<str:entry>", views.entry, name="entry")
]
