
# SmartCare — Assignment 3

**Requirements baseline:** SmartCare A3 2026, revision 2.

## Running SmartCare

From the `project` directory, run the demonstration:

```bash
python main.py
```

To launch the interactive SmartCare menu:

```bash
python main.py --interactive
```

To run the automated tests:

```bash
python -m pytest -q
```

The application uses Python and the standard library at runtime. Pytest is required for running the tests. If needed, install the development dependencies using:

```bash
python -m pip install -r requirements-dev.txt
```

## Stage 9 features

The application supports:

- Patient registration and lookup.
- Practitioner registration and lookup.
- Appointment booking and lookup.
- Appointment cancellation.
- Practitioner appointment listings.
- Optional filtering by appointment status.
- Appointment sorting by date and appointment ID.
- Practitioner booking conflict checking.
- Input validation and error recovery in the interactive menu.

Appointment listings return a new list, ordered by appointment date and time, then appointment ID. By default, listings include all appointment statuses. Users can also filter by scheduled, cancelled or completed status.

## Data storage and limitations

SmartCare uses three in-memory collections for patients, practitioners and appointments. All records are session-only and are lost when the application exits. No database, file-based or other persistent storage is implemented.

Use synthetic information only.

The application does not implement appointment rescheduling or additional assurance features. No age, appointment-duration, patient-conflict or past-date restrictions are applied unless specified by the existing requirements.

## Validation and testing

The automated test suite covers domain behaviour, services, regression checks, query functions and practitioner appointment listing workflows.

The interactive menu was also manually tested for successful registration, booking, cancellation, listing, status filtering, invalid input handling and recovery from errors.