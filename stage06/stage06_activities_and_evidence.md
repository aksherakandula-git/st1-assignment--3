# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: [4483 Software Technology 1 – Online Group 3, Tuesday 5:30–7:30 pm]
- Members, GitHub usernames and cohorts: [Akshera Kandula – aksherakandula-git – UG; Harleen Partola – Harleenpartola – UG]
- Repository URL: [https://github.com/aksherakandula-git/st1-assignment--3]
- Starting SHA: [db5f939e1ca707e4cbe5cce43d4127da61f705f]

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Implement FR-02 patient search by ID
- Context: SmartCare can register patients, but PatientService.find_patient is currently incomplete. The service needs to retrieve a registered patient from the shared session store using the patient ID while preserving the supplied validation and object identity rules.
- Requirement: FR-02 Patient Search — allow a registered patient to be retrieved by patient ID through PatientService.
- Acceptance criteria: A known valid patient ID returns the actual registered Patient object. Surrounding whitespace is trimmed and IDs remain case-sensitive. A valid but unknown ID raises LookupError, while a blank or invalid ID raises ValueError. Lookup must not create or replace a patient.
- Scope: Implement PatientService.find_patient and focused tests only. Do not add name searching, fuzzy searching, persistence, authentication, console changes or Stage 9 functionality.
- Definition of Done: The lookup satisfies the published service contract; known, unknown, trimmed, case-sensitive and invalid ID behaviour is meaningfully tested; existing tests continue to pass; the work is reviewed by another team member; feedback is resolved; and the reviewed change is merged and verified on main.
- Owner: Akshera Kandula — aksherakandula-git
- Actual issue link: https://github.com/aksherakandula-git/st1-assignment--3/issues/1

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Implement FR-06 appointment cancellation with FR-07 retained history
- Context: The Appointment domain object already provides guarded cancellation, but AppointmentService.cancel_appointment is currently incomplete. The service must coordinate cancellation while retaining the same appointment object in the shared session history.
- Requirement: FR-06 Appointment Cancellation together with FR-07 Retained Appointment History.
- Acceptance criteria: Cancelling a stored SCHEDULED appointment changes that same object's status to CANCELLED, returns the same object and keeps it retrievable from the store. Repeated cancellation and cancellation of a COMPLETED appointment raise ValueError without changing state. A valid but unknown appointment ID raises LookupError, while a blank or invalid ID raises ValueError.
- Scope: Implement only the Stage 6 appointment cancellation service workflow and focused tests. Do not delete appointments, directly change protected state, create replacement appointments, add notifications, add rescheduling or implement Stage 9 functionality.
- Definition of Done: Cancellation uses the supplied Appointment.cancel() domain transition; object identity, CANCELLED status and retained history are demonstrated; successful and rejected operations are meaningfully tested; existing behaviour remains passing; another team member reviews the change; feedback is resolved; and the reviewed change is merged and verified on main.
- Owner: Akshera Kandula — aksherakandula-git
- Actual issue link: https://github.com/aksherakandula-git/st1-assignment--3/issues/3

## B Commit quality
| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | Weak | This is too vague because it does not explain what behaviour or part of the system changed. |
| final version | Weak | This does not describe the engineering change and gives a reviewer no useful information about the commit. |
| Add patient search by ID | Strong | This clearly identifies the behaviour implemented and gives the commit a focused purpose. |
| fix stuff | Weak | This is vague and does not identify what problem was fixed or which behaviour changed. |
| Prevent cancellation of completed appointments | Strong | This describes a specific behavioural rule being enforced and clearly communicates the purpose of the change. |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: The PR should focus on appointment cancellation. Renaming unrelated patient fields, restructuring unrelated code and adding a new dependency unnecessarily increases the scope and makes the cancellation change harder to review against FR-06 and FR-07.

- Responsibility and architecture concerns: `AppointmentService` should coordinate the cancellation workflow while the `Appointment` domain object remains responsible for its state transition. Unrelated restructuring could blur these responsibilities and introduce unnecessary coupling.

- Testing and review concerns: A passing test suite alone does not prove that all unrelated changes are correct or necessary. The cancellation change needs focused evidence for successful cancellation, retained history, illegal state transitions, invalid and unknown IDs, and unchanged state after rejected operations.

- Changes to remove or separate, with reasons: The unrelated patient-field renaming, unrelated restructuring and new dependency should be removed from this PR. If any of these changes are genuinely required, they should have their own issue, focused branch, tests and PR so they can be reviewed independently.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: The statement "Looks good; tests pass" does not show which requirement or acceptance criteria were checked, what changed in the actual diff, whether SmartCare responsibility boundaries were preserved, whether the test assertions meaningfully verify the required behaviour, whether unrelated changes were introduced, or what test command and result were actually observed.

- Follow-up review question 1: Which changed lines satisfy each linked requirement and acceptance criterion?

- Follow-up review question 2: Do the tests verify the required object identity, state, retained history and documented exception behaviour rather than only checking that an object exists?

- Follow-up review question 3: Does the implementation preserve SmartCare's responsibility boundaries, with services coordinating workflows, the store retaining objects and `Appointment` controlling its own state transition?

- Follow-up review question 4: Does the diff contain unrelated changes, new dependencies or unnecessary architectural changes that should be removed or moved to another PR?

- Follow-up review question 5: What exact test command and observed result provide evidence that both the focused behaviour and the full regression suite pass?

- Additional question: What required behaviour remains untested or uncertain even if the current tests pass?

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | Use focused branch names such as `feature/fr02-service-lookups` and `feature/fr06-cancellation`. |
| Commit message convention | Use short, meaningful behaviour-focused messages such as `Add patient lookup by ID` or `Implement guarded appointment cancellation`. |
| PR size | Keep each PR focused on one behaviour or closely related change. Unrelated refactoring, dependencies or features should be separated into another issue and PR. |
| Another-member review requirement | A different group member must review each PR before merge. Self-review may be used as preparation but does not replace independent review. |
| Merge rule | Merge only after the linked acceptance criteria are satisfied, focused and full tests pass, reviewer feedback is resolved and another group member has approved the PR. |
| Significant Copilot disclosure rule | Record significant GitHub Copilot assistance, its purpose, the output considered, the human verification performed and whether the suggestion was accepted, modified or rejected. Do not claim Copilot ran tests unless the tests were independently executed and observed. |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|--|---|---|---|---|
| https://github.com/aksherakandula-git/st1-assignment--3/issues/1 | FR-02 Patient Search | Akshera Kandula — aksherakandula-git | Known valid ID returns the actual stored `Patient`; surrounding whitespace is trimmed; IDs remain case-sensitive; valid unknown ID raises `LookupError`; blank or invalid ID raises `ValueError`. | Open |
| https://github.com/aksherakandula-git/st1-assignment--3/issues/2 | Supporting practitioner lookup for Stage 6 / FR-03 registered practitioners | Akshera Kandula — aksherakandula-git | Known valid ID returns the actual stored `Practitioner`; surrounding whitespace is trimmed; IDs remain case-sensitive; valid unknown ID raises `LookupError`; blank or invalid ID raises `ValueError`. | Open |
| https://github.com/aksherakandula-git/st1-assignment--3/issues/3 | FR-06 Appointment Cancellation / FR-07 Retained History | Akshera Kandula — aksherakandula-git | A stored `SCHEDULED` appointment changes to `CANCELLED` using the domain transition, the same object is returned and retained, and illegal transitions or invalid/unknown IDs are rejected according to the contract. | Open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/aksherakandula-git/st1-assignment--3/pull/4 — Complete Stage 6 service operations and tests
- Linked issue and requirement: Issues #1, #2 and #3 — FR-02 Patient Search; supporting Stage 6 practitioner lookup over FR-03 registered practitioners; FR-06 Appointment Cancellation; FR-07 Retained Appointment History
- Feature branch: `feature/fr02-service-lookups`
- Changed behaviour: Implemented patient lookup, practitioner lookup and appointment cancellation. Lookups return the actual registered objects and distinguish invalid IDs from valid unknown IDs. Cancellation uses `Appointment.cancel()`, returns the same appointment object, changes `SCHEDULED` to `CANCELLED`, retains history and rejects illegal transitions without mutation.
- Meaningful commits: Commit `e7c567f` — Complete Stage 6 service operations and tests
- Test command, directory and observed result: From `project/`, ran `python3 -m pytest tests/test_services.py -v` and `python3 -m pytest`. Focused Stage 6 service tests passed and the full regression suite reported 19 passed.
- Another-member reviewer: Harleen Partola — Harleenpartola
- Human observations recorded before Copilot: Harleen reviewed PR #4 before the Copilot comparison and inspected the actual changed code and tests.
- Requirement, responsibilities, test assertions and unrelated-scope checks: Human review confirmed that patient and practitioner lookup return the registered objects, appointment cancellation delegates to `Appointment.cancel()`, cancelled appointments remain stored, tests check identity/state/errors/state preservation, and no unrelated Stage 9 changes were identified.
- Key feedback: Harleen found the implementation consistent with the Stage 6 requirements and responsibility boundaries. Her written review did not identify a specific code defect or required implementation change.
- Author response/change and verification: No code change made at this point because the human review did not identify a concrete implementation defect. Existing focused and full regression results remain the current verification evidence.
- Reviewer recheck and approval: Pending after Copilot comparison and final recheck.
- Merge outcome and SHA: Pending.
- Significant Copilot assistance: Pending required Copilot comparison.
- Linked issue closure: Pending merge.
- Each member updated main: Pending merge.
- Integrated verification after merge: Pending merge.

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task:  Akshera Kandula — Copilot review of Stage 6 PR #4
- Prompt/purpose and relevant issue/diff: Review PR #4 against FR-02 Patient Search, the supporting practitioner lookup contract, FR-06 Appointment Cancellation and FR-07 Retained History. Check correctness, SmartCare responsibility boundaries, assertion quality, error handling, unrelated scope and maintainability.
- Summary of output: The copilot review found no critical or important correctness defect. It confirmed that lookups return the stored objects, cancellation delegates to `Appointment.cancel()`, cancelled history is retained, meaningful assertions are present and no unrelated Stage 9 work was identified. It raised only an optional maintainability observation that the completed lookup docstrings still contain starter/TODO wording.
- Human check against actual code, requirements and tests: I checked the copilot comments against the actual PR diff, the Stage 6 contracts, Harleen's independent human review and the observed test results. The implementation matches the required behaviour and the optional docstring observation does not affect the published Stage 6 behaviour.
- Decision — Accept / Modify / Reject: Accept
- Reason: The copilot review was consistent with the actual implementation and human review. No functional defect requiring a production-code change was identified. The optional documentation observation was noted but is not required to satisfy the Stage 6 acceptance criteria.
- Verification/evidence: PR #4 — https://github.com/aksherakandula-git/st1-assignment--3/pull/4. Focused Stage 6 service tests passed and the full regression suite reported 19 passed.

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: Harleen independently verified that patient and practitioner lookup return the stored registered objects, unknown IDs are handled correctly, appointment cancellation uses `Appointment.cancel()`, cancelled appointments remain in the data store, tests cover object identity, state transitions, exception handling and unchanged state after rejected operations, and no unrelated Stage 9 changes were present.
- Copilot noticed: The tutor-approved AI review reached the same overall conclusion. It found no critical or important correctness issue, confirmed the service/domain responsibility boundaries and meaningful test assertions, and additionally noted an optional maintainability issue that the completed lookup docstrings still contain starter/TODO wording.
- Overlap: Both reviews agreed that the lookup operations preserve registered-object identity, cancellation correctly delegates to the domain transition, retained history is preserved, the tests meaningfully verify the required behaviour and no unrelated Stage 9 work was introduced.
- What did the human reviewer notice that Copilot did not: The human review directly inspected the actual changed lines in GitHub and specifically confirmed the implemented patient, practitioner and cancellation changes against the PR diff.
- What did Copilot identify that the human reviewer initially missed: The AI review identified the optional maintainability concern that the lookup docstrings still contain starter/TODO wording even though the methods are now implemented.
- Unsupported or incorrect Copilot suggestion: None identified. The optional docstring observation was valid but was not a requirement-level defect.
- Human judgement accepted, modified or rejected, and why: The AI review was accepted as supporting evidence because its conclusions matched the actual code, published requirements, Harleen's independent review and the observed tests. No production-code change was required from the AI review.
- Which evidence justified merge approval: The linked requirements and acceptance criteria, the actual PR diff, Harleen's independent review, meaningful identity/state/error assertions, focused Stage 6 service tests and the full regression suite reporting 19 passed.

## J Contributions

### Akshera Kandula

- Member: Akshera Kandula — `aksherakandula-git`
- Implementation: Implemented the three Stage 6 service operations in `project/smartcare/services.py`: patient lookup, practitioner lookup and appointment cancellation. The lookup services use the existing `SmartCareDataStore`, while cancellation delegates the state transition to `Appointment.cancel()`.
- Testing: Created and developed `project/tests/test_services.py`. Added lookup tests for registered-object identity, trimming, case sensitivity, unknown IDs and invalid IDs. Added cancellation tests for same-object return, `CANCELLED` status, retained history, repeated cancellation, `COMPLETED` cancellation, unknown IDs and blank IDs. Final integrated regression suite reported 19 passed.
- Review: Prepared PR #4 and PR #5 for another-member review, responded to the review process and verified the reviewed changes before integration.
- Issue refinement: Created and documented GitHub Issues #1, #2 and #3 with requirements, acceptance criteria, scope and Definition of Done for patient lookup, practitioner lookup and appointment cancellation/retained history.
- Design and responsibility discussion: Preserved the supplied SmartCare responsibility boundaries by keeping storage and lookup behaviour in `SmartCareDataStore`, workflow coordination in services and appointment state transitions in the `Appointment` domain object.
- Debugging or integration: Identified that cancellation tests were initially not collected because they were incorrectly nested. Corrected the test structure, reran the focused and full suites, added the cancellation regression-test PR and verified the final integrated result on `main`.
- Documentation or team support: Completed the Stage 6 activity/evidence record, documented the human-versus-Copilot review comparison and coordinated the final review and verification steps with Harleen.

### Harleen Partola

- Member: Harleen Partola — `Harleenpartola`
- Implementation: Not applicable for the Stage 6 implementation owned by Akshera.
- Testing: Reviewed the Stage 6 test changes, including identity, cancellation state, exception handling and state-preservation checks. Final independent `main` verification will be recorded in Section M when completed.
- Review: Independently reviewed the actual PR #4 diff before the Copilot comparison, checking the patient and practitioner lookup implementations, `Appointment.cancel()` usage, retained history, assertion quality, exception handling and unrelated scope. Also reviewed and approved the follow-up cancellation regression-test PR #5.
- Issue refinement: Not applicable.
- Design and responsibility discussion: Confirmed during review that the implementation preserves the existing service/domain responsibility boundaries and does not introduce unrelated Stage 9 functionality.
- Debugging or integration: Supported integration by reviewing the corrected Stage 6 changes before merge.
- Documentation or team support: Provided independent human review evidence and approval required for Stage 6 integration.

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high commit count does not necessarily show strong contribution because commits can be very small, repetitive or poorly scoped. One coherent commit can represent substantial implementation and testing work, while another team member may contribute through requirement analysis, debugging, code review, testing, integration or team support without producing many commits. Contribution should therefore be judged by the quality, relevance and verified impact of the work rather than the number of commits alone.

## L Stage 6 formative questions

### 1. What is version control?

Version control is a system for recording and managing changes to project files over time. It allows a team to track who changed what, return to earlier versions and collaborate on the same project while preserving a history of the work.

### 2. Why is a feature branch useful?

A feature branch allows a focused change to be developed separately from the stable `main` branch. This lets the developer implement and test the change without disrupting integrated working code, and the branch can then be reviewed through a pull request before merging.

### 3. What makes a commit a good engineering commit?

A good engineering commit contains one coherent and meaningful change and has a message that clearly explains the behaviour or purpose of that change. It should avoid unrelated modifications and leave useful history for reviewers and future developers.

### 4. What is a pull request?

A pull request proposes integrating changes from one branch into another, usually into `main`. It exposes the diff so another team member can review the implementation, requirements, tests, scope and code quality before the change is merged.

### 5. What is the purpose of code review?

Code review provides an independent check of a proposed change before integration. It can identify defects, weak tests, responsibility violations, unrelated changes or maintainability concerns and helps confirm that the implementation satisfies its requirement and acceptance criteria.

### 6. What does a Git diff show?

A Git diff shows the changes between two versions of files, such as lines that were added, removed or modified. It allows a reviewer to inspect exactly what a branch or commit changes rather than reviewing the whole project again.

### 7. What is a Definition of Done?

A Definition of Done is the shared set of conditions that must be satisfied before work is considered complete. In Stage 6, this goes beyond writing code and includes meeting the requirement, meaningful testing, human review, resolving feedback, integration and appropriate evidence/documentation.

### 8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot can assist by identifying possible correctness risks, weak tests, responsibility issues, unrelated changes or maintainability concerns. Its output is supporting evidence only. A human must independently review the actual diff first, verify Copilot's suggestions against the requirements, code and observed tests, and decide whether to accept, modify or reject them.

### 9. Why should individual contribution not be judged only by commit count?

Commit count does not measure the difficulty or quality of work. Important contribution can include implementation, test design, debugging, reviewing another member's code, refining requirements, integration, documentation and mentoring. Contribution should be based on observable engineering value and follow-through rather than a raw number of commits.

### 10. What is the Stage 6 engineering rule?

The Stage 6 engineering rule is to take a requirement through a focused and reviewable engineering workflow: link it to an issue and observable acceptance criteria, develop it on a focused branch, implement only the required behaviour, verify it with meaningful tests, obtain independent human review, resolve feedback and integrate the verified change into stable `main` while preserving the supplied responsibility boundaries.

## M Completion and handover

- Starting SHA: [response]
- Final Stage 6 code SHA: [response]
- Test command: [response]
- Working directory: [response]
- Observed result: [response]
- PR and another-member reviewer: [links]
- Unresolved issue or none: [response]
- Stage 7 handover status: [ready for tutor checkpoint / unresolved work]
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [ ] Three Stage 6 service targets completed and checked.
- [ ] Original supplied tests retained and passing.
- [ ] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
