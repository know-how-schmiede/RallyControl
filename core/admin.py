from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    Capture,
    Driver,
    Event,
    Gate,
    Leaderboard,
    OCRResult,
    Passage,
    RaceClass,
    Run,
    Session,
    Stage,
    User,
    Vehicle,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("RallyControl", {"fields": ("role", "created_at", "updated_at")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(RaceClass)
class RaceClassAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "first_name",
        "last_name",
        "team",
        "race_class",
        "default_start_number",
        "is_active",
    )
    list_filter = ("race_class", "is_active")
    search_fields = ("first_name", "last_name", "display_name", "team")


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "start_date", "end_date", "timezone")
    list_filter = ("timezone",)
    search_fields = ("name", "location")


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ("name", "event", "stage_order", "mode", "is_active")
    list_filter = ("mode", "is_active", "event")
    search_fields = ("name",)
    ordering = ("event", "stage_order")


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("name", "stage", "session_type", "status", "start_time", "end_time")
    list_filter = ("session_type", "status", "stage")
    search_fields = ("name",)


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ("name", "gate_uid", "gate_type", "stage", "is_enabled", "last_seen_at")
    list_filter = ("gate_type", "is_enabled", "stage")
    search_fields = ("name", "gate_uid", "ip_address")


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "driver",
        "race_class",
        "default_start_number",
        "is_active",
    )
    list_filter = ("race_class", "is_active")
    search_fields = ("name", "driver__first_name", "driver__last_name")


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = (
        "driver",
        "session",
        "vehicle",
        "status",
        "start_number_used",
        "final_time_ms",
    )
    list_filter = ("status", "session")
    search_fields = ("driver__first_name", "driver__last_name", "comment")
    autocomplete_fields = ("driver", "session", "vehicle")


@admin.register(Passage)
class PassageAdmin(admin.ModelAdmin):
    list_display = ("session", "gate", "timestamp_ms", "run", "is_valid", "received_at")
    list_filter = ("gate", "session", "is_valid")
    search_fields = ("timestamp_ms",)
    autocomplete_fields = ("run", "session", "gate")


@admin.register(Capture)
class CaptureAdmin(admin.ModelAdmin):
    list_display = ("id", "passage", "image_path", "created_at", "sha256")
    search_fields = ("image_path", "sha256")
    autocomplete_fields = ("passage",)


@admin.register(OCRResult)
class OCRResultAdmin(admin.ModelAdmin):
    list_display = ("capture", "detected_number", "confidence", "engine", "status", "created_at")
    list_filter = ("status", "engine")
    search_fields = ("detected_number", "engine")
    autocomplete_fields = ("capture",)


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("session", "race_class", "generated_at", "checksum")
    list_filter = ("session", "race_class")
    search_fields = ("session__name",)
