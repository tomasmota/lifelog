from django.core.management.base import BaseCommand
from timeline.models import EventType

DEFAULTS = [
    {
        "name": "gym",
        "fields": [
            {"name": "duration", "kind": "int", "required": True,  "placeholder": "minutes"},
            {"name": "body_parts", "kind": "string_list", "required": False, "placeholder": "chest, triceps"},
        ],
    },
    {
        "name": "weight",
        "fields": [
            {"name": "kg", "kind": "float", "required": True, "placeholder": "e.g. 58.3"},
        ],
    },
    {
        "name": "calories",
        "fields": [
            {"name": "kcal", "kind": "int", "required": True, "placeholder": "e.g. 2300"},
        ],
    },
]

class Command(BaseCommand):
    help = "Create default EventTypes (gym, weight, calories) if they don't exist"

    def handle(self, *args, **kwargs):
        created = 0
        for spec in DEFAULTS:
            obj, was_created = EventType.objects.get_or_create(
                name=spec["name"],
                defaults={"fields": spec["fields"]},
            )
            if not was_created and not obj.fields:
                obj.fields = spec["fields"]
                obj.save(update_fields=["fields"])
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Done. Created: {created}"))
