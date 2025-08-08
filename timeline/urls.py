from django.urls import path
from . import views

app_name = "timeline"

urlpatterns = [
    path("", views.index, name="index"),
    path("fields/", views.fields_partial, name="fields"),
    path("events/create/", views.create_event, name="create_event"),
]
