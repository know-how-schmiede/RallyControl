from __future__ import annotations

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base class that adds created/updated timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """Custom user to support roles on top of Django auth."""

    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        OPERATOR = "operator", "Operator"
        VIEWER = "viewer", "Viewer"

    email = models.EmailField("email address", unique=True, null=True, blank=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OPERATOR,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.get_full_name() or self.username


class RaceClass(TimeStampedModel):
    """Vehicle / scoring class."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "classes"
        ordering = ["name"]
        verbose_name = "Klasse"
        verbose_name_plural = "Klassen"

    def __str__(self) -> str:
        return self.name


class Driver(TimeStampedModel):
    """Driver entity to which runs are attached."""

    default_start_number = models.IntegerField(blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=150, blank=True, null=True)
    team = models.CharField(max_length=150, blank=True, null=True)
    race_class = models.ForeignKey(
        RaceClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="drivers",
    )
    transponder_id = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return self.display_name or f"{self.first_name} {self.last_name}"


class Event(TimeStampedModel):
    """Event container for a race day."""

    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    timezone = models.CharField(max_length=50, default="Europe/Berlin")
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["-start_date", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.start_date})"


class Stage(TimeStampedModel):
    """Stage within an event."""

    class Mode(models.TextChoices):
        TRAINING = "training", "Training"
        QUALIFYING = "qualifying", "Qualifying"
        RACE = "race", "Race"

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="stages",
    )
    name = models.CharField(max_length=150)
    stage_order = models.PositiveIntegerField(default=1)
    mode = models.CharField(max_length=20, choices=Mode.choices, default=Mode.TRAINING)
    distance_m = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["event", "stage_order"]
        unique_together = ("event", "name")

    def __str__(self) -> str:
        return f"{self.event.name} - {self.name}"


class Session(TimeStampedModel):
    """Timed session or heat within a stage."""

    class SessionType(models.TextChoices):
        TIMED_RUN = "timed_run", "Timed Run"
        MULTI_LAP = "multi_lap", "Multi Lap"
        OPEN_PRACTICE = "open_practice", "Open Practice"

    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        RUNNING = "running", "Running"
        FINISHED = "finished", "Finished"
        ARCHIVED = "archived", "Archived"

    stage = models.ForeignKey(
        Stage,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    name = models.CharField(max_length=150)
    session_type = models.CharField(
        max_length=20, choices=SessionType.choices, default=SessionType.TIMED_RUN
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PLANNED
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ["stage", "start_time", "name"]
        unique_together = ("stage", "name")

    def __str__(self) -> str:
        return f"{self.stage} – {self.name}"


class Gate(TimeStampedModel):
    """Hardware gate for timing (start/finish/checkpoint)."""

    class GateType(models.TextChoices):
        START = "start", "Start"
        FINISH = "finish", "Finish"
        CHECKPOINT = "checkpoint", "Checkpoint"

    gate_uid = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    gate_type = models.CharField(
        max_length=20, choices=GateType.choices, default=GateType.START
    )
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="gates",
    )
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    location_hint = models.CharField(max_length=200, blank=True, null=True)
    is_enabled = models.BooleanField(default=True)
    last_seen_at = models.DateTimeField(blank=True, null=True)
    fw_version = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.gate_uid})"


class Vehicle(TimeStampedModel):
    """Optional vehicles per driver."""

    driver = models.ForeignKey(
        Driver, on_delete=models.CASCADE, related_name="vehicles"
    )
    race_class = models.ForeignKey(
        RaceClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="vehicles",
    )
    name = models.CharField(max_length=150)
    default_start_number = models.IntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["driver", "name"]

    def __str__(self) -> str:
        return f"{self.driver} – {self.name}"


class Run(TimeStampedModel):
    """A single timed run of a driver."""

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        FINISHED = "finished", "Finished"
        DNF = "dnf", "Did Not Finish"
        DSQ = "dsq", "Disqualified"
        VOID = "void", "Void"

    class StartNumberSource(models.TextChoices):
        DRIVER_DEFAULT = "driver_default", "Driver Default"
        VEHICLE_DEFAULT = "vehicle_default", "Vehicle Default"
        MANUAL_OVERRIDE = "manual_override", "Manual Override"
        OCR_DETECTED = "ocr_detected", "OCR Detected"

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="runs",
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name="runs",
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="runs",
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.QUEUED
    )
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    total_time_ms = models.BigIntegerField(blank=True, null=True)
    penalty_ms = models.PositiveIntegerField(default=0)
    final_time_ms = models.BigIntegerField(blank=True, null=True)
    start_number_used = models.IntegerField(blank=True, null=True)
    start_number_source = models.CharField(
        max_length=20,
        choices=StartNumberSource.choices,
        default=StartNumberSource.DRIVER_DEFAULT,
    )
    comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["session", "driver"]
        indexes = [
            models.Index(fields=["session"]),
            models.Index(fields=["driver"]),
        ]

    def __str__(self) -> str:
        return f"{self.driver} @ {self.session}"


class Passage(TimeStampedModel):
    """Gate event with source timestamp."""

    run = models.ForeignKey(
        Run,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="passages",
    )
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="passages",
    )
    gate = models.ForeignKey(
        Gate,
        on_delete=models.CASCADE,
        related_name="passages",
    )
    timestamp_ms = models.BigIntegerField()
    received_at = models.DateTimeField(default=timezone.now)
    direction = models.CharField(max_length=20, blank=True, null=True)
    signal_quality = models.CharField(max_length=50, blank=True, null=True)
    raw_payload = models.TextField(blank=True, null=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        ordering = ["timestamp_ms"]
        indexes = [
            models.Index(fields=["session"]),
            models.Index(fields=["gate"]),
            models.Index(fields=["timestamp_ms"]),
        ]

    def __str__(self) -> str:
        return f"{self.gate} @ {self.timestamp_ms}"


class Capture(models.Model):
    """Captured image from RaspiCam."""

    passage = models.ForeignKey(
        Passage,
        on_delete=models.CASCADE,
        related_name="captures",
    )
    image_path = models.CharField(max_length=255)
    captured_at_ms = models.BigIntegerField(blank=True, null=True)
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    sha256 = models.CharField(max_length=64, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Capture {self.pk} for {self.passage}"


class OCRResult(models.Model):
    """OCR detection for a capture."""

    class Status(models.TextChoices):
        OK = "ok", "OK"
        LOW_CONFIDENCE = "low_confidence", "Low Confidence"
        FAILED = "failed", "Failed"

    capture = models.ForeignKey(
        Capture,
        on_delete=models.CASCADE,
        related_name="ocr_results",
    )
    detected_number = models.IntegerField(blank=True, null=True)
    confidence = models.FloatField()
    engine = models.CharField(max_length=50)
    processing_ms = models.PositiveIntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.OK
    )
    raw_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        number = self.detected_number or "?"
        return f"OCR {number} ({self.engine})"


class Leaderboard(models.Model):
    """Cached leaderboard JSON payload for fast kiosk rendering."""

    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="leaderboards",
    )
    race_class = models.ForeignKey(
        RaceClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leaderboards",
    )
    generated_at = models.DateTimeField(auto_now_add=True)
    data_json = models.JSONField()
    checksum = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        ordering = ["-generated_at"]
        unique_together = ("session", "race_class", "generated_at")

    def __str__(self) -> str:
        return f"Leaderboard for {self.session}"
