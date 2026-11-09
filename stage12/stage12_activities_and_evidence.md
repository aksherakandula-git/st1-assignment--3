# Stage 12 activities and evidence

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
| Purpose and included common/PG scope | Root `README.md` and `project/README.md` | Akshera Kandula; Harleen Partola | Common UG release scope is documented, covering completed Stage 6–9 SmartCare functionality. Stage 10 and Stage 11 PG work is not applicable to this UG-only group. |
| Out-of-scope capabilities and known limitations | Root `README.md` and `project/README.md` | Akshera Kandula; Harleen Partola | Session-only storage and out-of-scope production capabilities are documented. Records are lost when the process exits; durable persistence and production-only capabilities are outside the current course-release scope. |
| Confirmed teaching Python version and dependency installation | Root `README.md`, `project/README.md`, `project/requirements-dev.txt` | Akshera Kandula; Harleen Partola | The documented teaching baseline is Python 3.13 with pytest 8.3.5. `requirements-dev.txt` pins `pytest==8.3.5`. Stage 12 verification also succeeded using Python 3.14 environments. |
| Working directory / demo / interactive / test commands | Root `README.md` and `project/README.md` | Akshera Kandula; Harleen Partola | `project/` is documented as the application working directory. `python main.py`, `python main.py --interactive` and `python -m pytest -q` are documented and were successfully followed during fresh-copy verification. |
| Repository structure and architecture responsibilities | `project/README.md` | Akshera Kandula; Harleen Partola | Responsibilities for `domain.py`, `data_store.py`, `services.py`, `queries.py`, `console.py` and `main.py` are documented consistently with the implemented architecture. |
| Responsible AI summary / synthetic-data rule | Root `README.md` and Stage 12 evidence | Akshera Kandula; Harleen Partola | README documents responsible AI use and the synthetic-data rule. AI/Copilot suggestions require human verification and no autonomous AI release approval is claimed. |
| Release label/version and SHA links | Root `README.md` and Stage 12 evidence | Akshera Kandula; Harleen Partola | Stage 12 candidate branch `feature/stage12-release` was independently verified at SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`. Final submitted SHA will be recorded in Section K after final integration. |

Root README index and `project/README` verified:
Yes. Both README files were reviewed and updated with the Stage 12 release scope, setup/run/test commands, architecture responsibilities, responsible-AI summary, synthetic-data rule and known limitations.

Fresh clone or extracted ZIP / candidate identity:
Harleen Partola created a fresh clone of the shared GitHub repository in a separate directory, switched to `feature/stage12-release`, confirmed a clean working tree with `git status --short`, and verified candidate SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`.

Verifier and clean environment / actual version:
Harleen Partola independently performed the verification from a fresh Windows clone. Her environment showed Python 3.14 64-bit with pytest 8.3.5 available. The verification did not rely on her existing project working copy or local changes.

Setup/run/test commands and observed results:
Harleen successfully ran `python -m pip install -r requirements-dev.txt`, `python main.py`, `python main.py --interactive` and exited normally using option `0`, then ran `python -m pytest -q`. The complete regression result was 58 passed in 0.12s.

Missing local file or setup gap / remedy and recheck:
No missing local file, additional setup requirement or release-blocking reproducibility gap was observed during the fresh-copy verification. No corrective action was required.

Session-only synthetic data and minute-precision local time:
SmartCare uses synthetic data only. Data exists only for the current application session and is lost when the process exits. Appointment datetimes use local naive date/time values at minute precision; persistent storage and timezone conversion are not implemented.

Production auth/roles, portal, notifications, billing/insurance, clinical AI exclusions:
These capabilities are outside the current course-release scope. SmartCare does not provide production authentication or role management, a patient portal, SMS/email notifications, billing or insurance processing, clinical decision support, or clinical AI functionality.

Scale/concurrency, timezone policy, operations/monitoring, accessibility/usability limitations:
The course release has not been designed or evaluated for enterprise-scale concurrency, multi-user deployment, formal timezone handling, production operations/monitoring, or formal accessibility/usability compliance. These are documented limitations rather than claims of production readiness.

Difference between accepted scope limit and unresolved required behaviour:
An accepted scope limitation is functionality deliberately excluded by the current revision 2 requirements, such as durable persistence or production authentication. Unresolved required behaviour would be a failure to satisfy an applicable FR, QRY, FP or UI requirement. No unresolved required UG behaviour was identified during the Stage 12 regression, demonstration and fresh-copy verification checks.

PG assurance residual risks / owner / status or not applicable:
Not applicable — this is a UG-only group. Stage 10 rescheduling and Stage 11 PG assurance requirements are outside the applicable release scope.


## G Known limitations debt and release notes

### Release notes

Delivered features:
- Patient registration and lookup.
- Practitioner registration and lookup.
- Appointment booking and lookup.
- Rejection of a second `SCHEDULED` appointment for the same practitioner at the exact same datetime.
- Allowing a different practitioner to be booked at the same datetime.
- Appointment cancellation while retaining cancelled appointment history.
- Rejection of repeated or invalid cancellation.
- Practitioner appointment listing with optional status filtering.
- Deterministic appointment ordering by date/time and then appointment ID.
- Interactive console with recovery from invalid menu, date, status and lookup input.
- Current-session SmartCare data using synthetic records only.

Important fixes:
- Stage 8 practitioner-conflict behaviour was corrected and regression-tested.
- Stage 8 cancelled-appointment history/lookup behaviour was corrected so cancelled appointments remain stored and retrievable.
- A review concern involving comparison with the string `"scheduled"` was corrected to use `AppointmentStatus.SCHEDULED`.
- Stage 9 integrated the query and practitioner-listing behaviour with the console and service layer.

Architecture and quality improvements:
- `Patient`, `Practitioner`, `Appointment` and `AppointmentStatus` retain domain responsibilities.
- One shared `SmartCareDataStore` maintains consistent current-session objects across services.
- Services coordinate workflows without taking over console responsibilities.
- `appointment_sort_key` and `select_appointments` remain reusable explicit-input query functions.
- Regression tests from earlier stages were retained rather than weakened or replaced.
- Stage 12 release verification completed with 58 passing tests and independent fresh-clone verification.

Known limitations:
- SmartCare stores data only for the current process; records are lost on exit.
- Appointment datetimes are local naive values at minute precision and no timezone policy is implemented.
- Production authentication/roles, patient portal, notifications, billing/insurance and clinical decision support are outside the current course scope.
- The application has not been evaluated for enterprise-scale concurrency, production monitoring, formal accessibility or production healthcare/security certification.
- Stage 10 rescheduling and Stage 11 PG assurance work are not applicable to this UG-only group.

AI-assisted development note:
AI/Copilot was used as an engineering assistant for selected test-design, debugging and review activities. Suggestions were checked by the group against the approved requirements, code and observed test results before being accepted, modified or rejected. For example, a proposed 30-minute overlap rule was rejected because FR-05 specifies an exact same-practitioner/date-time conflict rather than an appointment-duration overlap rule. Human reviewers remained responsible for implementation and release decisions.

### Technical debt

| Debt item | Impact | Priority | Future action | Accepted? |
|---|---|---|---|---|
| Session-only in-memory storage | Data is lost when the application exits, so the system cannot retain records between sessions. | Medium | If future requirements introduce durable storage, design and verify an appropriate persistence solution without changing current behaviour unexpectedly. | Yes — persistence is outside the current revision 2 scope. |
| No explicit timezone policy | Local naive appointment datetimes may become ambiguous if the application is extended across locations or timezones. | Low | Define timezone requirements and use timezone-aware datetime handling if future deployment requires it. | Yes — not required for the current course release. |
| No production authentication or role control | A real deployed healthcare application would require access control and user accountability. | High for production; not applicable to course scope | Define user roles, authentication and authorisation requirements before any real deployment. | Yes — accepted as an out-of-scope production limitation. |
| No enterprise concurrency or persistence testing | Current tests establish the single-process course workflows but do not establish safe multi-user/enterprise behaviour. | Medium for future deployment | Add concurrency, persistent-storage and integration testing if the application scope expands. | Yes — outside the current course release. |
| No formal accessibility/usability evaluation | Console behaviour has been functionally tested but not formally evaluated against accessibility/usability standards. | Medium for future user-facing deployment | Conduct structured accessibility and usability evaluation before a production-facing release. | Yes — accepted as future work. |

Technical-debt conclusion:
The items above are accepted future-work or production-readiness limitations rather than failures of the current UG requirements. No known unmet FR, QRY, FP or UI requirement has been reclassified as technical debt.

## H Release findings and corrective action

| Requirement / claim | Reproducible observation | Impact / severity | Owner | Action | Corrective diff | Verification | Remaining limit |
|---|---|---|---|---|---|---|---|
| Applicable UG requirements are integrated and working | Full accumulated suite on the Stage 12 candidate reported 58 passed, 0 failed. Interactive release demonstration also completed successfully. | No release blocker identified | Akshera Kandula; Harleen Partola | No code correction required. Preserve the verified candidate and complete final review/integration. | None required | Akshera: 58 passed. Harleen fresh clone: 58 passed at SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`. | Tests and demonstrations support the scoped course release but do not establish production healthcare readiness. |
| README and setup instructions must reproduce the candidate from a clean copy | Harleen cloned the repository into a separate clean directory, switched to `feature/stage12-release`, installed/checked dependencies, ran the demo, interactive console and complete test suite successfully. | No reproducibility blocker identified | Akshera Kandula | README release/setup information was updated before independent verification. | Documentation-only Stage 12 README updates | Fresh-clone verification succeeded with 58 passed and no additional setup step required. | Final source ZIP still needs to be produced from and checked against the final submitted SHA. |
| Cancellation must retain appointment history | Release demonstration showed a cancelled appointment remained findable as `CANCELLED`; retained regression tests also verify retained history and repeated cancellation rejection. | No release blocker identified | Group | No Stage 12 correction required. | None | Relevant regression tests retained and full suite passed. | Session history is retained only for the current process because persistence is intentionally out of scope. |
| Same-practitioner exact-time conflict must be enforced without inventing an overlap rule | Exact-time same-practitioner conflict was rejected, while a different practitioner at the same time was allowed. A proposed 30-minute overlap rule was rejected because it was not supported by FR-05. | No release blocker identified | Group | Keep current exact-time rule and reject unsupported feature expansion. | None | Interactive demonstration and retained conflict tests passed. | Appointment-duration/overlap scheduling is not part of the current requirement set. |
| Query/listing behaviour must remain deterministic and non-mutating | Practitioner listing supports default all-status results and explicit status filtering. Query functions remain explicit-input functions with deterministic date/time then ID ordering. | No release blocker identified | Group | No correction required. | None | Stage 9 tests retained; full Stage 12 suite passed. | Equal-time tie behaviour is primarily demonstrated through automated tests rather than the simple console flow. |
| Current release must disclose significant limitations rather than hide them | README and Stage 12 evidence document session-only storage, local naive minute-precision time, and production features that are outside scope. | No blocker; documented limitation | Akshera Kandula | Retain limitations in README/release evidence. | Documentation updates only | README review and fresh-copy check completed successfully. | No durable persistence, production authentication/roles, portal, notifications, billing/insurance, clinical AI, enterprise concurrency, monitoring or formal accessibility/usability assurance. |
| No unexplained or unsafe AI-generated release change should remain | Significant AI/Copilot suggestions were checked against requirements and tests; unsupported overlap behaviour was rejected. No autonomous AI release approval was used. | No release blocker identified | Akshera Kandula; Harleen Partola | Continue human review of final diff and release decision. | None | AI decisions are recorded in Stage 7/8 and Stage 12 evidence; full regression suite passed after accepted work. | AI assistance does not prove correctness; final accountability remains with the group. |
| PG rescheduling and assurance scope | Both members are UG students, so Stage 10 and Stage 11 PG requirements do not apply. | Not applicable | Not applicable | Leave supplied PG-only Stage 10/11 records unchanged. | None | Cohort/scope reviewed against Stage 12 pathway. | None for the UG release scope. |

Release-blocker conclusion:
No unresolved blocker against the applicable UG Stage 12 release scope was identified. The remaining items are documented scope limitations or final release-administration tasks rather than unmet FR, QRY, FP or UI requirements. Any later executable-code change would require focused verification followed by the full regression suite.

## I Git review and integration evidence

Issue / PR / diff links and reviewed SHA:
Stage 12 release work was completed on branch `feature/stage12-release` and reviewed through the Stage 12 pull request before integration into `main`. Harleen Partola independently verified the reviewed candidate at SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`.

Independent reviewer / feedback / response:
Harleen Partola acted as the independent reviewer. She also reproduced the candidate from a fresh clone, confirmed the demo and interactive console worked, and obtained 58 passing tests. No release-blocking issue or unrelated change was identified. No corrective code change was required following the review.

Integration commit / full recheck:
The approved Stage 12 changes were merged into `main`. After updating local `main`, the full regression suite was rerun from `project/` using `python3 -m pytest -q`. Result: 58 passed, 0 failed. The integrated `main` SHA is `ce62d54cc5b2725c420996be7e121ff035914017`.

Tracked and untracked file inspection / cleanliness:
`git status --short` produced no output after integration and regression verification, confirming no remaining modified or untracked files in the working tree. The integrated change contained the intended root `README.md`, `project/README.md` and Stage 12 evidence updates.

Secrets/staff material/caches/tool-metadata exclusion check:
The final reviewed changes contain synthetic SmartCare data only. No credentials, tokens, real patient information, confidential peer forms, staff solutions, environment directories, cache/compiled files or temporary tool-recovery artefacts were intentionally included in the release changes.

Candidate recovery plan / known-good SHA:
The independently verified pre-merge Stage 12 candidate can be recovered from SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`. The current integrated known-good `main` state is SHA `ce62d54cc5b2725c420996be7e121ff035914017`, verified with 58 passing tests. Git history provides the recovery path without deleting or rewriting earlier work.

Named substantive contributions:
- Akshera Kandula: Stage 12 release coordination, release-scope review, regression verification, interactive end-to-end demonstration, README/release documentation updates, limitation and technical-debt documentation, release evidence preparation and final integration verification.
- Harleen Partola: independent Stage 12 review and fresh-clone reproducibility verification, including dependency/setup checks, demo/interactive execution and full regression verification with 58 passing tests.

## J Human release decision

Decision — READY FOR COURSE RELEASE / READY WITH DOCUMENTED LIMITATIONS / NOT YET READY:
**READY WITH DOCUMENTED LIMITATIONS**

Approver / date / rationale and evidence:
Akshera Kandula and Harleen Partola — 9 November 2026. The group approves the SmartCare UG candidate for course release with the documented limitations. Evidence includes the completed Stage 12 end-to-end demonstration, retained regression suite with 58 passing tests, Harleen's independent fresh-clone verification at candidate SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`, human PR review, successful integration into `main`, and a post-integration full regression result of 58 passed at SHA `ce62d54cc5b2725c420996be7e121ff035914017`.

What risks remain / conditions / owners:
Remaining risks are documented scope limitations rather than unresolved UG requirements. SmartCare is session-only, uses local naive minute-precision appointment times, and does not provide production authentication/roles, durable persistence, portal access, notifications, billing/insurance, clinical decision support, enterprise concurrency, production monitoring or formal accessibility/usability assurance. These are accepted course-release limitations. Akshera Kandula owns final release packaging and SHA/ZIP correspondence checks before submission.

Can the team explain the system:
Yes. Both group members have worked with and reviewed the common SmartCare project. The team can explain the main requirements, shared `SmartCareDataStore`, domain/service/query/console responsibilities, booking-conflict and cancellation behaviour, meaningful regression evidence, responsible AI decisions and known limitations.

Can a change be recovered:
Yes. Git history preserves the reviewed Stage 12 candidate and earlier checkpoints. The independently verified candidate can be recovered at SHA `8a13da96e1ed6a2aff643d2fc8593c59a151474c`, and the integrated tested `main` state is SHA `ce62d54cc5b2725c420996be7e121ff035914017`. Recovery does not require deleting or rewriting repository history.

Common decision / PG decision where different:
Common UG decision: **READY WITH DOCUMENTED LIMITATIONS**. PG decision: **Not applicable — both group members are UG students and Stage 10/11 PG requirements are outside the release scope.**


## K Final tested release SHA

Exact tested release SHA:
`ce62d54cc5b2725c420996be7e121ff035914017`

Tested branch / state:
`main` after the reviewed Stage 12 pull request was merged.

Verification command and result:
From `project/`, `python3 -m pytest -q` was run after integration and reported **58 passed, 0 failed**.

Final submitted SHA:
**Pending final evidence-only commit after Sections K–N are completed and reviewed.**

Difference between tested SHA and final submitted SHA:
The tested release SHA `ce62d54cc5b2725c420996be7e121ff035914017` identifies the integrated executable release that passed the full regression suite. A later final submitted SHA is expected to contain only completed Stage 12 evidence/documentation. No executable application code is intended to change after the tested SHA. If executable code changes, the affected checks and full regression suite must be rerun before submission.

Common / PG identifiers:
Common UG tested release SHA: `ce62d54cc5b2725c420996be7e121ff035914017`.
PG release SHA: Not applicable — this is a UG-only group.

Source / ZIP correspondence:
The final source ZIP will be generated from the exact final submitted SHA after the remaining Stage 12 evidence is completed and committed. The ZIP will then be extracted and checked against that SHA before submission.


## L Submission package verification

Confirmed assessment item/upload route:
One final group source ZIP, accessible GitHub repository URL, full release SHA, README files and Stage 12 release evidence are required. Submission will use the Software Technology 1 Assignment 3 upload route provided by the teaching team.

Deadline/timezone:
11:59 PM, Monday 9 November 2026, AEDT (Australian Eastern Daylight Time).

Repository access arrangement:
Public shared GitHub repository accessible to teaching staff: `aksherakandula-git/st1-assignment--3`.

Mixed-candidate upload arrangement:
Not applicable — this is a UG-only group. One common UG release candidate is required and no separate PG candidate is needed.

Oral/video recording/accessibility arrangements:
The Individual Oral Assessment is completed separately in Cadmus. Each student completes six recorded common-project questions, with up to two attempts, 60 seconds preparation time and up to 3 minutes per response. Screen recording or screen sharing is not required. Any approved accessibility arrangements follow the teaching team's process.

Remaining administration or release dependency:
Complete final source ZIP packaging and verification, confirm the exact final submitted SHA, and submit the required Assignment 3 materials through the confirmed upload route before 11:59 PM AEDT on Monday 9 November 2026.

- [x] Feature freeze and scoped requirements traced.
- [x] Applicable full regressions, integrated demo and invalid paths verified.
- [x] Architecture/code quality and final AI/dependency checks complete.
- [x] Root README and project/README reproduced by another verifier.
- [x] Release notes, technical debt and limitations visible.
- [x] Independent human review, integration and release decision recorded.
- [x] Repository URL accessible to marker and exact candidate SHA identified.
- [x] One source ZIP from submitted commit with root README.md and .gitignore.
- [x] project/ source and all accumulated applicable tests included.
- [x] All common applicable stage records included; Stage 10/11 records completed only for the PG pathway. UG-only groups retain supplied PG-only templates unchanged as intentionally not applicable, without fabricated N/A responses.
- [x] No .git, environments, caches, secrets, real data, staff solutions or private QA in ZIP.
- [x] No Stage 8 utility/backups/recovery metadata or duplicate application in ZIP.
- [x] Mixed-group common protection and candidate upload routing checked.
- [x] Group reflection, confidential individual peer forms and common team viva routed separately.
## M Formative questions

1. **What is a release candidate?**  
A release candidate is a specific version of the software that the team believes is ready for final release checking. It should have the intended scope integrated, be identifiable by an exact Git SHA, and be tested before it is approved for release.

2. **What is feature freeze and why is it used?**  
Feature freeze means stopping optional feature development so the team can focus on verification, defects, documentation and release readiness. It reduces the risk of introducing new problems while preparing the final release.

3. **What is regression testing in a release context?**  
Regression testing means rerunning previously accumulated tests after integration or changes to confirm that behaviour that worked before still works. For SmartCare, the final integrated release passed the complete suite with 58 tests.

4. **What is a known limitation?**  
A known limitation is a behaviour or capability that is deliberately not provided by the current release and is clearly documented. For SmartCare, an example is session-only storage, where records are lost when the application exits.

5. **What is technical debt?**  
Technical debt is work that may reasonably be deferred now but could need attention if the system is extended or prepared for a different environment. It should be documented with its impact, priority and possible future action rather than being confused with an unmet current requirement.

6. **What are release notes?**  
Release notes summarise what the released version delivers, important fixes or improvements, known limitations and other relevant release information so reviewers and future maintainers can understand the version being released.

7. **What is software maintenance?**  
Software maintenance is the work performed after a release to correct defects, adapt the system to new needs or environments, and improve its quality. A released version should remain identifiable so later maintenance changes do not silently replace it.

8. **What is the purpose of the individual demonstration/viva?**  
The purpose is to confirm that each student genuinely understands the shared SmartCare project and can explain requirements, architecture, testing, debugging, AI decisions, limitations and their own contribution rather than relying only on submitted group artefacts.

9. **What should the final responsible-AI check establish before release?**  
It should establish that significant AI/Copilot suggestions were understood and independently checked, that no unsupported requirements or unexplained changes were introduced, that synthetic data and privacy rules were followed, and that final engineering and release decisions remained human decisions.

10. **What is the main course conclusion about AI and the role of the software engineer?**  
AI can assist with tasks such as generating ideas, tests, debugging suggestions and review comments, but software engineers are still responsible for interpreting requirements, judging correctness, evaluating evidence, managing risks, making design and release decisions, and remaining accountable for the final system.

## N Reflection viva and handover

### Reflection

Strongest evidence that SmartCare is ready:
The strongest evidence is the combination of the full regression suite, end-to-end demonstration, independent review and fresh-clone verification. The integrated `main` release at SHA `ce62d54cc5b2725c420996be7e121ff035914017` passed 58 tests. The interactive demonstration also verified registration, lookup, booking, practitioner conflict handling, cancellation/history, practitioner listing, invalid-input recovery and normal exit. Harleen independently reproduced the Stage 12 candidate from a fresh clone and also obtained 58 passing tests. Together these provide stronger release evidence than a single successful run.

Weakest area:
The weakest area is production readiness outside the current course scope. SmartCare stores data only for the current session, uses local naive minute-precision datetimes and has no production authentication/roles, persistence, notifications, billing, clinical decision support, enterprise concurrency, production monitoring or formal accessibility/usability assurance. These are documented limitations rather than failures of the current UG requirements.

How did our use of AI change from Stage 1 to Stage 12:
In Stage 1, our focus was recognising that AI-generated code or feature suggestions cannot automatically be treated as correct. We identified that client requirements still need human validation and rejected unsupported suggestions such as facial recognition, AI diagnosis, online payment and insurance processing. By Stage 12, our AI use became more evidence-driven. AI/Copilot was used for bounded tasks such as test-design ideas, debugging and review, but suggestions were traced back to requirements and independently verified. For example, a proposed 30-minute appointment-overlap rule was rejected because FR-05 specifies an exact same-practitioner/date-time conflict. The main change was moving from simply recognising that AI needs checking to using explicit Accept/Modify/Reject decisions supported by requirements, code inspection and test evidence.

### Start / Stop / Continue retrospective

| Area | Start doing | Stop doing | Continue doing |
|---|---|---|---|
| Engineering practice | Start planning release evidence and reproducibility checks earlier so README, SHA and clean-copy verification are maintained throughout development. | Stop treating a passing test count by itself as proof that the system is correct or release-ready. | Continue using focused branches, human review, requirement-linked tests, full regression checks and exact Git SHAs for important checkpoints. |
| AI use | Start writing the human expectation and requirement trace before asking AI for implementation, testing or review suggestions. | Stop accepting AI-generated rules, assumptions or suggested features unless they are supported by the approved requirements. | Continue treating AI/Copilot output as candidate advice that must be independently checked, accepted, modified or rejected by the team. |

What worked well:
Requirement-linked testing, human PR review, keeping one shared `SmartCareDataStore`, retaining earlier tests, and using small focused corrections helped prevent regressions. The Stage 8 debugging work was particularly useful because the team diagnosed behaviour against FR-05 and FR-07 rather than changing tests simply to obtain a green result.

What caused rework:
Some rework came from needing to revisit documentation, release evidence and branch/integration details late in the process. AI suggestions also required additional checking when they introduced assumptions beyond the requirements, such as the proposed appointment-overlap rule.

What we would improve in a future delivery:
We would maintain release documentation, known limitations and reproducibility instructions continuously rather than completing much of this at the final release stage. We would also record significant AI decisions and verification evidence immediately when they occur.

What should continue:
We would continue requirement-first reasoning, meaningful automated tests, independent human review, explicit responsibility boundaries, synthetic-data use and verification of AI-generated suggestions before integration.

### Viva / handover preparation

| Preparation item | Own explanation and evidence link |
|---|---|
| Problem and stakeholders | SmartCare addresses clinic problems caused by spreadsheets and paper records, including duplicate bookings, difficulty locating patient information, inconsistent appointment status and limited history. Stakeholders include reception/admin staff, practitioners, patients and clinic management. |
| Two requirements and acceptance criteria | FR-05: the same practitioner cannot have another `SCHEDULED` appointment at the exact same datetime, while another practitioner may use that time. FR-06/FR-07: a scheduled appointment can be cancelled, becomes `CANCELLED`, remains stored/retrievable and cannot be cancelled repeatedly. |
| Domain model and architecture | `Patient`, `Practitioner`, `Appointment` and `AppointmentStatus` represent domain concepts and state. `SmartCareDataStore` holds current-session objects. Services coordinate workflows, query functions perform explicit-input selection/sorting, and the console owns user interaction. |
| Design trade-off | SmartCare deliberately uses one shared in-memory store instead of persistence. This keeps the course architecture simple and makes object identity/session behaviour clear, but records are lost when the process exits. |
| Meaningful test and its limits / 100 percent coverage | `test_f8_02_cancelled_appointment_remains_available_in_store` verifies that cancellation changes the appointment to `CANCELLED`, keeps the same appointment retrievable and retains it in the store. Even 100% code coverage would not prove requirement correctness, meaningful assertions or that all important behaviours were tested. |
| Diagnosed defect and verification | Stage 8 identified defects in practitioner conflict handling and cancelled-history behaviour. Repairs were checked with focused regression tests and then the full suite. The final integrated release passed 58 tests. |
| Shared store and session-state/query responsibilities | All services use the same `SmartCareDataStore`, allowing them to work with the same registered objects. Query functions receive explicit appointment collections and return filtered/sorted results without mutating the store. |
| What would break if session-state lookup/query responsibilities changed | Returning replacement objects instead of the stored objects could break identity and retained-history behaviour. Allowing query functions to mutate or secretly access the store would weaken deterministic behaviour and responsibility separation. |
| Why cancellation is a domain responsibility | Whether an appointment can transition from `SCHEDULED` to `CANCELLED` is a rule about the Appointment object's valid state. The service locates the appointment and coordinates the workflow, while `Appointment.cancel()` protects the state transition itself. |
| FR-07 retained-history evidence | Cancellation does not delete the appointment. The regression test verifies that the same object remains retrievable with `CANCELLED` status, and the interactive demonstration also showed the cancelled appointment remaining available in history. |
| Actual AI change rejected/modified or acceptance check | A proposed 30-minute overlap conflict rule was rejected because FR-05 only defines conflict for the same practitioner at the exact same datetime while `SCHEDULED`. Adding an overlap rule would invent an unsupported requirement. |
| Unresolved limitation / future production work | Session-only storage is the clearest limitation. Real deployment would also require authentication/roles, durable persistence, timezone policy, security, monitoring, concurrency handling and accessibility/usability evaluation. |
| Personal implementation contribution | Akshera contributed Stage 12 release coordination, regression checking, interactive demonstration, README/release documentation, technical-debt/limitation recording and final integration verification. |
| Personal test/review/design/integration contribution | Akshera participated in testing, debugging, review and integration across the common SmartCare stages. Harleen independently reviewed and reproduced the Stage 12 candidate from a fresh clone and verified the complete regression suite. |
| PG agentic change and rescheduling verification | Not applicable — both group members are UG students. |
| PG responsible-AI risk/remediation or supported no-finding decision | Not applicable — Stage 10 and Stage 11 PG requirements are outside the UG release scope. |

Optional bounded-change practice only:
No additional code change was required for Stage 12. The team preserved the tested release rather than introducing unnecessary late changes.

Practice question/change and reasoning:
If a small change were required after release testing, we would first identify the exact requirement affected, predict the expected impact, make the smallest justified change, run the focused test and then rerun the full regression suite before accepting a new release candidate.

Separate reflection / peer / common team viva evidence:
The Stage 12 record supports release evidence and viva preparation. The approximately 500-word group reflection, confidential individual peer forms and common team viva/oral assessment follow their separate teaching-team submission processes.

No further coding stage:
The integrated tested candidate remains the release baseline. Any later executable change must follow the published correction/review process and be reverified rather than silently replacing the submitted version.

### Closing question — If AI can write code, why do we still need software engineers?

AI can generate code quickly, but software engineering involves much more than producing code. Engineers must understand stakeholder needs, validate requirements, choose appropriate architecture, design meaningful tests, diagnose defects, assess risks, review changes and decide whether evidence is sufficient for release. This matches our Stage 1 conclusion that validating requirements with the client cannot safely be delegated entirely to AI because AI may make assumptions that do not reflect the client's actual needs. The SmartCare project reinforced this throughout the semester: AI helped with suggestions, test ideas and review, but humans had to reject unsupported features, verify behaviour against requirements and remain accountable for the final release.