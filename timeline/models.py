from __future__ import annotations
import json
from django.db import models
from django.utils import timezone

class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    # fields: list[ {name, kind, required, placeholder} ]
    fields = models.JSONField(default=list, blank=True)

    def __str__(self) -> str:
        return self.name

class Event(models.Model):
    type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events")
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-timestamp", "-id"]

    def __str__(self) -> str:
        return f"{self.type.name} @ {self.timestamp.isoformat()}"

    @property
    def data_json(self) -> str:
        return json.dumps(self.data, ensure_ascii=False)
