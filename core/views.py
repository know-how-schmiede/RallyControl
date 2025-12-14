from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from . import forms
from .models import Driver, Event, Gate, RaceClass, Session, Stage, Vehicle


NAV_ITEMS = [
    {"label": "Dashboard", "url_name": "core:dashboard"},
    {"label": "Fahrer", "url_name": "core:driver_list"},
    {"label": "Fahrzeuge", "url_name": "core:vehicle_list"},
    {"label": "Klassen", "url_name": "core:raceclass_list"},
    {"label": "Events", "url_name": "core:event_list"},
    {"label": "Stages", "url_name": "core:stage_list"},
    {"label": "Sessions", "url_name": "core:session_list"},
    {"label": "Gates", "url_name": "core:gate_list"},
]


class NavContextMixin:
    """Injects navigation for the admin dashboard."""

    page_title: str | None = None

    def get_nav_items(self):
        return NAV_ITEMS

    def get_page_title(self) -> str:
        if self.page_title:
            return self.page_title
        if hasattr(self, "model"):
            return self.model._meta.verbose_name_plural.title()
        return "RallyControl"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["nav_items"] = self.get_nav_items()
        ctx["page_title"] = self.get_page_title()
        return ctx


class DashboardView(NavContextMixin, TemplateView):
    template_name = "core/dashboard.html"
    page_title = "RallyControl Dashboard"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["stats"] = {
            "events": Event.objects.count(),
            "stages": Stage.objects.count(),
            "sessions": Session.objects.count(),
            "drivers": Driver.objects.count(),
            "vehicles": Vehicle.objects.count(),
            "gates": Gate.objects.count(),
        }
        return ctx


class MasterDataListView(NavContextMixin, ListView):
    template_name = "core/generic_list.html"
    list_display: list[str] = []
    page_title: str | None = None
    ordering = []

    def get_list_display(self) -> list[str]:
        return self.list_display or [self.model._meta.pk.name]

    def get_columns(self):
        columns = []
        for field_name in self.get_list_display():
            try:
                field = self.model._meta.get_field(field_name)
                label = field.verbose_name
            except Exception:
                label = field_name.replace("_", " ").title()
            columns.append({"name": field_name, "label": label})
        return columns

    def get_create_url(self) -> str:
        return reverse(f"core:{self.model._meta.model_name}_create")

    def get_edit_url(self, obj) -> str:
        return reverse(f"core:{self.model._meta.model_name}_update", args=[obj.pk])

    def get_rows(self):
        rows = []
        queryset = getattr(self, "object_list", None) or self.get_queryset()
        for obj in queryset:
            values = []
            for field in self.get_list_display():
                value = getattr(obj, field, "")
                if callable(value):
                    try:
                        value = value()
                    except TypeError:
                        value = value
                values.append(value)
            rows.append({"object": obj, "values": values, "edit_url": self.get_edit_url(obj)})
        return rows

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["list_display"] = self.get_list_display()
        ctx["columns"] = self.get_columns()
        ctx["rows"] = self.get_rows()
        ctx["create_url"] = self.get_create_url()
        ctx["model_verbose_name"] = self.model._meta.verbose_name
        ctx["model_verbose_name_plural"] = self.model._meta.verbose_name_plural
        return ctx


class MasterDataCreateView(NavContextMixin, CreateView):
    template_name = "core/generic_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.object} gespeichert.")
        return response

    def get_success_url(self):
        return reverse_lazy(f"core:{self.model._meta.model_name}_list")


class MasterDataUpdateView(NavContextMixin, UpdateView):
    template_name = "core/generic_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"{self.object} aktualisiert.")
        return response

    def get_success_url(self):
        return reverse_lazy(f"core:{self.model._meta.model_name}_list")


class RaceClassListView(MasterDataListView):
    model = RaceClass
    list_display = ["name", "description", "is_active"]
    page_title = "Klassen"


class RaceClassCreateView(MasterDataCreateView):
    model = RaceClass
    form_class = forms.RaceClassForm
    page_title = "Klasse anlegen"


class RaceClassUpdateView(MasterDataUpdateView):
    model = RaceClass
    form_class = forms.RaceClassForm
    page_title = "Klasse bearbeiten"


class DriverListView(MasterDataListView):
    model = Driver
    list_display = ["display_name", "first_name", "last_name", "team", "race_class"]
    page_title = "Fahrer"


class DriverCreateView(MasterDataCreateView):
    model = Driver
    form_class = forms.DriverForm
    page_title = "Fahrer anlegen"


class DriverUpdateView(MasterDataUpdateView):
    model = Driver
    form_class = forms.DriverForm
    page_title = "Fahrer bearbeiten"


class EventListView(MasterDataListView):
    model = Event
    list_display = ["name", "location", "start_date", "end_date"]
    page_title = "Events"


class EventCreateView(MasterDataCreateView):
    model = Event
    form_class = forms.EventForm
    page_title = "Event anlegen"


class EventUpdateView(MasterDataUpdateView):
    model = Event
    form_class = forms.EventForm
    page_title = "Event bearbeiten"


class StageListView(MasterDataListView):
    model = Stage
    list_display = ["event", "name", "stage_order", "mode", "is_active"]
    page_title = "Stages"


class StageCreateView(MasterDataCreateView):
    model = Stage
    form_class = forms.StageForm
    page_title = "Stage anlegen"


class StageUpdateView(MasterDataUpdateView):
    model = Stage
    form_class = forms.StageForm
    page_title = "Stage bearbeiten"


class SessionListView(MasterDataListView):
    model = Session
    list_display = ["stage", "name", "session_type", "status", "start_time"]
    page_title = "Sessions"


class SessionCreateView(MasterDataCreateView):
    model = Session
    form_class = forms.SessionForm
    page_title = "Session anlegen"


class SessionUpdateView(MasterDataUpdateView):
    model = Session
    form_class = forms.SessionForm
    page_title = "Session bearbeiten"


class GateListView(MasterDataListView):
    model = Gate
    list_display = ["name", "gate_uid", "gate_type", "stage", "is_enabled", "last_seen_at"]
    page_title = "Gates"


class GateCreateView(MasterDataCreateView):
    model = Gate
    form_class = forms.GateForm
    page_title = "Gate anlegen"


class GateUpdateView(MasterDataUpdateView):
    model = Gate
    form_class = forms.GateForm
    page_title = "Gate bearbeiten"


class VehicleListView(MasterDataListView):
    model = Vehicle
    list_display = ["driver", "name", "race_class", "default_start_number", "is_active"]
    page_title = "Fahrzeuge"


class VehicleCreateView(MasterDataCreateView):
    model = Vehicle
    form_class = forms.VehicleForm
    page_title = "Fahrzeug anlegen"


class VehicleUpdateView(MasterDataUpdateView):
    model = Vehicle
    form_class = forms.VehicleForm
    page_title = "Fahrzeug bearbeiten"
