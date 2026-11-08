from datetime import datetime

from smartcare.domain import (
    Appointment,
    AppointmentStatus,
    Patient,
    Practitioner,
)
from smartcare.queries import (
    appointment_sort_key,
    select_appointments,
)


def make_appointment(
    appointment_id,
    practitioner_id="DR1",
    date_time=None,
    status=AppointmentStatus.SCHEDULED,
):
    patient = Patient("P1", "Alex Example")
    practitioner = Practitioner(
        practitioner_id,
        "Dana Example",
        "General Practice",
    )

    if date_time is None:
        date_time = datetime(2026, 10, 1, 9, 0)

    return Appointment(
        appointment_id,
        patient,
        practitioner,
        date_time,
        status,
    )


def test_appointment_sort_key_returns_datetime_and_id():
    appointment = make_appointment("A1")
    assert appointment_sort_key(appointment) == (
        datetime(2026, 10, 1, 9, 0),
        "A1",
    )


def test_select_appointments_filters_by_practitioner():
    first = make_appointment("A1", "DR1")
    second = make_appointment("A2", "DR2")

    result = select_appointments([first, second], "DR1")

    assert result == [first]


def test_select_appointments_includes_all_statuses_by_default():
    scheduled = make_appointment("A1")
    cancelled = make_appointment(
        "A2",
        status=AppointmentStatus.CANCELLED,
    )
    completed = make_appointment(
        "A3",
        status=AppointmentStatus.COMPLETED,
    )

    result = select_appointments(
        [scheduled, cancelled, completed],
        "DR1",
    )

    assert result == [scheduled, cancelled, completed]


def test_select_appointments_filters_by_status():
    scheduled = make_appointment("A1")
    cancelled = make_appointment(
        "A2",
        status=AppointmentStatus.CANCELLED,
    )

    result = select_appointments(
        [scheduled, cancelled],
        "DR1",
        AppointmentStatus.CANCELLED,
    )

    assert result == [cancelled]


def test_select_appointments_sorts_by_datetime_then_id():
    later = make_appointment(
        "A1",
        date_time=datetime(2026, 10, 2, 9, 0),
    )
    same_time_z = make_appointment("Z1")
    same_time_a = make_appointment("A2")

    result = select_appointments(
        [later, same_time_z, same_time_a],
        "DR1",
    )

    assert result == [same_time_a, same_time_z, later]


def test_select_appointments_does_not_mutate_source_list():
    later = make_appointment(
        "A2",
        date_time=datetime(2026, 10, 2, 9, 0),
    )
    earlier = make_appointment("A1")
    source = [later, earlier]
    original = source.copy()

    result = select_appointments(source, "DR1")

    assert source == original
    assert result == [earlier, later]
    assert result is not source


def test_select_appointments_returns_new_empty_list():
    source = []
    result = select_appointments(source, "DR1")

    assert result == []
    assert result is not source


def test_select_appointments_rejects_invalid_status():
    appointment = make_appointment("A1")

    try:
        select_appointments([appointment], "DR1", "scheduled")
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid status should raise ValueError")