from datetime import datetime, timezone

import pytest

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)


def make_participants():
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner("DR1", "Dana Example", "General Practice")
    return patient, practitioner


def test_patient_valid_fields_are_trimmed_and_stored():
    patient = Patient("  P1  ", "  Alex Example  ")

    assert patient.patient_id == "P1"
    assert patient.name == "Alex Example"


def test_blank_patient_id_is_rejected():
    with pytest.raises(ValueError):
        Patient("   ", "Alex Example")


def test_blank_patient_name_is_rejected():
    with pytest.raises(ValueError):
        Patient("P1", "   ")


def test_practitioner_valid_fields_are_trimmed_and_stored():
    practitioner = Practitioner(
        "  DR1  ",
        "  Dana Example  ",
        "  General Practice  ",
    )

    assert practitioner.practitioner_id == "DR1"
    assert practitioner.name == "Dana Example"
    assert practitioner.specialty == "General Practice"


def test_blank_practitioner_specialty_is_rejected():
    with pytest.raises(ValueError):
        Practitioner("DR1", "Dana Example", "   ")


def test_new_appointment_starts_scheduled_and_retains_participants():
    patient, practitioner = make_participants()
    date_time = datetime(2026, 10, 1, 9, 0)

    appointment = Appointment("A1", patient, practitioner, date_time)

    assert appointment.appointment_id == "A1"
    assert appointment.patient is patient
    assert appointment.practitioner is practitioner
    assert appointment.date_time == date_time
    assert appointment.status is AppointmentStatus.SCHEDULED


def test_appointment_rejects_invalid_patient_object():
    _, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            "A1",
            "not-a-patient",
            practitioner,
            datetime(2026, 10, 1, 9, 0),
        )


def test_appointment_rejects_invalid_practitioner_object():
    patient, _ = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            "A1",
            patient,
            "not-a-practitioner",
            datetime(2026, 10, 1, 9, 0),
        )


def test_appointment_rejects_non_minute_precision_datetime():
    patient, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            "A1",
            patient,
            practitioner,
            datetime(2026, 10, 1, 9, 0, 1),
        )


def test_appointment_rejects_timezone_aware_datetime():
    patient, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            "A1",
            patient,
            practitioner,
            datetime(2026, 10, 1, 9, 0, tzinfo=timezone.utc),
        )


def test_appointment_rejects_invalid_status():
    patient, practitioner = make_participants()

    with pytest.raises(ValueError):
        Appointment(
            "A1",
            patient,
            practitioner,
            datetime(2026, 10, 1, 9, 0),
            "scheduled",
        )


def test_appointment_cancellation_and_repeat_guard():
    patient, practitioner = make_participants()
    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
    )

    appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.CANCELLED


def test_completed_appointment_cannot_be_cancelled():
    patient, practitioner = make_participants()
    appointment = Appointment(
        "A1",
        patient,
        practitioner,
        datetime(2026, 10, 1, 9, 0),
        AppointmentStatus.COMPLETED,
    )

    with pytest.raises(ValueError):
        appointment.cancel()

    assert appointment.status is AppointmentStatus.COMPLETED