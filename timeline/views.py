from __future__ import annotations
import json
from typing import Any
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from .models import EventType, Event

def index(request: HttpRequest) -> HttpResponse:
    event_types = EventType.objects.all().order_by("name")
    events = Event.objects.select_related("type").all()
    return render(request, "timeline/index.html", {"event_types": event_types, "events": events})

@require_http_methods(["GET"])
def fields_partial(request: HttpRequest) -> HttpResponse:
    et_id = request.GET.get("event_type")
    if not et_id:
        return HttpResponseBadRequest("missing event_type")
    et = get_object_or_404(EventType, pk=et_id)
    return render(request, "timeline/_fields.html", {"et": et})

@require_http_methods(["POST"])
def create_event(request: HttpRequest) -> HttpResponse:
    et_id = request.POST.get("event_type")
    if not et_id:
        return HttpResponseBadRequest("missing event_type")
    et = get_object_or_404(EventType, pk=et_id)

    # Build JSON data based on EventType.fields
    # Field kinds: "string" | "int" | "float" | "string_list"
    errors: list[str] = []
    data: dict[str, Any] = {}

    fields = et.fields or []
    for f in fields:
        name = f.get("name")
        kind = (f.get("kind") or "string").lower()
        required = bool(f.get("required"))
        raw = (request.POST.get(name) or "").strip()

        if required and raw == "":
            errors.append(f"Missing required field: {name}")
            continue
        if raw == "":
            continue

        try:
            if kind == "int":
                data[name] = int(raw)
            elif kind == "float":
                data[name] = float(raw)
            elif kind == "string_list":
                parts = [p.strip() for p in raw.split(",") if p.strip()]
                data[name] = parts
            else:
                data[name] = raw
        except Exception:
            errors.append(f"Invalid value for {name} ({kind})")

    if errors:
        return HttpResponseBadRequest("\n".join(errors))

    Event.objects.create(type=et, data=data)

    # Re-render the events list (HTMX will swap)
    events = Event.objects.select_related("type").all()
    return render(request, "timeline/_events.html", {"events": events})
