from __future__ import annotations
import json
from typing import Any
from django.shortcuts import get_object_or_404, render
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime

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

    # Optional timestamp
    raw_ts = (request.POST.get("timestamp") or "").strip()
    when = None
    if raw_ts:
        parsed = parse_datetime(raw_ts)
        if parsed is None:
            try:
                parsed = timezone.datetime.fromisoformat(raw_ts)  # e.g. "2025-08-08T12:34"
            except Exception:
                parsed = None
        if parsed is not None:
            if timezone.is_naive(parsed):
                parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
            when = parsed

    errors: list[str] = []
    if raw_ts and when is None:
        errors.append("Invalid value for timestamp (datetime-local)")

    # Build JSON data based on EventType.fields
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
        events = Event.objects.select_related("type").all()
        resp = render(
            request,
            "timeline/create_response.html",
            {"events": events, "ok": False, "errors": errors, "et": et},
        )
        resp.status_code = 400
        return resp

    Event.objects.create(type=et, data=data, timestamp=when or timezone.now())

    events = Event.objects.select_related("type").all()
    resp = render(
        request,
        "timeline/create_response.html",
        {"events": events, "ok": True, "errors": [], "et": et},
    )
    resp["HX-Trigger"] = json.dumps({"event-added": {"type": et.name}})
    return resp

