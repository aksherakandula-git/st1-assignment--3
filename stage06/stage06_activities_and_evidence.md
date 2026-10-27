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
- Actual issue link: [response]

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Implement FR-06 appointment cancellation with FR-07 retained history
- Context: The Appointment domain object already provides guarded cancellation, but AppointmentService.cancel_appointment is currently incomplete. The service must coordinate cancellation while retaining the same appointment object in the shared session history.
- Requirement: FR-06 Appointment Cancellation together with FR-07 Retained Appointment History.
- Acceptance criteria: Cancelling a stored SCHEDULED appointment changes that same object's status to CANCELLED, returns the same object and keeps it retrievable from the store. Repeated cancellation and cancellation of a COMPLETED appointment raise ValueError without changing state. A valid but unknown appointment ID raises LookupError, while a blank or invalid ID raises ValueError.
- Scope: Implement only the Stage 6 appointment cancellation service workflow and focused tests. Do not delete appointments, directly change protected state, create replacement appointments, add notifications, add rescheduling or implement Stage 9 functionality.
- Definition of Done: Cancellation uses the supplied Appointment.cancel() domain transition; object identity, CANCELLED status and retained history are demonstrated; successful and rejected operations are meaningfully tested; existing behaviour remains passing; another team member reviews the change; feedback is resolved; and the reviewed change is merged and verified on main.
- Owner: Akshera Kandula — aksherakandula-git
- Actual issue link: [response]

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
| Branch naming | [response] |
| Commit message convention | [response] |
| PR size | [response] |
| Another-member review requirement | [response] |
| Merge rule | [response] |
| Significant Copilot disclosure rule | [response] |

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| [issue 1] | [response] | [response] | [response] | [response] |
| [issue 2] | [response] | [response] | [response] | [response] |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: [response]
- Linked issue and requirement: [response]
- Feature branch: [response]
- Changed behaviour: [response]
- Meaningful commits: [links]
- Test command, directory and observed result: [response]
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: [response]
- Implementation: [work and evidence]
- Testing: [work and evidence]
- Review: [work and evidence]
- Issue refinement: [work and evidence]
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

[response]

## L Stage 6 formative questions

1. What is version control?

[response]

2. Why is a feature branch useful?

[response]

3. What makes a commit a good engineering commit?

[response]

4. What is a pull request?

[response]

5. What is the purpose of code review?

[response]

6. What does a Git diff show?

[response]

7. What is a Definition of Done?

[response]

8. What is the appropriate role of GitHub Copilot in pull-request review?

[response]

9. Why should individual contribution not be judged only by commit count?

[response]

10. What is the Stage 6 engineering rule?

[response]

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
