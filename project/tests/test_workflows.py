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
        "Jordan Example",
        "Cardiology",
    )


def test_list_practitioner_appointments_returns_sorted_results():
    _, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    later = appointments.book_appointment(
        "A2", "P1", "DR1", datetime(2026, 10, 2, 10, 0)
    )
    earlier = appointments.book_appointment(
        "A1", "P1", "DR1", datetime(2026, 10, 1, 9, 0)
    )

    result = appointments.list_practitioner_appointments("DR1")

    assert result == [earlier, later]


def test_list_practitioner_appointments_includes_all_statuses():
    _, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    first = appointments.book_appointment(
        "A1", "P1", "DR1", datetime(2026, 10, 1, 9, 0)
    )
    second = appointments.book_appointment(
        "A2", "P1", "DR1", datetime(2026, 10, 2, 9, 0)
    )
    appointments.cancel_appointment("A1")

    result = appointments.list_practitioner_appointments("DR1")

    assert result == [first, second]
    assert first.status is AppointmentStatus.CANCELLED


def test_list_practitioner_appointments_filters_status():
    _, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    first = appointments.book_appointment(
        "A1", "P1", "DR1", datetime(2026, 10, 1, 9, 0)
    )
    appointments.book_appointment(
        "A2", "P1", "DR1", datetime(2026, 10, 2, 9, 0)
    )
    appointments.cancel_appointment("A1")

    result = appointments.list_practitioner_appointments(
        "DR1",
        AppointmentStatus.SCHEDULED,
    )

    assert len(result) == 1
    assert result[0].appointment_id == "A2"
    assert first.status is AppointmentStatus.CANCELLED


def test_list_practitioner_appointments_isolated_by_practitioner():
    _, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    first = appointments.book_appointment(
        "A1", "P1", "DR1", datetime(2026, 10, 1, 9, 0)
    )
    appointments.book_appointment(
        "A2", "P1", "DR2", datetime(2026, 10, 1, 9, 0)
    )

    result = appointments.list_practitioner_appointments("DR1")

    assert result == [first]


def test_known_practitioner_without_appointments_returns_empty_list():
    _, _, practitioners, appointments = make_services()
    practitioners.register_practitioner(
        "DR1",
        "Dana Example",
        "General Practice",
    )

    result = appointments.list_practitioner_appointments("DR1")

    assert result == []


def test_unknown_practitioner_raises_lookup_error():
    _, _, _, appointments = make_services()

    with pytest.raises(LookupError):
        appointments.list_practitioner_appointments("DR999")


def test_blank_practitioner_id_raises_value_error():
    _, _, _, appointments = make_services()

    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments("   ")


def test_invalid_status_raises_value_error():
    _, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    with pytest.raises(ValueError):
        appointments.list_practitioner_appointments(
            "DR1",
            "scheduled",
        )


def test_listing_returns_a_new_list_without_changing_store():
    data_store, patients, practitioners, appointments = make_services()
    register_participants(patients, practitioners)

    first = appointments.book_appointment(
        "A1", "P1", "DR1", datetime(2026, 10, 1, 9, 0)
    )
    second = appointments.book_appointment(
        "A2", "P1", "DR1", datetime(2026, 10, 2, 9, 0)
    )

    original_store_list = data_store.list_appointments()
    result = appointments.list_practitioner_appointments("DR1")

    assert result == [first, second]
    assert result is not original_store_list
    assert data_store.list_appointments() == original_store_list