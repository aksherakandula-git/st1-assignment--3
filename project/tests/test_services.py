from datetime import datetime

import pytest

from smartcare.data_store import SmartCareDataStore
from smartcare.domain import Appointment, AppointmentStatus
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


def test_find_patient_returns_same_registered_object_and_trims_id():
    _, patients, _, _ = make_services()
    patient = patients.register_patient("P1", "Alex Example")

    result = patients.find_patient("  P1  ")

    assert result is patient


def test_find_patient_is_case_sensitive_and_reports_unknown_id():
    _, patients, _, _ = make_services()
    patients.register_patient("P1", "Alex Example")

    with pytest.raises(LookupError):
        patients.find_patient("p1")


def test_find_patient_rejects_blank_id():
    _, patients, _, _ = make_services()

    with pytest.raises(ValueError):
        patients.find_patient("   ")


def test_find_practitioner_returns_same_registered_object_and_trims_id():
    _, _, practitioners, _ = make_services()
    practitioner = practitioners.register_practitioner(
        "DR1",
        "Dana Example",
        "General Practice",
    )

    result = practitioners.find_practitioner("  DR1  ")

    assert result is practitioner


def test_find_practitioner_is_case_sensitive_and_reports_unknown_id():
    _, _, practitioners, _ = make_services()
    practitioners.register_practitioner(
        "DR1",
        "Dana Example",
        "General Practice",
    )

    with pytest.raises(LookupError):
        practitioners.find_practitioner("dr1")


def test_find_practitioner_rejects_blank_id():
    _, _, practitioners, _ = make_services()

    with pytest.raises(ValueError):
        practitioners.find_practitioner("   ")

        def register_participants(patients, practitioners):
            patient = patients.register_patient("P1", "Alex Example")
            practitioner = practitioners.register_practitioner(
                "DR1",
                "Dana Example",
                "General Practice",
            )
            return patient, practitioner

        def test_cancel_returns_same_object_and_retains_cancelled_history():
            data_store, patients, practitioners, appointments = make_services()
            register_participants(patients, practitioners)

            appointment = appointments.book_appointment(
                "A1",
                "P1",
                "DR1",
                datetime(2026, 10, 1, 9, 0),
            )

            result = appointments.cancel_appointment("  A1  ")

            assert result is appointment
            assert appointment.status is AppointmentStatus.CANCELLED
            assert data_store.find_appointment("A1") is appointment

        def test_repeated_cancellation_is_rejected_without_state_change():
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
            assert data_store.find_appointment("A1") is appointment

        def test_completed_appointment_cannot_be_cancelled_or_mutated():
            data_store, patients, practitioners, appointments = make_services()
            patient, practitioner = register_participants(patients, practitioners)

            appointment = Appointment(
                "A1",
                patient,
                practitioner,
                datetime(2026, 10, 1, 9, 0),
                AppointmentStatus.COMPLETED,
            )

            data_store.add_appointment(appointment)

            with pytest.raises(ValueError):
                appointments.cancel_appointment("A1")

            assert appointment.status is AppointmentStatus.COMPLETED
            assert data_store.find_appointment("A1") is appointment

        def test_cancel_unknown_appointment_reports_absence():
            _, _, _, appointments = make_services()

            with pytest.raises(LookupError):
                appointments.cancel_appointment("A999")

        def test_cancel_rejects_blank_appointment_id():
            _, _, _, appointments = make_services()

            with pytest.raises(ValueError):
                appointments.cancel_appointment("   ")