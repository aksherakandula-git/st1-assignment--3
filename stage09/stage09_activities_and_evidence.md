# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Session/domain state| Patient details must remain available during the session so patients can be found and used when booking appointments.|
| Appointment history | Session/domain state| Appointments must remain available during the session, including cancelled appointments.|
| Temporary menu choice | Transient state| The menu choice is only needed to decide which action the user wants to perform.|
| Practitioner specialty | Session/domain state| Specialty is part of the practitioner's registered information.|
| Debug print output | Transient state| Debug output is only used to help developers check the program.|
| Appointment status | Session/domain state| Status records whether an appointment is scheduled, cancelled or completed.|

What is intentionally lost on exit? All session data is lost when the application exits. This includes registered patients, practitioners and appointments because Stage 9 uses in-memory storage and does not include permanent database storage.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | One Appointment object| Tuple of date_time and appointment_id| Creates a consistent sorting key without changing the appointment.| Uses the existing appointment date/time and ID.|
| select_appointments | Appointment list, practitioner ID (string), optional status (AppointmentStatus or None)| New sorted list of appointments| Selects appointments for one practitioner and optional status. Must not change the original list.| Uses the existing appointment practitioner ID and status.|
| Service listing | Practitioner ID (string), optional AppointmentStatus or None| List of matching appointments| Checks the practitioner, validates the status, retrieves appointments and calls the query function.| Uses existing store and service contracts.|
| Console | User input and existing service objects| Printed menu, messages and results| Collects input, converts values, calls services and displays errors.| Reuses existing date/time parser and appointment formatter.|

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: Patient ID and name belong to the Patient object. Practitioner ID, name and specialty belong to the Practitioner object. Appointment ID, patient, practitioner, date_time and status belong to the Appointment object. The implementation should use the existing classes and fields rather than creating duplicate information.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | The domain object is handling user interaction.| Appointment should enforce cancellation rules. The console collects input and calls the service.|
| Service prints/reads the menu | The service is handling console interaction.| The console handles prompts and output. The service coordinates application operations.|
| Query sorts its source in place | The query changes the original appointment list.| The query should use sorted() to return a new list without changing the source.|
| Store prints Appointment saved | The store is handling user-interface output.| The store manages data. The console displays the success message.|

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: appointments.sort(key=appointment_sort_key) changes the original list and returns None. sorted(appointments, key=appointment_sort_key) creates a new sorted list and leaves the original list unchanged. A good mutation check is to save the original list order before calling the query and compare it afterwards. The returned list should also have a different identity from the original list.

Score-example prediction and explanation of passing the named key: The sorting key returns the appointment date_time and appointment_id. Appointments are sorted by date and time first. If two appointments have the same date and time, the appointment ID is used to decide their order. Using a named key makes the sorting rule reusable and easier to test.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: Cancellation does not delete an appointment. It changes the appointment status to CANCELLED while keeping the appointment in the data store. This means the appointment can still be found by its ID and included when listing all appointment statuses. When filtering by SCHEDULED only, the cancelled appointment should not appear. These checks confirm that appointment history is retained during the session.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning:The design decisions were based on the Stage 9 requirements and the existing SmartCare structure. The query functions will use explicit inputs and return results without changing the original appointment data. The service layer will coordinate data-store access and validation, while the console will handle user input and output. Appointment cancellation will update the appointment status rather than deleting the record, so appointment history remains available during the session. The existing domain classes, service contracts and validation rules will be reused rather than creating duplicate structures or adding database storage.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01| Appointment list and practitioner ID| Query selects appointments for the requested practitioner.| Only matching appointments are returned.| Test matching and different practitioner IDs.|
| QRY-02| Practitioner ID and optional status                                    | Query filters by the supplied status when provided.                                                          | No status returns all statuses. A supplied enum returns only that status.| Test all enum statuses and no matches.|
| QRY-03| Appointments with different and equal date/times                                   | Query sorts using the named appointment sorting key.                                                         | Sorted by date/time, then appointment ID. Original list stays unchanged.| Test ordering, tie-break and source preservation.|
| FP-01      | Same explicit inputs used repeatedly                                                                                  | Pure query function                                                                                                               | Repeated calls return equivalent results without hidden state or I/O.                                                                        | Repeat calls and compare results.                                                 |
| FP-02     | Empty, already sorted and unsorted lists                                                                                   | Pure query function                                                                                                             | Each call returns a new list without modifying the original list or appointment fields.                                                                       | Check list identity, original order and fields.                                                 |
| FP-03   | Appointment object                                                                                  | Named sorting key                                                                                                             | Returns the expected date/time and appointment ID tuple.                                                                        | Test the key directly and check query reuse.                                                |
| QRY-04      | Practitioner ID and optional enum status                                                                                  | Appointment service listing function                                                                                                              | Known practitioner returns results or an empty list. Unknown practitioner raises LookupError. Invalid input raises ValueError.                                                                        | Test known, unknown, blank and invalid status.                                                 |
| UI-01      | Synthetic patient, practitioners and appointment details                                                                                  | Console calls existing services.                                                                                                              | Registration, booking, conflict checking, cancellation and listing work in one session.                                                                        | Run the full menu workflow.                                                 |
| UI-02      | Invalid menu choices and invalid user input                                                                                  | Console and existing service validation                                                                                                              | Displays a useful error and returns to the menu without changing records.                                                                        | Test invalid inputs followed by a successful action.                                                 |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: The query functions should receive all required information through their parameters instead of relying on a global data store. This makes them easier to test and reuse. The query should return a new list but can safely reuse references to the existing Appointment objects because it does not modify those objects.

An empty result means the practitioner exists and the request is valid, but no appointments match. An unknown practitioner means the ID is not registered and should raise LookupError. A blank or invalid ID should raise ValueError under the existing validation rules. An invalid status should also raise ValueError.

The console should convert the user's status text into an AppointmentStatus enum before passing it to the service. The service should receive an enum or None, rather than interpreting menu text itself.

When an operation is rejected, the program should display an error and return to the menu. The tests should check that the original records and their fields have not changed after a rejected operation. This helps confirm that failed bookings, registrations or cancellations do not leave partial changes.

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| QRY-01| smartcare/queries.py; tests/test_queries.py| Filters appointments by practitioner ID and excludes other practitioners.|Passed | tests/test_queries.py|
| QRY-02| smartcare/queries.py; tests/test_queries.py| Checks that the default includes all statuses and an explicit status filters correctly.|Passed| tests/test_queries.py|
| QRY-03| smartcare/queries.py; tests/test_queries.py| Checks date/time ordering and appointment ID tie-breaking for equal times.| Passed| tests/test_queries.py|
| QRY-04| smartcare/services.py; tests/test_workflows.py| Checks known practitioners, empty results, unknown practitioners, blank IDs and invalid statuses.| Passed| tests/test_workflows.py|
| FP-01| smartcare/queries.py; tests/test_queries.py| Checks repeatable query results using the same inputs.| Passed| tests/test_queries.py|
| FP-02| smartcare/queries.py; tests/test_queries.py| Checks empty results, fresh list identity and unchanged source-list order.| Passed| tests/test_queries.py|
| FP-03| smartcare/queries.py; tests/test_queries.py| Checks the named sorting key directly and its use by the query.| Passed| tests/test_queries.py|

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: The query functions use explicit inputs and do not access the data store, global variables, files or external services. The sorting key returns a tuple containing the appointment date/time and appointment ID. The selection function filters the supplied appointments and uses sorted() to return a new list. It does not change the original list or modify the Appointment objects. The service retrieves the appointments from the shared data store and passes them to the query function.

What the tests do and do not establish: The automated tests verify practitioner filtering, status filtering, ordering, tie-breaking, fresh list results, source-list preservation and service validation. The full test suite completed successfully with 58 passed in 0.09 seconds. These tests establish that the tested behaviour works for the supplied cases, but they do not prove that every possible input or real-world deployment scenario has been tested.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | Run python main.py --interactive. Register P1 (Alex Example), D1 (Taylor Example) and D2 (Jordan Example). Book A1 with D1 at 2026-10-01 09:00, attempt A-CONFLICT with D1 at the same time, then book A2 with D2 at the same time. Cancel and find A1. List D1's appointments with a blank status, then with scheduled. Book A3 with D1 at the same time and list again.| D1's conflicting booking is rejected; D2's booking is accepted. A1 remains visible as cancelled, is excluded from scheduled-only results, and A3 can use the released time slot.| Passed. Conflict was rejected, A2 was accepted, A1 remained cancelled when found and listed, scheduled-only returned no matching appointments, and A3 was accepted. Final listing showed A1 cancelled and A3 scheduled.| Manual terminal observation; no screenshot captured.|
| UI-02 invalid-input recovery | Run python main.py --interactive. Try menu choice 99, a blank practitioner ID, unknown practitioner DR999, malformed date not-a-date, impossible date 2026-02-30 10:00, unknown appointment A999, and cancelling A1 again.| Each invalid input displays a clear error. The application returns to the menu and continues running without crashing.| Passed. Invalid menu choice, blank and unknown practitioner, invalid dates, unknown appointment and repeated cancellation produced errors. The menu remained available.| Manual terminal observation; no screenshot captured.|
| Automated service workflow | Run python -m pytest -q from the project directory. See tests/test_queries.py, tests/test_workflows.py and the existing test files.| Query and service behaviour passes, including filtering, ordering, validation, fresh results and regression checks.| Passed. Full test suite: 58 passed in 0.09 seconds.| Test result recorded in this evidence document; no separate log file saved.|

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

Manual testing note:
The interactive checks were performed manually using python main.py --interactive. The results were observed in the terminal during the test session. No separate screenshots or saved terminal transcript were captured, so the results are recorded as manual observations rather than linked screenshot evidence.

## E. GitHub Copilot review and human decisions
1. Human design reference
The Stage 9 design was based on the existing SmartCare project structure and the Stage 9 requirements. The query functions were kept separate from the service layer so that filtering and sorting could be tested independently. The service layer validates the practitioner and status before retrieving and filtering appointments. The console handles user input and output, while the services enforce the application rules.

2. GitHub Copilot prompt and context
GitHub Copilot review was not run for this implementation. No Copilot prompt or review response is available to record.

3. Copilot response
Not applicable – GitHub Copilot was not used to review the Stage 9 implementation.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Copilot| No GitHub Copilot findings were produced because a Copilot review was not conducted.| N/A| N/A| No change | N/A|
Reason : No GitHub Copilot findings were produced because a Copilot review was not conducted.	No Copilot suggestions were accepted or rejected.	The implementation was checked against the Stage 9 requirements and verified using the automated test suite and manual console tests.

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: The implementation was checked against the Stage 9 requirements. The query module contains the filtering and sorting logic, the service layer handles validation and access to the data store, and the console handles interaction with the user. The automated tests and manual checks were used to verify the implemented behaviour. A separate GitHub Copilot review remains outstanding.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? The main architectural concern was making sure the interactive console, services and data store all used the same shared application objects during one session. The console needed to call the service layer instead of implementing business rules itself. This ensured that appointments were stored, retrieved, cancelled and listed consistently.

2. Which Copilot suggestion did you reject as over-engineering, and why? Not applicable. GitHub Copilot was not used for a review, so no Copilot suggestions were received or rejected. I avoided claiming that a suggestion was rejected when no review took place.

3. How did you prove cancelled appointments remain retrievable and listable in the same session? I booked appointment A1 and then cancelled it using the interactive menu. I searched for A1 and confirmed that it was still available with its status changed to cancelled. I then listed all appointments for the practitioner and confirmed A1 appeared. When I filtered for scheduled appointments, A1 was excluded. Finally, I booked A3 in the same time slot and confirmed that A1 remained cancelled while A3 was scheduled.
## G. Ten formative answers


1. Why should query functions be pure?
Pure query functions are easier to test because they only use the information given to them. They do not change the original data or cause unexpected side effects.

2. Why should functions use explicit inputs instead of accessing a global data store?
Explicit inputs make the functions easier to understand, reuse and test. They also avoid hidden dependencies on other parts of the application.

3. Why should the query return the existing Appointment objects instead of creating new ones?
Returning the existing objects keeps the appointment information consistent. It also means the query does not create unnecessary copies or change the appointment data.

4. Why use a named sorting key?
A named sorting key makes the ordering rule clear and reusable. It sorts appointments by date and time first, then by appointment ID when two appointments have the same time.

5. What is the difference between the default status filter and an explicit status filter?
When no status is provided, the query returns appointments with all statuses. When a status is provided, it only returns appointments matching that status.

6. What is the difference between an empty result, an unknown practitioner and invalid input?
An empty result means the practitioner exists but has no matching appointments. An unknown practitioner means the ID does not exist. Invalid input means the supplied value is blank or has the wrong type or format.

7. How should the console handle errors?
The console should display a clear error message and return to the menu so the user can try again. It should not crash or unexpectedly change stored data.

8. How does the application protect data integrity?
The application uses the data store and service layer to manage appointments. It checks booking conflicts, validates inputs and changes an appointment's status to cancelled instead of deleting it.

9. Why is human verification important when using AI tools?
AI-generated suggestions should not automatically be trusted. Code needs to be checked against the assignment requirements and tested. For this Stage 9 implementation, GitHub Copilot was not used for a review, so no Copilot findings can be reported.

10. How do pure functions and object-oriented design work together?
Object-oriented design organises the application into classes with different responsibilities. Pure functions handle specific tasks such as filtering and sorting without changing the stored objects. Together, they make the application easier to maintain and test.

## H. Review, completion and common handover

Issues and bounded branches: Stage 9 implementation has been completed and tested locally. The Stage 8 branch was debug/stage08, with PR #8 previously approved and merged. The Stage 9 branch and pull request details still need to be confirmed.

PR/diff and another-member human reviewer: Stage 9 pull request and independent human reviewer details are pending. No independent review or approval is claimed at this stage.

Review responses and Copilot comparison:GitHub Copilot review was not conducted. No Copilot findings or comparison are available. The implementation was checked against the Stage 9 requirements and verified through automated tests and manual console testing.

Integrated common Stage 9 SHA: Pending confirmation of the final integrated Stage 9 commit on the common branch.

Full regression command, working directory, actual count/result and evidence: Command: python -m pytest -q
Working directory: C:\Users\Harle\PycharmProjects\st1-assignment--3\project
Actual result: 58 passed in 0.09 seconds.
Status: Passed.
Evidence: Test result observed in the PyCharm terminal. No separate test log was saved.

README run instructions and scope/limitations: project/README.md – includes installation instructions, demo and interactive run commands, test command, Stage 9 functionality and project limitations.

Unresolved issues and support/action: GitHub Copilot review, independent human review, final Stage 9 pull request approval and merge, and integrated common SHA confirmation remain outstanding. These need to be completed or confirmed before the common Stage 9 candidate is treated as final. The application uses in-memory storage only, so information is lost when the program exits.

UG common candidate / PG future branch plan: The Stage 9 implementation is intended to be the common candidate for the next stage. The UG progression is Stage 6 → 7 → 8 → 9 → 12. PG Stage 10 and Stage 11 work should be completed later on the approved branch without changing the protected common candidate. Mixed groups should use one repository and protect the common Stage 9 version.

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
