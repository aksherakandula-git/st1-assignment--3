from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import AppointmentStatus
from smartcare.services import (
    AppointmentService,
    PatientService,
    PractitionerService,
)


def make_services():
    data_store = SmartCareDataStore()
    patients = PatientService(data_store)
    practitioners = PractitionerService(data_store)
    appointments = AppointmentService(data_store)
    return data_store, patients, practitioners, appointments


def register_participants(patients, practitioners):
    patients.register_patient("P1", "Alex Example")
    practitioners.register_practitioner(
        "DR1",
        "Dana Example",
        "General Practice",
    )
    practitioners.register_practitioner(
        "DR2",
        "Morgan Example",
        "General Practice",
    )


def test_f8_01_same_practitioner_cannot_have_two_scheduled_appointments():
    data_store, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    when = datetime(2026, 10, 1, 9, 0)

    first = appointments.book_appointment(
        "A1", "P1", "DR1", when
    )

    with pytest.raises(ValueError):
        appointments.book_appointment(
            "A2", "P1", "DR1", when
        )

    assert data_store.list_appointments() == [first]

    # A different practitioner can still book the same time.
    second = appointments.book_appointment(
        "A3", "P1", "DR2", when
    )

    assert second.status is AppointmentStatus.SCHEDULED
    assert data_store.list_appointments() == [first, second]


def test_f8_02_cancelled_appointment_remains_available_in_store():
    data_store, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    appointment = appointments.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    result = appointments.cancel_appointment("A1")

    assert result is appointment
    assert appointment.status is AppointmentStatus.CANCELLED
    assert data_store.find_appointment("A1") is appointment
    assert appointment in data_store.list_appointments()


def test_f8_02_repeated_cancellation_is_rejected_without_state_change():
    data_store, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    appointment = appointments.book_appointment(
        "A1",
        "P1",
        "DR1",
        datetime(2026, 10, 1, 9, 0),
    )

    appointments.cancel_appointment("A1")

    with pytest.raises(ValueError):
        appointments.cancel_appointment("A1")

    assert appointment.status is AppointmentStatus.CANCELLED
    assert appointment in data_store.list_appointments()