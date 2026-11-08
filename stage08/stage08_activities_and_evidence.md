# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: [complete]
Members and UG/PG cohorts: [complete]
Record owner / contribution links for each member: [complete]

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
**Response and reason:**

The method has several code smells, including duplicated status strings, direct collection manipulation, printing inside business logic, repeated validation and deeply nested conditionals.

Small refactorings could include extracting repeated conflict-checking logic into a helper, replacing magic status strings with the existing `AppointmentStatus` enum, and simplifying nested conditionals. Storage operations should use the existing `SmartCareDataStore` rather than directly manipulating collections.

**Classification of proposed changes:**

- Rename `appt` to `appointment` – Refactoring, because it improves readability without changing behaviour.
- Extract a repeated conflict helper – Refactoring, because it reduces duplicated code while keeping the same conflict rules.
- Add rescheduling – Feature, because it introduces new functionality.
- Restore retained cancellation lookup – Repair, because it fixes incorrect existing behaviour.
- Replace a magic status string with the existing enum – Refactoring, because it improves consistency without changing behaviour.

The main behaviour to preserve is appointment booking, cancellation, status transitions, practitioner conflict checking, validation, and the use of the shared data store. No new functionality should be introduced during refactoring.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

## B. Stage 7 baseline and safe preparation

## Section B – Baseline and Preparation Evidence

### Official Stage 8 preparation

The Stage 8 preparation was completed by Pranav using the official preparation utility, version 1.1. The prepared debugging state was pushed to the group's shared GitHub repository on a separate branch. The existing `main` branch remained unchanged.

**Preparation utility:** Version 1.1

**Baseline Git SHA:**
`e5e7b65da71cbde83301cf65b51e3f35bf3bf294`

**Baseline SHA256:**
`b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375`

**Prepared branch:** `debug/stage08`

### Prepared defects

- **F8-01 – Practitioner conflict:** The prepared defect affects the checking of appointments for the same practitioner at the same date and time.
- **F8-02 – Retained-history lookup:** The prepared defect affects retrieving an appointment after it has been cancelled.

### Official preparation verification

Pranav reported that the preparation utility successfully completed its checks and confirmed exactly two expected preparation fault signatures.

The supplied preparation output included:

`CHECK ONLY: project unchanged; both proposed fault signatures verified in a temporary copy`

`PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup`

`VERIFIED: exactly 2 expected failures; both approved symptom signatures present`

The utility also reported that a backup and hash were recorded in `.stage8_faults`.

### Local verification by group member

### Local prepared-branch verification

**Local Git SHA:** `ab2234955ce40f4a4bec24fb160939001a92e37f`

**Test command:** `py -m pytest -q`

**Working directory:** `project`

**Actual result:** 35 passed, 3 failed in 0.12 seconds.

**Observed failures:**

1. `test_cancel_returns_same_object_and_retains_cancelled_history` failed because `data_store.find_appointment("A1")` returned `None` instead of the original cancelled appointment.
2. `test_repeated_cancellation_is_rejected_without_state_change` failed because the second cancellation raised `LookupError` instead of the expected `ValueError`. The appointment could no longer be found after cancellation.
3. `test_conflict_rule_and_different_practitioner` failed because booking another appointment for the same practitioner at the same date and time did not raise the expected `ValueError`.

These results indicate two defects: cancelled appointments are not being retained for lookup, and the practitioner-conflict rule is not being enforced.

The official preparation was performed by Pranav. The local branch and test results above will be recorded separately after checking the prepared branch on my computer.

## B. New Local Regression test reproduction
### Local regression test reproduction

**Test file:** `project/tests/test_regressions.py`

**Test command:** `py -m pytest tests/test_regressions.py -q`

**Actual result:** 3 failed in 0.10 seconds.

**F8-01 – Practitioner conflict**

- Test: `test_f8_01_same_practitioner_cannot_have_two_scheduled_appointments`
- Actual failure: `Failed: DID NOT RAISE <class 'ValueError'>`.
- This confirms that the system did not reject a second scheduled appointment for the same practitioner at the same date and time.

**F8-02 – Cancelled appointment history**

- Test: `test_f8_02_cancelled_appointment_remains_available_in_store`
- Actual failure: `data_store.find_appointment("A1")` returned `None` instead of the original appointment object.
- This confirms that the cancelled appointment could not be retrieved through the data-store lookup.

**F8-02 – Repeated cancellation**

- Test: `test_f8_02_repeated_cancellation_is_rejected_without_state_change`
- Actual failure: `LookupError: Appointment not found`.
- Expected: `ValueError` when attempting to cancel an already-cancelled appointment.

**Conclusion:** All three regression tests reproduced the expected symptoms of F8-01 and F8-02 before any repairs were made.

### Full test suite after repairs

**Command:** `py -m pytest -q`

**Working directory:** `project`

**Actual result:** 41 passed in 0.04 seconds.

**Conclusion:** All project tests passed after repairing F8-01 and F8-02, including the new regression tests. No test failures remained.

## C. F8-01 diagnosis and repair
**Symptom / observed behaviour:** The system allowed two scheduled appointments for the same practitioner at the same date and time.

**Expected behaviour and requirement:** A second scheduled appointment for the same practitioner at the exact same date and time must be rejected with a ValueError. A different practitioner must still be allowed to book at that time.

**Minimal synthetic reproduction steps:** Register one patient and two practitioners. Book an appointment for the first practitioner, then attempt to book another appointment for that same practitioner at the same date and time.

**Meaningful failing test path/name and exact relevant failure:** `project/tests/test_regressions.py::test_f8_01_same_practitioner_cannot_have_two_scheduled_appointments`. Before repair, the test failed with `Failed: DID NOT RAISE <class 'ValueError'>`.

**Human hypothesis and intended checks:** See Section E, F8-01.

**Supported root cause and inspected code/runtime evidence:** The `has_practitioner_conflict()` method in `smartcare/data_store.py` used `!=` when comparing practitioner IDs. This checked for a different practitioner instead of the same practitioner.

**Smallest justified fix / diff / why other behaviour is preserved:** Changed the practitioner ID comparison from `!=` to `==`. This makes the conflict check apply to the same practitioner while preserving bookings for different practitioners.

**Repair SHA / focused verification result:** The regression test was rerun after the change. Result: 1 passed, 2 failed in 0.05 seconds. The F8-01 test passed and the two remaining failures relate to F8-02. Record the repair commit SHA after committing the change.

## D. F8-02 diagnosis and repair

**Symptom / observed behaviour:** After an appointment was cancelled, the data store could no longer retrieve it using its appointment ID. Attempting to cancel it again raised `LookupError` instead of `ValueError`.

**Expected behaviour and requirement:** Cancelled appointments must remain stored and retrievable. Repeated cancellation must raise `ValueError` without changing the appointment's cancelled status.

**Minimal synthetic reproduction steps:** Register a patient and practitioner, book an appointment, cancel it, then check whether the data store can still find the same appointment object. Attempt to cancel it again.

**Meaningful failing test path/name and exact relevant failure:**
- `test_f8_02_cancelled_appointment_remains_available_in_store` failed because `find_appointment("A1")` returned `None`.
- `test_f8_02_repeated_cancellation_is_rejected_without_state_change` failed with `LookupError: Appointment not found`.

**Human hypothesis and intended checks:** See Section E, F8-02.

**Supported root cause and inspected code/runtime evidence:** The `find_appointment()` method in `smartcare/data_store.py` excluded appointments with the status `"cancelled"`. This prevented the service from retrieving the appointment and reaching the domain cancellation validation.

**Smallest justified fix / diff / why other behaviour is preserved:** Removed the cancelled-status condition from the data-store lookup. The method now finds appointments by ID regardless of their status, while still returning `None` for a valid ID that does not exist and raising `ValueError` for a blank ID.

**Repair SHA / focused verification result:** The F8-02 regression tests passed after the change. The focused regression suite subsequently reported 3 passed. Record the repair commit SHA after committing the change.
**Repair SHA / focused verification result:** The F8-02 regression tests passed after the change. The focused regression suite subsequently reported 3 passed. Record the repair commit SHA after committing the change.

## E. Human-first hypotheses

## E. Human-first hypotheses

### F8-01 human entry

**Likely cause and why plausible:**

I believe the issue is in the `has_practitioner_conflict()` method in `data_store.py`. The practitioner ID comparison appears to check for a different practitioner instead of the same practitioner. This would explain why the system allows two appointments for the same practitioner at the same date and time.

**Evidence intended to inspect / competing explanation / discriminating check:**

I will inspect the practitioner ID comparison, appointment date and time, and appointment status conditions. I will also check how `AppointmentService` uses this method before booking. Another possible explanation is that the booking service is not correctly checking the conflict result.

**Member and saved sequence/time or commit showing this preceded consultation:**

Member: Harleen Partola.  
Sequence: Initial investigation after running the prepared Stage 8 tests and before consulting Copilot.  
Evidence: Local test output and Git commit/history, if available.

### F8-02 human entry

**Likely cause and why plausible:**

I believe the issue is in the `find_appointment()` method in `data_store.py`. The method appears to exclude appointments with a cancelled status. This would explain why cancelled appointments cannot be found and why attempting to cancel one again raises a `LookupError`.

**Evidence intended to inspect / competing explanation / discriminating check:**

I will inspect the status condition in `find_appointment()` and check whether cancelled appointments remain in the appointment collection. I will also inspect the cancellation method in `AppointmentService` to see how it handles appointments that have already been cancelled. Another possible explanation is that the cancellation process removes the appointment from the store.

**Member and saved sequence/time or commit showing this preceded consultation:**

Member: Harleen Partola.  
Sequence: Initial investigation after running the prepared Stage 8 tests and before consulting Copilot.  
Evidence: Local test output and Git commit/history, if available.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
### F8-01 Copilot review

**Actual prompt / output reference and member:**

Member: Harleen Partola.

Tool: GitHub Copilot Chat in PyCharm.

Prompt: Reviewed the practitioner booking conflict, including the observed behaviour, expected behaviour, reproduction, failing test, initial human hypothesis and relevant code. Requested three ranked possible causes and checks without changing any files.

Output: GitHub Copilot Chat response saved in the Stage 8 evidence.

**1. Ranked suggestion: Reversed practitioner comparison**

- **Evidence check:** Inspect the practitioner ID comparison in `data_store.py`, inside `has_practitioner_conflict()`.
- **Observed evidence:** The condition uses `!= practitioner_id`, meaning it checks for a different practitioner instead of the same practitioner.
- **Assessment:** Correct.
- **Decision:** Accept. The actual code supports this explanation and matches the failing test.

**2. Ranked suggestion: Appointment may not be in the same data store**

- **Evidence check:** Check whether the first appointment is stored and whether the service uses the same data-store object.
- **Observed evidence:** The existing test successfully books the first appointment, and the service checks conflicts using its own shared `data_store`.
- **Assessment:** Unlikely / not supported by the observed failure.
- **Decision:** Reject as the main cause because the reversed practitioner comparison directly explains the failure.

**3. Ranked suggestion: Appointment time or status may not match**

- **Evidence check:** Inspect the stored appointment's date/time and status.
- **Observed evidence:** The test uses the same date/time for both bookings, and the domain uses the `scheduled` status value.
- **Assessment:** Unlikely / not supported by the observed failure.
- **Decision:** Reject as the main cause because the practitioner ID comparison is the confirmed issue.

**Final human conclusion and comparison with initial hypothesis:**

Copilot confirmed my initial hypothesis. The problem is caused by the reversed practitioner ID comparison in `has_practitioner_conflict()`. This prevents the system from detecting appointments for the same practitioner at the same time. The other suggestions were possible explanations, but the code evidence supports the first suggestion as the actual cause. Copilot did not change any files.
### F8-02 Copilot review
### F8-02 Copilot review

**Actual prompt / output reference and member:**

Member: Harleen Partola.

Tool: GitHub Copilot Chat in PyCharm.

Prompt: Reviewed the cancelled appointment history issue, including the observed behaviour, expected behaviour, reproduction steps, failing tests, initial human hypothesis and relevant code. Requested three ranked causes and evidence checks without changing any files.

Output: GitHub Copilot Chat response saved in the Stage 8 evidence.

**1. Ranked suggestion: Data-store lookup filters out cancelled appointments**

- **Evidence check:** Inspect `find_appointment()` in `data_store.py` and check whether cancelled appointments remain in the appointment collection.
- **Observed evidence:** The method contains `appointment.status.value != "cancelled"`, which excludes cancelled appointments from lookup. However, `list_appointments()` still returns the stored appointments.
- **Assessment:** Correct.
- **Decision:** Accept. This directly explains why the cancelled appointment cannot be found.

**2. Ranked suggestion: The service raises the wrong error when cancelling again**

- **Evidence check:** Inspect `AppointmentService.cancel_appointment()` and trace what happens when the appointment has already been cancelled.
- **Observed evidence:** The service calls `find_appointment()` first. Because the data store returns `None` for cancelled appointments, the service raises `LookupError` before the domain cancellation method can reject the repeated cancellation.
- **Assessment:** Correct.
- **Decision:** Accept. This explains why the repeated cancellation test raises `LookupError` instead of `ValueError`.

**3. Ranked suggestion: The test may be using a different module copy**

- **Evidence check:** Check which `smartcare` package path is being used by the test runner.
- **Observed evidence:** The inspected code already explains both failed tests. There is no evidence that a different module copy is being used.
- **Assessment:** Unlikely / not supported.
- **Decision:** Reject as the main cause because the lookup condition directly explains the failures.

**Final human conclusion and comparison with initial hypothesis:**

Copilot supported my initial hypothesis. The main issue is that `find_appointment()` excludes cancelled appointments even though they remain stored in the data store. This also causes the repeated cancellation error because the service cannot retrieve the appointment to reach the domain method that should reject the second cancellation with `ValueError`. The third suggestion was not supported by the inspected code. Copilot did not change any files.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

## H. Refactoring decision and before/after verification

**Smell and exact location:** Repeated validation logic in `project/smartcare/data_store.py`, inside the `find_appointment()` method. The method manually checks whether the appointment ID is a valid, non-empty string, even though the existing `required_text()` helper is already used in other lookup methods.

**Small proposed structural change / why justified:** Replace the manual appointment ID validation with the existing `required_text(appointment_id, "Appointment ID")` helper. This makes validation consistent with `find_patient()` and `find_practitioner()` and avoids duplicating code.

**External behaviour to preserve / relevant tests:**
- Invalid or blank appointment IDs must raise `ValueError`.
- Valid but missing appointment IDs must return `None`.
- Cancelled appointments must remain available through lookup.
- The same stored appointment object must be returned.
- Practitioner conflict detection must continue working correctly.
- All existing tests and the three regression tests must continue passing.
Before result: see G, full passing suite.
**Actual change / diff / separate refactor SHA:**

Updated `find_appointment()` in `project/smartcare/data_store.py` to use the existing `required_text()` helper instead of manually checking the appointment ID. This reduced duplicated validation logic and kept the existing lookup behaviour unchanged.

**Focused and full after-refactor commands / working directory / results / evidence:**

Working directory: `project`

- `py -m pytest tests/test_regressions.py -q` – 3 passed.
- `py -m pytest -q` – 41 passed in 0.5 seconds.

**Result — accepted, revised or rejected / reason / behaviour-preservation conclusion:**

Accepted. The refactoring was successful because it reused the existing validation helper and made the code more consistent. All three regression tests and all 41 project tests passed after the change. The required appointment lookup and cancellation behaviour remained intact.
## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]
