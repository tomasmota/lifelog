from django.contrib import admin
from .models import EventType, Event

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "timestamp")
    list_filter = ("type",)
    search_fields = ("type__name",)
