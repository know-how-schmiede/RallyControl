from django import forms

from .models import Driver, Event, Gate, RaceClass, Session, Stage, Vehicle


class RaceClassForm(forms.ModelForm):
    class Meta:
        model = RaceClass
        fields = ["name", "description", "is_active"]


class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            "first_name",
            "last_name",
            "display_name",
            "team",
            "race_class",
            "default_start_number",
            "transponder_id",
            "is_active",
            "notes",
        ]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "location",
            "start_date",
            "end_date",
            "timezone",
            "notes",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }


class StageForm(forms.ModelForm):
    class Meta:
        model = Stage
        fields = [
            "event",
            "name",
            "stage_order",
            "mode",
            "distance_m",
            "is_active",
        ]


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = [
            "stage",
            "name",
            "session_type",
            "status",
            "start_time",
            "end_time",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class GateForm(forms.ModelForm):
    class Meta:
        model = Gate
        fields = [
            "gate_uid",
            "name",
            "gate_type",
            "stage",
            "ip_address",
            "location_hint",
            "is_enabled",
            "last_seen_at",
            "fw_version",
            "notes",
        ]
        widgets = {
            "last_seen_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "driver",
            "race_class",
            "name",
            "default_start_number",
            "notes",
            "is_active",
        ]
