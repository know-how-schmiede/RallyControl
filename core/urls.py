from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("classes/", views.RaceClassListView.as_view(), name="raceclass_list"),
    path("classes/new/", views.RaceClassCreateView.as_view(), name="raceclass_create"),
    path("classes/<int:pk>/edit/", views.RaceClassUpdateView.as_view(), name="raceclass_update"),
    path("drivers/", views.DriverListView.as_view(), name="driver_list"),
    path("drivers/new/", views.DriverCreateView.as_view(), name="driver_create"),
    path("drivers/<int:pk>/edit/", views.DriverUpdateView.as_view(), name="driver_update"),
    path("events/", views.EventListView.as_view(), name="event_list"),
    path("events/new/", views.EventCreateView.as_view(), name="event_create"),
    path("events/<int:pk>/edit/", views.EventUpdateView.as_view(), name="event_update"),
    path("stages/", views.StageListView.as_view(), name="stage_list"),
    path("stages/new/", views.StageCreateView.as_view(), name="stage_create"),
    path("stages/<int:pk>/edit/", views.StageUpdateView.as_view(), name="stage_update"),
    path("sessions/", views.SessionListView.as_view(), name="session_list"),
    path("sessions/new/", views.SessionCreateView.as_view(), name="session_create"),
    path("sessions/<int:pk>/edit/", views.SessionUpdateView.as_view(), name="session_update"),
    path("gates/", views.GateListView.as_view(), name="gate_list"),
    path("gates/new/", views.GateCreateView.as_view(), name="gate_create"),
    path("gates/<int:pk>/edit/", views.GateUpdateView.as_view(), name="gate_update"),
    path("vehicles/", views.VehicleListView.as_view(), name="vehicle_list"),
    path("vehicles/new/", views.VehicleCreateView.as_view(), name="vehicle_create"),
    path("vehicles/<int:pk>/edit/", views.VehicleUpdateView.as_view(), name="vehicle_update"),
]
