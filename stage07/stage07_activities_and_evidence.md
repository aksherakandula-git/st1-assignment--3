# Stage 7 Testing and Verification Record

Group/tutorial: 4483 Software Technology 1 – Online Group 3, Tuesday 5:30–7:30 pm
Members/cohorts: Akshera Kandula – aksherakandula-git – UG; Harleen Partola – Harleenpartola – UG
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.


All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement | Positive test | Negative test | Key assertion |
|---|---|---|---|
| FR-01 Register patient | Register a patient using valid required data and an unused patient ID, then confirm the registered patient is stored in the shared session store. | Attempt to register another patient using an already registered patient ID and expect `ValueError`, while confirming the original patient remains stored. | `assert data_store.find_patient("P1") is patient` and, after the rejected duplicate, confirm the stored object is still the original patient. |
| FR-05 Prevent practitioner conflict | Book appointments for two different practitioners at the same exact datetime and confirm both bookings are allowed. | Attempt to book a second `SCHEDULED` appointment for the same practitioner at the same exact datetime and expect `ValueError`. | Confirm the permitted appointment is stored; for the conflict case use `pytest.raises(ValueError)` and confirm the rejected appointment was not stored. |
| FR-06 Cancel appointment | Cancel a stored `SCHEDULED` appointment and confirm the same appointment object changes to `CANCELLED`. | Attempt to cancel an already `CANCELLED` or `COMPLETED` appointment and expect `ValueError` without changing its existing state. | `assert result is appointment` and `assert appointment.status is AppointmentStatus.CANCELLED`; after a rejected transition, assert the previous status is unchanged. |
| FR-07 Retain cancelled history | Cancel a `SCHEDULED` appointment and then retrieve it again from the store during the same session. | Attempt a repeated cancellation, expect `ValueError`, and confirm the cancelled appointment is still retained and retrievable. | `assert data_store.find_appointment("A1") is appointment` and `assert appointment.status is AppointmentStatus.CANCELLED`. |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`

Judgement: Weak/unclear

Reason: This only proves that execution reached the assertion. It does not check any required SmartCare behaviour, result, state or error.

`assert appointment is not None`

Judgement: Weak/unclear

Reason: This only proves that an appointment exists. It does not prove that it is the correct appointment, the same stored object or in the required state.

`assert appointment.status == AppointmentStatus.CANCELLED`

Judgement: Strong for stated behaviour

Reason: This directly verifies that cancellation changed the appointment to the required `CANCELLED` state. It does not by itself prove retained history or object identity.

`assert len(results) > 0`

Judgement: Weak/unclear

Reason: This only proves that the collection contains at least one item. It does not prove that the correct records are present or that filtering and ordering are correct.

`assert data_store.find_appointment('A1') is appointment`

Judgement: Strong for stated behaviour

Reason: This verifies that appointment `A1` remains retrievable and that the retrieved reference is the same stored appointment object.

### Activity 3 Boundary thinking

| Boundary or edge case | Input / starting state | Expected result | Contract supporting the expectation |
|---|---|---|---|
| Blank identifier | Use a blank patient, practitioner or appointment ID such as `""`. | The operation raises `ValueError` and no existing stored state is changed. | Required identifiers must be non-blank text. Invalid or blank IDs raise `ValueError`. |
| Whitespace-only required name | Attempt to register a patient or practitioner with a required name such as `"   "`. | Registration raises `ValueError` and the object is not stored. | Required text is trimmed and must contain non-blank content. |
| Same-time practitioner booking | A `SCHEDULED` appointment already exists for practitioner `DR1` at a specific datetime, then another appointment is requested for `DR1` at exactly the same datetime. | The second booking raises `ValueError` and is not stored. | FR-05 defines a conflict as the same practitioner at the exact same datetime while an existing appointment is `SCHEDULED`. |
| Same time with a different practitioner | An appointment exists for `DR1` at a specific datetime, then another appointment is booked for `DR2` at the same datetime. | The second booking succeeds. | FR-05 permits different practitioners to have appointments at the same time. |
| Cancelled appointment and practitioner slot | An appointment for `DR1` is cancelled, then a new appointment is requested for `DR1` at the same datetime. | The new booking is allowed because the cancelled appointment no longer creates a `SCHEDULED` conflict. | The conflict rule applies to an existing `SCHEDULED` appointment; a `CANCELLED` appointment does not occupy the slot. |
| Repeated cancellation | An appointment is already `CANCELLED`, then cancellation is requested again. | `ValueError` is raised and the appointment remains `CANCELLED` and retained in the store. | FR-06 permits cancellation only from `SCHEDULED`; FR-07 requires cancelled history to remain retrievable. |
| Invalid status transition from COMPLETED | An appointment is in `COMPLETED` state and cancellation is requested. | `ValueError` is raised and the status remains `COMPLETED`. | The domain cancellation transition only permits `SCHEDULED` to become `CANCELLED`; illegal transitions must not mutate state. |

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.

| Candidate | Diagnosis | Revised test intention |
|---|---|---|
| Test 1 — only checks `object is not None` | Weak assertion. It only proves that some object exists and does not verify the specific required result, identity, state or error behaviour. | Replace the existence check with an assertion tied to the requirement, such as checking that the returned object is the same registered object using `is`, or checking the exact required state/value. |
| Test 2 — only checks `object is not None` | Weak assertion for the same reason. A wrong object or object in the wrong state could still satisfy the test. | Assert the exact required observable behaviour, for example `assert result is expected_object`, exact status, exact stored value, or the documented exception. |
| Test 3 — uses `assert True` | This does not verify any SmartCare behaviour. The test will pass regardless of whether the implementation is correct. | Replace it with an assertion that checks the actual requirement, such as a state transition, object identity, exact stored result, specific exception or preserved state after rejection. |
| Test 4 — assumes an SMS notification exists | Invalid test because SMS notification behaviour is not part of the current SmartCare requirements. The test invents functionality and could incorrectly fail a correct implementation. | Remove the SMS assumption and test only published behaviour, such as successful registration, booking, lookup, cancellation, conflict handling or retained history. |
| Test 5 — assumes an SMS notification exists | Invalid requirement assumption. A passing or failing SMS test would not provide evidence for the approved SmartCare baseline. | Replace it with a requirement-linked case using observable public behaviour and the current SmartCare contracts, without introducing notification functionality. |

The main issue with the generated tests is that passing tests do not automatically provide useful verification evidence. Each test must trace to a real requirement, use meaningful assertions, avoid invented behaviour and be capable of failing when the required behaviour is broken.

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?
100% code coverage only shows that every line of code was executed during testing. It does not prove that the tests checked the correct requirements, used meaningful assertions, covered important input combinations or detected incorrect behaviour. A test can execute every line while still using weak assertions such as `assert True` or checking the wrong expected result. Therefore, high coverage can coexist with poor verification if the tests do not actually prove the required behaviour.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement | Acceptance criterion | Test ID | Test type | Test name / location | Expected behaviour | Result / observed status | Supplied or student-authored |
|---|---|---|---|---|---|---|---|
| FR-01 Register patient | AC-01.1 | TEST-S7-01 | Service positive | `tests/test_services.py::test_register_patient_stores_same_object` | Valid required patient data with an unused ID is registered and the same patient object is stored. | Planned — not yet implemented/run | Student-authored Stage 7 |
| FR-01 Register patient | AC-01.2 | TEST-S7-02 | Service negative | `tests/test_services.py::test_duplicate_patient_preserves_original_stage7` | Registration with an existing patient ID raises `ValueError` and the original stored patient remains unchanged. | Planned — not yet implemented/run | Student-authored Stage 7 |
| FR-01 Register patient | Revision 2 required-field validation contract | TEST-S7-03 | Domain boundary | `tests/test_domain.py::test_blank_patient_id_is_rejected` | A blank or whitespace-only patient ID raises `ValueError`. | Planned — not yet implemented/run | Student-authored Stage 7 |
| FR-02 Patient Search | AC-02.1 | TEST-S7-04 | Service positive | `tests/test_services.py::test_find_patient_returns_same_registered_object_and_trims_id` | A known patient ID returns the actual registered patient object. | Passed in Stage 7 baseline | Student-authored Stage 6 retained as regression evidence |
| FR-02 Patient Search | AC-02.2 | TEST-S7-05 | Service negative | `tests/test_services.py::test_find_patient_unknown_id_reports_absence` | A valid but unknown patient ID raises `LookupError`. | Planned — not yet implemented/run | Student-authored Stage 7 |
| FR-04 Book appointment | AC-03.1 | TEST-S7-06 | Service positive | `tests/test_starter.py::test_registration_and_booking` | Registered participants, a unique appointment ID and a free time produce a stored `SCHEDULED` appointment. | Passed in Stage 7 baseline | Supplied |
| FR-04 Book appointment | AC-03.2 | TEST-S7-07 | Service negative | `tests/test_starter.py::test_unregistered_participants_rejected` | Booking with an unknown patient or practitioner is rejected. | Passed in Stage 7 baseline | Supplied |
| FR-05 Prevent practitioner conflict | AC-04.1 / AC-04.2 | TEST-S7-08 | Service negative/positive | `tests/test_starter.py::test_conflict_rule_and_different_practitioner` | Same practitioner, exact time and `SCHEDULED` status conflicts; a different practitioner at the same time is allowed. | Passed in Stage 7 baseline | Supplied |
| FR-06 Cancel appointment | AC-05.1 | TEST-S7-09 | Service positive | `tests/test_services.py::test_cancel_returns_same_object_and_retains_cancelled_history` | Cancelling a `SCHEDULED` appointment returns the same object and changes its status to `CANCELLED`. | Passed in Stage 7 baseline | Student-authored Stage 6 retained as regression evidence |
| FR-07 Retain cancelled history | AC-05.2 | TEST-S7-10 | Service positive | `tests/test_services.py::test_cancel_returns_same_object_and_retains_cancelled_history` | A cancelled appointment remains retrievable as the same stored object during the current session. | Passed in Stage 7 baseline | Student-authored Stage 6 retained as regression evidence |
| FR-06 Cancel appointment | AC-05.3 | TEST-S7-11 | Service negative | `tests/test_services.py::test_repeated_cancellation_is_rejected_without_state_change` | Repeated cancellation raises `ValueError` and the appointment remains `CANCELLED` and retained. | Passed in Stage 7 baseline | Student-authored Stage 6 retained as regression evidence |
| FR-06 Cancel appointment | Domain cancellation guard supporting AC-05.1/AC-05.3 | TEST-S7-12 | Domain positive/negative | `tests/test_domain.py::test_appointment_cancellation_and_repeat_guard` | A new appointment begins `SCHEDULED`, cancellation changes it to `CANCELLED`, and a repeated cancellation raises `ValueError`. | Planned — not yet implemented/run | Student-authored Stage 7 |
| FR-08 Appointment lookup | AC-06.1 | TEST-S7-13 | Service positive | `tests/test_services.py::test_known_appointment_lookup_returns_same_object` | A known appointment ID returns the same stored appointment object. | Planned — not yet implemented/run | Student-authored Stage 7 |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention | Observable result expected | Added evidence beyond supplied tests |
|---|---|---|---|---|---|---|
| TEST-S7-01 | FR-01 Register patient | AC-01.1 | Positive | Register a patient with valid required data and an unused ID through `PatientService`. | The returned patient is the same object stored and retrievable from the shared `SmartCareDataStore`. | Provides explicit service-level evidence that valid registration results in storage, rather than only successful object construction. |
| TEST-S7-02 | FR-01 Register patient | AC-01.2 | Negative | Attempt to register a second patient using an existing patient ID. | `ValueError` is raised and the original stored patient remains unchanged and retrievable. | Confirms duplicate rejection also preserves the original registered object. |
| TEST-S7-03 | FR-01 Register patient | Revision 2 required-field validation contract | Boundary | Construct a patient using a blank or whitespace-only patient ID. | `ValueError` is raised. | Adds explicit domain-level evidence for the non-blank ID validation boundary. |
| TEST-S7-04 | FR-02 Patient Search | AC-02.1 | Positive | Look up a registered patient using its ID, including surrounding whitespace. | The actual registered patient object is returned. | Confirms trimming and object identity through the completed Stage 6 lookup service. |
| TEST-S7-05 | FR-02 Patient Search | AC-02.2 | Negative | Look up a valid but unknown patient ID. | `LookupError` is raised and existing store state is unchanged. | Explicitly verifies the service-level distinction between invalid input and a valid-but-absent ID. |
| TEST-S7-06 | FR-04 Book appointment | AC-03.1 | Positive | Book an appointment using registered participants, a unique appointment ID and an available exact time. | A stored appointment is returned with `SCHEDULED` status and references to the registered patient and practitioner. | Confirms the complete service workflow and object identity, not only appointment construction. |
| TEST-S7-07 | FR-04 Book appointment | AC-03.2 | Negative | Attempt to book using an unknown patient or practitioner. | `LookupError` is raised and no appointment is stored. | Verifies rejected booking does not create partial stored state. |
| TEST-S7-08 | FR-05 Prevent practitioner conflict | AC-04.1 / AC-04.2 | Boundary | Attempt a second `SCHEDULED` appointment for the same practitioner at the exact same datetime, and compare with a different practitioner at that time. | Same practitioner/time raises `ValueError`; a different practitioner at the same time is allowed. | Tests the exact boundary of the conflict rule rather than inventing patient or duration conflicts. |
| TEST-S7-09 | FR-06 Cancel appointment | AC-05.1 | Positive | Cancel a stored `SCHEDULED` appointment through `AppointmentService`. | The same appointment object is returned and its status becomes `CANCELLED`. | Verifies service coordination and domain state transition together. |
| TEST-S7-10 | FR-07 Retain cancelled history | AC-05.2 | Positive | Retrieve an appointment after successful cancellation. | The same cancelled appointment remains retrievable from the store during the session. | Explicitly proves retained history and object identity after cancellation. |
| TEST-S7-11 | FR-06 Cancel appointment | AC-05.3 | Negative | Attempt to cancel an already `CANCELLED` appointment. | `ValueError` is raised; status remains `CANCELLED` and the appointment remains stored. | Verifies rejected repeated cancellation does not mutate or delete history. |
| TEST-S7-12 | FR-06 Cancel appointment | Domain cancellation guard | Negative / Boundary | Attempt to cancel an appointment constructed in `COMPLETED` state. | `ValueError` is raised and status remains `COMPLETED`. | Adds explicit evidence for another illegal status transition and state preservation. |
| TEST-S7-13 | FR-08 Appointment lookup | AC-06.1 | Positive | Look up a known stored appointment by ID. | The same stored appointment object is returned. | Adds an explicit identity assertion for appointment lookup. |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID | Arrange | Act | Assert | Why meaningful / why assertion proves criterion |
|--|---|---|---|---|
| TEST-S7-01 | Create a fresh `SmartCareDataStore` and `PatientService`. Use valid synthetic patient data with an unused ID. | Call `register_patient("P1", "Alex Example")`. | Assert the returned patient is the same object returned by `data_store.find_patient("P1")`. | This proves valid registration stores the actual registered patient object, which directly supports AC-01.1. |
| TEST-S7-02 | Create a fresh store and register patient `P1`. Keep a reference to the original patient. | Attempt to register another patient using ID `P1`. | Use `pytest.raises(ValueError)` and then assert `data_store.find_patient("P1") is original_patient`. | This proves duplicate registration is rejected and that the original stored patient is not overwritten, supporting AC-01.2. |
| TEST-S7-03 | Prepare a Patient construction using a whitespace-only ID. | Construct `Patient("   ", "Alex Example")`. | Use `pytest.raises(ValueError)`. | This checks the exact non-blank identifier boundary defined by the revision 2 validation contract. |
| TEST-S7-04 | Create a fresh store and register patient `P1`. | Call `patients.find_patient("  P1  ")`. | Assert `result is patient`. | This proves surrounding whitespace is trimmed and the service returns the actual registered object, supporting AC-02.1. |
| TEST-S7-05 | Create a fresh store containing no patient with ID `P999`. | Call `patients.find_patient("P999")`. | Use `pytest.raises(LookupError)`. | This proves a valid but unknown ID reports absence through the service contract, supporting AC-02.2. |
| TEST-S7-06 | Create fresh shared services, register real patient and practitioner objects, and choose a unique appointment ID and free datetime. | Call `book_appointment(...)`. | Assert the appointment is stored, has `SCHEDULED` status, and references the registered patient and practitioner objects. | These assertions verify the complete booking workflow rather than only successful object construction, supporting AC-03.1. |
| TEST-S7-07 | Create fresh shared services but do not register the requested patient or practitioner. | Attempt to book an appointment using the unknown participant ID. | Use `pytest.raises(LookupError)` and assert the appointment was not stored. | This proves unknown participants are rejected without creating partial appointment state, supporting AC-03.2. |
| TEST-S7-08 | Create fresh shared services, register practitioners and book a `SCHEDULED` appointment for `DR1` at a fixed datetime. | Attempt a second booking for `DR1` at exactly the same datetime, then separately book `DR2` at that same time. | Assert the same-practitioner booking raises `ValueError`, while the different-practitioner booking succeeds. | This tests both sides of the exact practitioner-conflict boundary in AC-04.1 and AC-04.2. |
| TEST-S7-09 | Create fresh shared services and a stored `SCHEDULED` appointment. | Call `cancel_appointment("A1")`. | Assert `result is appointment` and `appointment.status is AppointmentStatus.CANCELLED`. | This proves cancellation returns the same stored object and performs the required state transition, supporting AC-05.1. |
| TEST-S7-10 | Create and successfully cancel appointment `A1`. | Retrieve `A1` again from the store. | Assert `data_store.find_appointment("A1") is appointment` and status remains `CANCELLED`. | This directly proves cancelled history remains retrievable in the current session, supporting AC-05.2. |
| TEST-S7-11 | Create and cancel appointment `A1` once so it is already `CANCELLED`. | Attempt to cancel `A1` again. | Use `pytest.raises(ValueError)` and assert the appointment remains `CANCELLED` and retained. | This proves repeated cancellation is rejected without mutating or deleting history, supporting AC-05.3. |
| TEST-S7-14 | Construct and store an appointment with `AppointmentStatus.COMPLETED`. | Attempt to cancel the completed appointment. | Use `pytest.raises(ValueError)` and assert the status remains `COMPLETED`. | This verifies the cancellation state guard and proves an illegal transition does not mutate state. |
| TEST-S7-13 | Create fresh shared services and store appointment `A1`. | Call `find_appointment("A1")`. | Assert the returned result `is` the stored appointment object. | This verifies a known appointment ID returns the actual stored appointment, supporting AC-06.1. |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-S7-15 | Valid Patient fields are trimmed and stored correctly. | `tests/test_domain.py::test_patient_valid_fields_are_trimmed_and_stored` | Passed |
| TEST-S7-03 | Blank or whitespace-only patient ID is rejected with `ValueError`. | `tests/test_domain.py::test_blank_patient_id_is_rejected` | Passed |
| TEST-S7-16 | Blank or whitespace-only patient name is rejected with `ValueError`. | `tests/test_domain.py::test_blank_patient_name_is_rejected` | Passed |
| TEST-S7-17 | Valid Practitioner fields are trimmed and stored correctly. | `tests/test_domain.py::test_practitioner_valid_fields_are_trimmed_and_stored` | Passed |
| TEST-S7-18 | Blank practitioner specialty is rejected with `ValueError`. | `tests/test_domain.py::test_blank_practitioner_specialty_is_rejected` | Passed |
| TEST-S7-19 | A new Appointment starts `SCHEDULED` and retains the supplied patient, practitioner and datetime. | `tests/test_domain.py::test_new_appointment_starts_scheduled_and_retains_participants` | Passed |
| TEST-S7-20 | Appointment construction rejects an invalid patient object. | `tests/test_domain.py::test_appointment_rejects_invalid_patient_object` | Passed |
| TEST-S7-21 | Appointment construction rejects an invalid practitioner object. | `tests/test_domain.py::test_appointment_rejects_invalid_practitioner_object` | Passed |
| TEST-S7-22 | Appointment construction rejects a datetime containing seconds because appointment time requires minute precision. | `tests/test_domain.py::test_appointment_rejects_non_minute_precision_datetime` | Passed |
| TEST-S7-23 | Appointment construction rejects a timezone-aware datetime because the current contract requires a local naive datetime. | `tests/test_domain.py::test_appointment_rejects_timezone_aware_datetime` | Passed |
| TEST-S7-24 | Appointment construction rejects a status value that is not an `AppointmentStatus`. | `tests/test_domain.py::test_appointment_rejects_invalid_status` | Passed |
| TEST-S7-12 | Cancelling a `SCHEDULED` appointment changes it to `CANCELLED`, while repeated cancellation raises `ValueError` and preserves `CANCELLED` state. | `tests/test_domain.py::test_appointment_cancellation_and_repeat_guard` | Passed |
| TEST-S7-14 | A `COMPLETED` appointment cannot be cancelled and remains `COMPLETED` after the rejected transition. | `tests/test_domain.py::test_completed_appointment_cannot_be_cancelled` | Passed |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID | Behaviour | Test file/function | Result |
|---|---|---|---|
| TEST-S7-01 | Valid patient registration stores and returns the same registered patient object. | `tests/test_services.py::test_register_patient_stores_same_object` | Passed |
| TEST-S7-02 | Duplicate patient registration raises `ValueError` and preserves the original stored patient object. | `tests/test_services.py::test_duplicate_patient_preserves_original_stage7` | Passed |
| TEST-S7-04 | Known patient lookup returns the actual registered patient object, including trimmed ID handling. | `tests/test_services.py::test_find_patient_returns_same_registered_object_and_trims_id` | Passed |
| TEST-S7-05 | Valid but unknown patient ID raises `LookupError`. | `tests/test_services.py::test_find_patient_unknown_id_reports_absence` | Passed |
| TEST-S7-06 | Valid booking with registered participants produces and stores a `SCHEDULED` appointment. | `tests/test_starter.py::test_registration_and_booking` | Passed |
| TEST-S7-07 | Booking with an unknown participant is rejected and no appointment is stored. | `tests/test_services.py::test_unknown_participant_booking_leaves_no_appointment` | Passed |
| TEST-S7-08 | Same practitioner at the exact same time conflicts, while the existing supplied regression test also confirms a different practitioner at that time is allowed. | `tests/test_starter.py::test_conflict_rule_and_different_practitioner` | Passed |
| TEST-S7-09 | Cancelling a stored `SCHEDULED` appointment returns the same object and changes status to `CANCELLED`. | `tests/test_services.py::test_cancel_returns_same_object_and_retains_cancelled_history` | Passed |
| TEST-S7-10 | Cancelled appointment history remains retrievable as the same stored object. | `tests/test_services.py::test_cancel_returns_same_object_and_retains_cancelled_history` | Passed |
| TEST-S7-11 | Repeated cancellation raises `ValueError` and preserves the existing `CANCELLED` state and stored object. | `tests/test_services.py::test_repeated_cancellation_is_rejected_without_state_change` | Passed |
| TEST-S7-13 | A known appointment ID returns the same stored appointment object. | `tests/test_services.py::test_known_appointment_lookup_returns_same_object` | Passed |
| TEST-S7-25 | After an appointment is cancelled, the same practitioner can be booked again at the same datetime because only `SCHEDULED` appointments create a conflict. | `tests/test_services.py::test_cancelled_appointment_does_not_block_same_practitioner_time` | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour | Boundary / invalid input | Expected result | Test ID | Additional risk checked |
|---|---|---|---|---|
| Patient identifier validation | Blank or whitespace-only patient ID such as `"   "` | `ValueError` is raised and no patient is created or stored. | TEST-S7-03 | Checks the exact non-blank identifier boundary rather than only normal valid IDs. |
| Patient registration uniqueness | Register a second patient using an already registered ID such as `P1`. | `ValueError` is raised and the original stored patient remains unchanged. | TEST-S7-02 | Checks that duplicate rejection does not overwrite existing session data. |
| Patient lookup | Use a syntactically valid but unknown ID such as `P999`. | `LookupError` is raised. | TEST-S7-05 | Checks the service distinction between invalid input and a valid-but-absent record. |
| Practitioner lookup | Use a valid ID with different case, such as registered `DR1` but lookup `dr1`. | `LookupError` is raised because IDs are case-sensitive. | Existing Stage 6 practitioner lookup regression test | Checks that lookup does not silently normalise case or return the wrong practitioner. |
| Practitioner required field | Use whitespace-only specialty such as `"   "`. | `ValueError` is raised and the practitioner is not created. | TEST-S7-18 | Checks trimming plus required non-blank text validation. |
| Appointment datetime precision | Supply a datetime with non-zero seconds, such as `09:00:01`. | `ValueError` is raised. | TEST-S7-22 | Checks the contract boundary requiring minute precision. |
| Appointment timezone rule | Supply a timezone-aware datetime. | `ValueError` is raised. | TEST-S7-23 | Checks the current contract requiring a local naive datetime. |
| Practitioner conflict | Book a second `SCHEDULED` appointment for the same practitioner at the exact same datetime. | `ValueError` is raised and the second appointment is not stored. | TEST-S7-08 | Checks the precise conflict boundary rather than inventing duration or patient conflicts. |
| Different practitioner at same time | Book another appointment at the same datetime but with a different practitioner. | Booking succeeds. | TEST-S7-08 | Confirms the conflict rule is practitioner-specific. |
| Cancelled slot reuse | Cancel a scheduled appointment, then book the same practitioner again at the same datetime. | The new booking succeeds because the cancelled appointment no longer creates a `SCHEDULED` conflict. | TEST-S7-25 | Checks that cancelled history is retained without incorrectly blocking future booking at that time. |
| Repeated cancellation | Attempt to cancel an appointment already in `CANCELLED` state. | `ValueError` is raised, status remains `CANCELLED`, and the appointment remains stored. | TEST-S7-11 | Checks both rejection and no mutation after failure. |
| Invalid cancellation transition | Attempt to cancel an appointment in `COMPLETED` state. | `ValueError` is raised and status remains `COMPLETED`. | TEST-S7-14 | Checks that illegal domain transitions are atomic and preserve state. |
| Unknown appointment lookup | Request a valid but absent appointment ID. | `LookupError` is raised at the service boundary. | Existing Stage 6 appointment lookup/cancellation regression evidence | Checks absence handling without confusing it with invalid input. |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-05 Prevent practitioner conflict

Acceptance criterion: AC-04.1 — A `SCHEDULED` appointment for the same practitioner at the exact same datetime conflicts and must be rejected.

Behaviour to test: Verify that SmartCare rejects a second `SCHEDULED` appointment for the same practitioner at the exact same datetime without changing the already stored appointment.

Human-first test idea/categories: Before using Copilot, the planned cases were: a valid conflict case using the same practitioner and exact datetime; a nearby non-conflict case using a different practitioner at the same datetime; and a state-preservation check confirming the rejected appointment is not stored.

Prompt and purpose: Ask Copilot to propose requirement-linked pytest candidates for FR-05 / AC-04.1 using only the current SmartCare public contracts, with meaningful assertions and no invented overlap, duration, notification or patient-conflict rules.

### Candidate 1

- Copilot test idea/candidate: Create a fresh shared `SmartCareDataStore`, register one patient and practitioner, book appointment `A1` for `DR1` at a fixed datetime, then attempt to book `A2` for the same practitioner at the exact same datetime.
- What it claims to verify: Same practitioner + exact datetime + existing `SCHEDULED` appointment is rejected as a conflict.
- Requirement trace: FR-05 / AC-04.1.
- Assertion quality: Strong. Uses `pytest.raises(ValueError)` for the rejected booking and can also verify that `A2` was not stored.
- Human critique: This candidate directly matches the published conflict rule and uses public service/store behaviour. It can fail for the right reason if the conflict protection is broken.
- Decision: Accept
- Reason: It directly verifies AC-04.1 without inventing extra business rules.
- Final test reference if accepted/modified: `tests/test_starter.py::test_conflict_rule_and_different_practitioner`
- Actual verification result: Passed in the Stage 7 regression suite.

### Candidate 2

- Copilot test idea/candidate: Book `A1` for `DR1` at a fixed datetime, then book `A2` for a different practitioner `DR2` at the same datetime.
- What it claims to verify: The conflict rule is practitioner-specific and does not reject another practitioner using the same datetime.
- Requirement trace: Supporting evidence around FR-05; this corresponds to AC-04.2 rather than AC-04.1.
- Assertion quality: Strong if it asserts that the second appointment is successfully stored and references `DR2`.
- Human critique: The test is useful but does not verify AC-04.1 itself. It provides complementary boundary evidence for the other side of the practitioner-conflict rule.
- Decision: Modify
- Reason: Retain it as explicit AC-04.2 boundary evidence rather than incorrectly labelling it as AC-04.1.
- Final test reference if accepted/modified: `tests/test_starter.py::test_conflict_rule_and_different_practitioner`
- Actual verification result: Passed in the Stage 7 regression suite.

### Candidate 3

- Copilot test idea/candidate: Reject a booking for the same practitioner when the second appointment starts within 30 minutes of the first appointment.
- What it claims to verify: Practitioner appointments must not overlap within a 30-minute duration window.
- Requirement trace: No valid trace to FR-05 / AC-04.1.
- Assertion quality: The assertion could be technically precise, but it would test an invented rule.
- Human critique: The current SmartCare contract defines conflict only as the same practitioner at the exact same datetime while an existing appointment is `SCHEDULED`. No appointment duration or overlap window is specified.
- Decision: Reject
- Reason: The candidate invents a 30-minute overlap rule that is not part of the approved requirement and could incorrectly fail a correct implementation.
- Final test reference if accepted/modified: Not retained.
- Actual verification result: Not run because the candidate was rejected before implementation.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? The candidate that proposed rejecting appointments within a 30-minute overlap window initially sounded reasonable because appointment conflicts often involve overlapping times. However, it was weak for this assignment because the SmartCare requirement only defines a conflict as the same practitioner at the exact same datetime while an existing appointment is `SCHEDULED`.
Why was it weak? It was weak because the SmartCare requirement does not define a 30-minute overlap rule. FR-05 only defines a conflict as the same practitioner at the exact same datetime while an existing appointment is `SCHEDULED`. The candidate therefore tested invented behaviour rather than an approved requirement.
How did you strengthen it? I rejected the invented 30-minute overlap rule and kept the test design tied to the published FR-05 contract. I used one case for the same practitioner at the exact same datetime and a complementary case for a different practitioner at the same time. This makes the evidence traceable to AC-04.1 and AC-04.2.
Accepted / modified / rejected test decisions and evidence: See Section H above for the recorded Accept / Modify / Reject decisions and verification evidence.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

- Working directory: `project/`
- Full-suite command: `python3 -m pytest`
- Tested SHA: b7ae8f301cc00cf12657a7910b3d8169da95b840
- Passed count: 38
- Failed count: 0
- Errors: 0
- Failures observed: None in the final Stage 7 regression run.
- Interpretation: The accumulated Stage 6 regression tests, new Stage 7 domain tests and new Stage 7 service tests all passed together. This provides verification evidence for the tested scenarios and assertions, but it does not prove that every possible SmartCare behaviour or input combination is correct.
- Coverage used: No. Code coverage tooling was not used because Stage 7 does not require a coverage percentage. Test quality was assessed through requirement traceability, meaningful assertions, positive/negative/boundary cases and observed regression results.
- Independence / repeatability check: Tests use fresh stores or freshly constructed domain objects with fixed synthetic data, so they do not depend on execution order, wall-clock time or external services.
Individual test runs and changed-order independence evidence: [commands, results, links]
Optional tutor-led demonstration notes: [optional; leave blank if not used]
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.
Requirement → test → failure/observation → diagnosis → change → verification: [concise links where applicable]

## K What the Suite Still Does Not Prove

What does your test suite still not prove?  
The Stage 7 test suite does not prove that every possible SmartCare input, workflow sequence or future feature is correct. It verifies the specific published requirements and contracts covered by the current tests, including registration, lookup, booking, practitioner conflicts, cancellation and retained history. It does not prove behaviour outside the approved requirements, such as appointment durations, notification delivery, patient schedule conflicts, persistence between sessions or later Stage 9 query/menu behaviour.

Coverage if used: Not used.

Which uncovered areas matter, and why does coverage percentage alone not establish correctness?  
The main uncovered areas are behaviours outside the current Stage 7 scope, especially later Stage 9 query and console functionality and any other requirements not represented by the current tests. A coverage percentage alone does not establish correctness because it only shows which code executed. It does not prove that the tests are linked to the correct requirements, use meaningful assertions, cover important boundaries or expect the correct behaviour.

Optional fixtures/parametrisation used and why, if any: Not used. The tests use clear local setup and fresh objects or a fresh `SmartCareDataStore` for each test so that cases remain independent and easy to understand.

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

- Issue/task: Stage 7 requirement-linked domain and service testing — GitHub Issue #6
- Issue link: https://github.com/aksherakandula-git/st1-assignment--3/issues/6
- Branch: `feature/stage7-testing`
- PR link: https://github.com/aksherakandula-git/st1-assignment--3/pull/7
- PR title: Add Stage 7 requirement-linked tests
- Reviewer: Harleen Partola (`Harleenpartola`)
- Full regression result before review: 38 passed
- Review focus: Requirement-to-test traceability, meaningful assertions, positive/negative/boundary coverage, independent test setup, supplied versus student-authored evidence and avoidance of invented SmartCare behaviour.
- Reviewer feedback: Harleen requested a final tidy-up of the Stage 7 evidence document. She identified remaining template placeholders such as `[complete]` and `[response]`, duplicate Group/tutorial entries, an unused Activity 1 template table, leftover Activity 2 placeholders, empty Activity 4 candidate rows, a duplicate/empty Service Test Evidence table and heading, and other unused template content.
- Author response/change: The requested evidence-document cleanup is being completed on the same `feature/stage7-testing` branch by removing unused placeholders, duplicate headings/tables and template-only content while retaining the completed Stage 7 evidence.
- Verification after change: The production code and tests are unchanged by the evidence cleanup. The regression suite previously reported 38 passed; the full suite will be rerun after the tidy-up before requesting reviewer recheck.
- Reviewer recheck: Pending after evidence tidy-up is pushed.
- Review outcome: Pending.
- Merge outcome: Pending.

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

### Akshera Kandula

- Member: Akshera Kandula — `aksherakandula-git`
- Test design: Designed requirement-linked positive, negative and boundary cases for FR-01, FR-02, FR-04, FR-05, FR-06, FR-07 and FR-08.
- Domain testing: Created `project/tests/test_domain.py` covering Patient and Practitioner validation, Appointment construction, initial state and guarded cancellation.
- Service testing: Extended `project/tests/test_services.py` with additional evidence for registration, duplicate preservation, lookup, booking rejection, appointment lookup and cancelled-slot reuse.
- Traceability: Assigned TEST IDs and linked tests to the relevant functional requirements, acceptance criteria and revision 2 validation contracts.
- Copilot/test-assistant critique: Used human-first test design, evaluated candidate tests, accepted requirement-linked candidates, modified incorrectly traced candidates and rejected the invented 30-minute overlap rule.
- Regression verification: Ran the focused and full pytest suites. The Stage 7 branch regression suite reported 38 passed.
- Diagnosis/setup: Identified that an early `test_domain.py` command failed because pytest was run from the repository root rather than `project/`; corrected the working directory and reran successfully.
- Git/integration: Created the Stage 7 issue, worked on `feature/stage7-testing`, committed and pushed the testing changes and opened PR #7 for another-member review.
- Documentation: Completed the Stage 7 requirement-to-test matrix, test-design reasoning, evidence tables and regression record.

### Harleen Partola

- Member: Harleen Partola — `Harleenpartola`
- Review: Reviewed PR #7 and checked the Stage 7 tests and evidence for requirement traceability, assertion quality, independent setup and scope.
- Documentation review: Identified remaining template placeholders, duplicate headings/tables and unused template content in the Stage 7 evidence document and requested a final tidy-up.
- Team support: Provided independent review feedback before Stage 7 integration.
- Final review/integration: Pending recheck and approval after the requested evidence-document tidy-up.

## N Formative Questions

1. What question does verification answer?  
Verification asks whether the implementation meets the specified requirements and behaves as the approved contract says it should.

2. What question does validation answer?  
Validation asks whether the specified product or requirement actually meets the intended user or business need.

3. What is a unit test?  
A unit test checks a small, focused unit of behaviour in isolation, such as a domain object's validation rule or state transition, using known inputs and meaningful assertions.

4. What is a pytest fixture?  
A pytest fixture is reusable setup that prepares data or objects for tests. It can help provide fresh, consistent test state without repeating the same setup code in every test.

5. What is parametrisation in pytest?  
Parametrisation lets the same test logic run with several meaningful input and expected-output combinations, reducing duplication while still checking distinct cases.

6. What is regression testing?  
Regression testing reruns previously useful tests after changes to confirm that earlier required behaviour still works and that new work has not broken existing functionality.

7. What does code coverage tell us, and what does it not prove?  
Code coverage shows which code was executed by the tests. It can help identify untested areas, but it does not prove that requirements are correct, assertions are meaningful, important boundaries are covered or the whole program is correct.

8. What makes an assertion weak?  
An assertion is weak when it does not directly check the required observable behaviour or could still pass while the requirement is broken. Examples include `assert True`, `is not None` when identity matters, or checking only that a result list is non-empty when exact contents matter.

9. What is the appropriate role of GitHub Copilot as a test assistant?  
Copilot can suggest candidate tests, edge cases and review questions, but a human must check every suggestion against the real requirement and public contract. Generated tests should be accepted, modified or rejected based on traceability, assertion quality and whether they invent any behaviour.

10. What is the Stage 7 engineering rule?  
The Stage 7 engineering rule is to ask what required behaviour each test actually proves: derive the expectation from the approved requirement, use meaningful and independent assertions, run focused and full regression tests, interpret failures against the contract, and retain traceable evidence for the verified result.

## O Stage Completion

Tested Stage 7 main SHA: [complete]
Full-suite result: [complete]
Unresolved defects and effect on baseline: [complete or none]
Clean working tree and integration evidence: [complete]
Stage 8 handover status: [complete; no Stage 8 work assigned]
All tutorial/formative responses and traceability/Copilot decisions complete: [confirm]
