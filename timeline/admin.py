from django.contrib import admin
from django.db import models
from django.contrib.admin.widgets import AdminTextareaWidget
from .models import EventType, Event

# Brand strings in the header
admin.site.site_header = "Lifelog Administration"
admin.site.site_title = "Lifelog Admin"
admin.site.index_title = "Data & Events"
admin.site.site_url = "/"  # "View site" link

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 25

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "type", "id")
    list_filter = ("type",)
    search_fields = ("type__name",)
    date_hierarchy = "timestamp"         # ⟵ handy time drilldown
    ordering = ("-timestamp", "-id")
    list_per_page = 25

    # Make JSON fields readable when editing by hand
    formfield_overrides = {
        models.JSONField: {
            "widget": AdminTextareaWidget(
                attrs={"rows": 10, "class": "vLargeTextField"}
            )
        }
    }

