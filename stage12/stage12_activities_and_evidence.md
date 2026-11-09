# Stage 12 activities and evidence

BLANK student response template. Supplied from the beginning in stage12/ in your EXISTING repository; complete it only when you reach Stage 12 after the previous applicable stage is integrated, verified and recorded; preserve project/, tests, earlier records and Git history. UG/common and PG/extended scope must be explicit. Use concise results and versioned links, not copied logs or source. No staff answers or fabricated approvals.

Group/tutorial: [response]
Members and UG/PG applicability: [response]


## A Release scope and starting SHA

Group/tutorial: 4483 Software Technology 1 – Online Group 3, Tuesday 5:30–7:30 pm

Members and UG/PG applicability:
- Akshera Kandula – `aksherakandula-git` – UG
- Harleen Partola – `Harleenpartola` – UG

## A Release scope and starting SHA

- Starting branch: `main`
- Starting integrated SHA: `7fd1678247413101dc9075d8b49d4c3894867d06`
- Release owner: Akshera Kandula
- Applicable scope: Common UG release scope only.
- Previous checkpoint: Stage 9 completed, reviewed, integrated and verified on `main`.
- Initial repository state: Clean working tree; no unexpected unstaged or staged changes were present.
- Initial full regression command: `python3 -m pytest -q`
- Working directory: `project/`
- Initial regression result: 58 passed, 0 failed.
- Interactive application check: `python3 main.py --interactive` opened the SmartCare menu successfully.
- Release scope: Verify the completed SmartCare functionality for FR-01–FR-09, QRY-01–04, FP-01–03 and the required console/UI behaviours using the accumulated tests and release checks.
- Feature freeze decision: Optional feature development is frozen for Stage 12. Only genuine release blockers or necessary release/documentation corrections will be changed.
- PG-only Stage 10/11 scope: Not applicable to this UG-only group.


## B Requirements and release readiness matrix

## B Tutorial release readiness and evidence

### Activity 1 – Release readiness decision

Decision: **Release with conditions**

Although all tests are passing in the scenario, passing tests alone are not sufficient evidence for release. The README setup instructions are incomplete, one dependency has not been reviewed, and a known limitation has not been documented. These gaps affect reproducibility, maintainability and transparency.

Before final sign-off:
- complete and verify the README setup/run instructions;
- review the dependency and confirm its purpose/origin;
- document the known limitation clearly;
- rerun the release checks after any required correction.

The candidate should only be signed off once these release conditions have been addressed.

### Activity 2 – Evidence for release claims

| Claim | Evidence source/location | Reviewer/check | Sufficient? | Gap/action |
|---|---|---|---|---|
| Cancellation history works | `project/tests/test_regressions.py`, including `test_f8_02_cancelled_appointment_remains_available_in_store`, plus retained Stage 6/7 cancellation tests | Human review during Stage 8 and accumulated pytest regression suite | Yes for the stated course requirement | Release verification should rerun the accumulated suite and demonstrate retained CANCELLED history. |
| Architecture has appropriate responsibilities | `project/smartcare/domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` and associated tests | Human inspection of responsibilities and Stage 6–9 reviews | Yes for the course architecture | Recheck at release that no persistence layer, unrelated framework or responsibility leakage has been introduced. |
| Rescheduling is safe | PG-only requirement | Not applicable to this UG-only group | N/A | Stage 10/11 PG work is outside our applicable release scope. |
| AI use is responsible | Stage 7 and Stage 8 evidence records containing human-first analysis and Accept/Modify/Reject decisions | Human verification of AI suggestions against requirements, code and tests | Yes for recorded examples | Final release check must confirm no unexplained AI-generated changes, secrets, invented requirements or unsupported dependencies remain. |
| System is maintainable | Focused domain/service/query structure, descriptive tests, Stage 8 behaviour-preserving refactor and 58-test regression suite | Human code review and regression verification | Sufficient for the course release | Continue documenting known limitations and avoid unnecessary architecture or speculative features. |

### Activity 3 – Architecture and evidence discussion

**Why use one shared `SmartCareDataStore` with services and pure queries?**  
One shared `SmartCareDataStore` preserves the same in-session Patient, Practitioner and Appointment objects across the services. Services coordinate use cases such as registration, booking and cancellation, while pure query functions receive collections explicitly and return selected/sorted results without mutating the store. This keeps state management, workflows and query processing separated and easier to test.

**Evidence that a cancelled appointment remains retrievable:**  
`project/tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_available_in_store` books an appointment, cancels it, checks that its status is `AppointmentStatus.CANCELLED`, verifies that `find_appointment("A1")` returns the same appointment object, and confirms that the appointment remains in `list_appointments()`.

**Example of an AI-generated suggestion that was rejected or modified:**  
During Stage 7 testing, a proposed 30-minute appointment-overlap rule was rejected because FR-05 only defines a conflict for the same practitioner at the exact same datetime while the existing appointment is `SCHEDULED`. Adding an overlap rule would have invented behaviour not supported by the requirement. AI suggestions were therefore treated as candidates rather than requirements.

**One unresolved limitation:**  
SmartCare stores data only for the current session. Records are lost when the process ends. Persistent storage is deliberately outside the current revision 2 course scope.

**What would break if session-state lookup or query responsibilities changed?**  
If lookup stopped returning the actual objects held by the shared store, identity and retained-history behaviour could break. If query functions began mutating the store or performing service responsibilities, deterministic non-mutating query behaviour and the separation between storage, workflows and pure selection/sorting would be weakened.

## C Full regression results

| Suite/scope | Environment/version | Working directory and command | Tested SHA | Actual result |
|---|---|---|---|---|
| Complete common | Python 3.14.3; pytest 8.3.5 | `project/` — `python3 -m pytest -q` | `7fd1678247413101dc9075d8b49d4c3894867d06` | 58 passed, 0 failed |
| Complete PG if applicable | Not applicable — UG-only group | Not applicable | Not applicable | Not applicable |
| Affected focused checks after correction | No Stage 12 corrective code change required at this point | Not applicable | `7fd1678247413101dc9075d8b49d4c3894867d06` | No Stage 12 release defect identified requiring a focused correction |
| Full integrated recheck | Python 3.14.3; pytest 8.3.5 | `project/` — `python3 -m pytest -q` | `7fd1678247413101dc9075d8b49d4c3894867d06` | 58 passed, 0 failed |

Prior assertions preserved / reviewed test diff:
All accumulated Stage 6–9 tests were retained. No tests were removed or weakened for the Stage 12 release check.

Demo command:
`python3 main.py`

Interactive command:
`python3 main.py --interactive`

Interactive result:
SmartCare menu opened successfully and exited normally using option `0`.

Remaining failure / limitation:
No regression failures were observed. SmartCare remains session-only, so records are lost when the process exits.


## D Console and end to end demonstration

## D Console and end to end demonstration

| Demo step | Synthetic setup/input | Expected requirement | Observed result / evidence |
|---|---|---|---|
| Problem and stakeholders | SmartCare Community Clinic appointment workflow using synthetic patients, practitioners and appointments | Reception/admin staff need reliable registration, lookup, booking, cancellation and practitioner schedule information without duplicate/conflicting bookings | Demonstration used the completed SmartCare console with synthetic records only. |
| Register and find Patient and two Practitioners | Patient `P1` / Alex Example; practitioners `D1` / Dana Example / General Practice and `D2` / Sam Example / Cardiology | Registered participants can be created and subsequently found by their IDs | Patient and practitioners were registered and found successfully through the menu. |
| Valid booking | `A1`, patient `P1`, practitioner `D1`, `2026-10-01 09:00` | A valid appointment using registered participants and a free practitioner/time is stored as `SCHEDULED` | `A1` was booked successfully. |
| Same practitioner exact-time conflict rejected | Attempt `A_CONFLICT`, `P1`, `D1`, `2026-10-01 09:00` while `A1` was already SCHEDULED | FR-05 / AC-04.1 requires a second SCHEDULED appointment for the same practitioner at the exact same datetime to be rejected | Conflict booking was rejected and the session continued. Existing stored appointment state was preserved. |
| Different practitioner same time allowed | `A2`, `P1`, `D2`, `2026-10-01 09:00` | AC-04.2 permits another practitioner to have an appointment at the same datetime | `A2` was booked successfully for `D2` at the same time. |
| Cancel SCHEDULED and retain/find CANCELLED object | Cancel `A1`, then find `A1` | FR-06/FR-07 require cancellation to change status to `CANCELLED` while retaining appointment history; FR-08 supports lookup | `A1` was cancelled and remained findable with CANCELLED status. Same-object identity is additionally verified by the retained regression tests. |
| Invalid/repeated cancellation rejected | Attempt to cancel `A1` again | Repeated cancellation must raise/recover from the invalid transition without removing or mutating the retained history incorrectly | Repeated cancellation was rejected and the menu remained usable. |
| Freed slot reused | `A3`, `P1`, `D1`, `2026-10-01 09:00` after `A1` was cancelled | A CANCELLED appointment no longer occupies the practitioner/time conflict slot | `A3` was booked successfully for `D1` at the previously occupied time. |
| Default all-status listing | List practitioner `D1`, leave status blank | Default practitioner listing includes appointments of all statuses | Listing returned D1 appointments including retained CANCELLED history and the new SCHEDULED booking. |
| Explicit status filtering | List practitioner `D1`, status `scheduled` | An explicit status filter returns only appointments matching that status | Scheduled-only listing returned the current scheduled appointment(s) and excluded the cancelled appointment. |
| Unknown practitioner listing | List practitioner `D999`, blank status | A valid but unknown practitioner must be reported as absent and the console must recover | Unknown practitioner was rejected/reported and the menu continued normally. |
| Invalid menu choice | Enter menu option `99` | Unknown menu input must not crash the application | Invalid choice was handled and the menu was shown again. |
| Invalid date/time recovery | Attempt booking using `2026-02-30 09:00` | Malformed/impossible datetime input must be rejected without creating a partial booking | Invalid date was rejected and the menu continued operating. |
| Invalid listing status recovery | List `D1` using status `pending` | Only supported statuses (`scheduled`, `cancelled`, `completed`) are accepted | Invalid status was rejected and the console returned to the menu. |
| Session-only limitation and normal exit | Menu option `0` | Application exits normally and clearly states that session data is discarded | Console printed `Exiting SmartCare.` and `Session-only data: records are lost on exit.` |
| One meaningful requirement-linked pytest test | `project/tests/test_regressions.py::test_f8_02_cancelled_appointment_remains_available_in_store` | A meaningful test should demonstrate a specific requirement rather than only execute code | Test verifies cancellation retains the same appointment in the store with `CANCELLED` status; full accumulated suite also passed with 58 tests. |
| Architecture and one actual AI decision | Shared store + services + pure queries; Stage 7 overlap suggestion reviewed | Domain/store/service/query/console responsibilities remain separated; AI suggestions require human verification | Shared `SmartCareDataStore` retains session objects; services coordinate workflows; queries filter/sort without mutation; console handles interaction. A proposed 30-minute overlap rule was rejected because it was not supported by FR-05. |
| Known course-release limitation | Current-session storage only | Release limitations must be stated rather than hidden | SmartCare has no durable persistence: all records are lost when the process exits. |

Stable demo owner / fresh process / command:
Akshera Kandula; fresh SmartCare interactive session from `project/` using `python3 main.py --interactive`.

PG demonstrations through service/tests or not applicable:
Not applicable — UG-only group. Stage 10/11 PG rescheduling and assurance demonstrations are outside the applicable release scope.


## E Final code quality and AI review

### Code quality and architecture review

| Review area | Evidence / observation | Decision / outcome |
|---|---|---|
| Naming and formatting | Classes use PascalCase and functions/methods/variables use snake_case. Existing modules use readable imports, four-space indentation and focused methods. | No Stage 12 correction required. |
| Domain responsibility | `Patient` and `Practitioner` own validated entity data. `Appointment` and `AppointmentStatus` own appointment state and cancellation rules. | Responsibility remains appropriate; no change required. |
| Data-store responsibility | `SmartCareDataStore` retains the current-session Patient, Practitioner and Appointment objects and provides add/find/list/conflict operations. | Correct for the revision 2 session-only architecture; no persistence layer should be added. |
| Service responsibility | Services coordinate registration, lookup, booking, cancellation and practitioner-listing workflows using the shared store and domain objects. | No responsibility leakage requiring correction was identified. |
| Query responsibility | `appointment_sort_key` and `select_appointments` operate from explicit inputs and return selected/sorted results without taking over console or store responsibilities. | Keep as pure query functions; do not force them into classes. |
| Console responsibility | `console.py` handles menu input/output, parsing, display and recovery from expected user errors while delegating business behaviour to services/domain objects. | Appropriate separation maintained. |
| Dependencies | `requirements-dev.txt` uses the pinned pytest dependency (`pytest 8.3.5`). No new runtime framework, SQL/database layer or speculative dependency is required. | No additional dependency required for release. |
| Unnecessary architecture/features | No SQL persistence, repository abstraction, authentication framework or speculative Stage 12 feature is required by the current release scope. | Feature freeze maintained; no cosmetic redesign required. |
| Regression impact | Full accumulated suite on the integrated candidate reports 58 passed. | No behaviour-preserving Stage 12 code correction was required at this point. |

### Final AI-use review

| AI claim / suggestion | Affected requirement/code | Independent human check | Decision | Actual outcome |
|---|---|---|---|---|
| Proposed 30-minute appointment-overlap rule during Stage 7 test design | FR-05 / practitioner conflict behaviour | Checked the current requirement, which defines conflict for the same practitioner at the exact same datetime while SCHEDULED | Reject | No overlap rule was added because it would invent behaviour outside the approved requirement. |
| Candidate test for same-practitioner exact-time conflict | FR-05 / AC-04.1 | Compared the candidate with the requirement and verified it through the retained conflict tests | Accept | Requirement-linked test evidence was retained and continues to pass in the 58-test regression suite. |

Final responsible-AI conclusion:
AI/Copilot suggestions were treated as candidates rather than authoritative requirements. Significant suggestions were checked against the approved SmartCare requirements, actual code behaviour and test evidence before acceptance. Unsupported behaviour was rejected. No autonomous AI release decision was used.

Security/privacy/dependency check:
Only synthetic SmartCare data was used. No credentials, tokens, real patient information or confidential peer-assessment material were intentionally included in the application evidence. No AI-suggested unknown dependency was installed for the release.

Access route or approved equivalent / limitations:
GitHub Copilot or the teaching-team approved equivalent was used only as an engineering assistant for suggestions and review. No autonomous AI agent or AI release approval was used. Final decisions were made and verified by the group using requirements, code review and test evidence.

Available AI evidence and missing evidence honestly disclosed:
Available evidence includes the recorded Stage 7 test-design suggestions and Accept/Modify/Reject decisions, plus Stage 8 debugging/review decisions and their human verification. The release evidence relies on the recorded prompts, decisions and verification already retained in the project.


## F README and reproducibility check

| README item | Location | Verifier | Result/gap |
|---|---|---|---|
| Purpose and included common/PG scope | [response] | [response] | [response] |
| Out-of-scope capabilities and known limitations | [response] | [response] | [response] |
| Confirmed teaching Python version and dependency installation | [response] | [response] | [response] |
| Working directory / demo / interactive / test commands | [response] | [response] | [response] |
| Repository structure and architecture responsibilities | [response] | [response] | [response] |
| Responsible AI summary / synthetic-data rule | [response] | [response] | [response] |
| Release label/version and SHA links | [response] | [response] | [response] |
Root README index and project/README verified: [response]
Fresh clone or extracted ZIP / candidate identity: [response]
Verifier and clean environment / actual version: [response]
Setup/run/test commands and observed results: [response]
Missing local file or setup gap / remedy and recheck: [response]


## G Known limitations debt and release notes

Delivered features: [response]
Important fixes: [response]
Architecture/quality improvements: [response]
Known limitations: [response]
AI-assisted development note: [response]

| Debt item | Impact | Priority | Future action | Accepted? / release rationale |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |
Session-only synthetic data and minute-precision local time: [response]
Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions: [response]
Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations: [response]
Difference between accepted scope limit and unresolved required behaviour: [response]
PG assurance residual risks / owner / status or not applicable: [response]


## H Release findings and corrective action

| Requirement/claim | Reproduction/observation | Impact/severity | Owner/action | Corrective diff | Focused/full recheck | Residual limit |
|---|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] | [response] |
Justified no-change conclusion if no defect found: [response]
Release blockers still open / status: [response]


## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA: [response]
Independent reviewer / feedback / response: [response]
Integration commit / full recheck: [response]
Tracked and untracked file inspection / cleanliness: [response]
Secrets/staff material/caches/tool-metadata exclusion check: [response]
Candidate recovery plan / known-good SHA: [response]
Named substantive contributions: [response]


## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY: [response]
Approver / date / rationale and evidence: [response]
What risks remain / conditions / owners: [response]
Can the team explain the system: [response]
Can a change be recovered: [response]
Common decision / PG decision where different: [response]


## K Final tested release SHA

Exact common tested SHA: [response]
Exact PG tested SHA or not applicable: [response]
Final submitted SHA / repository URL: [response]
Evidence-only later commit and difference explanation: [response]
Executable changes after testing and re-verification: [response]
Source ZIP name / SHA correspondence / extracted comparison: [response]


## L Submission package verification

- [ ] Feature freeze and scoped requirements traced.
- [ ] Applicable full regressions, integrated demo and invalid paths verified.
- [ ] Architecture/code quality and final AI/dependency checks complete.
- [ ] Root README and project/README reproduced by another verifier.
- [ ] Release notes, technical debt and limitations visible.
- [ ] Independent human review, integration and release decision recorded.
- [ ] Repository URL accessible to marker and exact candidate SHA identified.
- [ ] One source ZIP from submitted commit with root README.md and .gitignore.
- [ ] project/ source and all accumulated applicable tests included.
- [ ] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [ ] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [ ] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [ ] Mixed-group common protection and candidate upload routing checked.
- [ ] Group reflection, confidential individual peer forms and common team viva routed separately.

Confirmed assessment item/upload route: [response]
Deadline/timezone: [response]
Repository access arrangement: [response]
Mixed-candidate upload arrangement: [response]
Oral/video recording/accessibility arrangements: [response]
Remaining administration or release dependency: [response]


## M Formative questions

1. What is a release candidate? [response]

2. What is feature freeze and why is it used? [response]

3. What is regression testing in a release context? [response]

4. What is a known limitation? [response]

5. What is technical debt? [response]

6. What are release notes? [response]

7. What is software maintenance? [response]

8. What is the purpose of the individual demonstration/viva? [response]

9. What should the final responsible-AI check establish before release? [response]

10. What is the main course conclusion about AI and the role of the software engineer? [response]


## N Reflection viva and handover

Strongest evidence SmartCare is ready: [response]
Weakest area: [response]
How AI use changed from Stage 1 to Stage 12: [response]
Start doing — engineering and AI use: [response]
Stop doing — engineering and AI use: [response]
Continue doing — engineering and AI use: [response]
What worked / caused rework / future delivery improvement: [response]
One paragraph — If AI can write code why do we still need software engineers: [response]

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | [response] |
| Two requirements and acceptance criteria | [response] |
| Domain model and architecture | [response] |
| Design trade-off | [response] |
| Meaningful test and its limits / 100 percent coverage | [response] |
| Diagnosed defect and verification | [response] |
| Shared store and session-state/query responsibilities | [response] |
| What would break if session-state lookup/query responsibilities changed? | [response] |
| Why cancellation is domain behaviour / conflict coordination is service behaviour | [response] |
| FR-07 retained history test | [response] |
| Actual AI change rejected/modified or honestly accepted with verification | [response] |
| Unresolved limitation / future production work | [response] |
| Personal implementation contribution | [response] |
| Personal test/review/design/integration contribution | [response] |
| PG agentic change and rescheduling verification | [response] |
| PG responsible-AI risk/remediation or supported no finding | [response] |

Optional bounded-change practice only: validation rule, focused test, safe error-message change, explicit-input query or agreed status rule with test. Explain expected impact before editing, make a small change, run the test, and identify evidence to inspect if unsure. No live AI unless explicitly permitted. Preserve the submitted candidate.

Practice question/change and reasoning: [response or not undertaken]
Separate reflection / peer / common team viva evidence links and routing: [response]
No further coding stage. Later corrections use the published assessment process.
