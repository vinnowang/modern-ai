# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.


## SUBMISSION DETAILS

Name: **Matthew** \
This assignment took me about **5** hours to do. 

## YOUR RESPONSES
Tasks completed:
> - **Task 4**: Frontend UI Expansion (Added the Filter menu toggle and the Bulk Complete feature)
> - **Task 6**: Intelligent Action Item Extraction (Upgraded the regex parser to handle standard Markdown checkboxes `- [ ]` alongside legacy TODO items)
> - **Task 7**: Global Error Handling (Implemented FastAPI middleware to catch unexpected errors and return clean, consistent JSON responses)

---

### Automation A: Warp Drive saved prompts, rules, MCP servers

a. Design of each automation, including goals, inputs/outputs, steps
> - **Goal**: Set up a fast, headless validation flow so I can verify code quality at once.
> - **Inputs**: The local project repository directory (`week6/backend`).
> - **Outputs**: Code cleanups using `black`, linting fixes by the `ruff`, and complete test suite results from `pytest`.
> - **Steps**: 
>   1. Trigger `make format` to let `black` automatically clean up code layouts and let `ruff check . --fix` handle linting updates.
>   2. Run the test suite using `PYTHONPATH=. pytest backend/tests` to ensure Python correctly resolves our local modules without path errors.

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> - **Before**: I had to track down inconsistencies, guess why `pytest` was giving `ModuleNotFoundError` variations inside nested folders, and manually fix environment dependency issues (like installing `httpx` for the FastAPI test client).
> - **After**: Everything is wrapped into simple terminal routines. A quick command formats the code, checks for deeper issues (like exception chaining warnings), and instantly verifies that all tests pass.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **Autonomy Level**: Highly Supervised Generation.
> - **Permissions**: Write permissions were limited to the local code files, frontend files, and tests inside the `week6/` folder.
> - **Supervision**: I closely supervised every automated code change. I manually tested the new regex logic and error handling by clicking through the UI at `localhost:8000` and double-checking the terminal outputs to confirm the test suite was completely green.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> N/A (Kept this as a focused, single-agent engineering flow).

e. How you used the automation (what pain point it resolves or accelerates)
> It speeds up the feedback loop significantly. Instead of worrying about manual style checks or accidentally breaking old features, I can confidently write a new extraction rule or update a layout, run the check, and know within seconds if it works perfectly.

---

### Automation B: Multi‑agent workflows in Warp 

a. Design of each automation, including goals, inputs/outputs, steps
> - **Goal**: Break down larger full-stack features into parallel workflows, separating the frontend layout tasks from the backend schema and endpoint code.
> - **Inputs**: Functional requirements for the user interface updates (Task 4) and text parsing logic (Task 6).
> - **Outputs**: Concurrently updated files, including frontend scripts, state filters, and improved backend text-matching tools.
> - **Steps**:
>   1. Used one dedicated terminal space to build out the frontend components (the filter dropdown logic and the bulk action checkbox array).
>   2. Used a parallel terminal space to focus completely on the backend (refining the Python regex logic and implementing the error middleware).

b. Before vs. after (i.e. manual workflow vs. automated workflow)
> - **Before**: I had to bounce back and forth between writing frontend JavaScript/HTML and editing FastAPI backend endpoints, which broken up my focus and made debugging take longer.
> - **After**: I could isolate the two parts of the stack. I worked on the visual UI filters in tandem with the backend data logic, which kept things organized and cut down development time.

c. Autonomy levels used for each completed task (what code permissions, why, and how you supervised)
> - **Autonomy Level**: Supervised Execution.
> - **Permissions**: Read/Write access strictly constrained to the `backend/app` and `frontend/` logic boundaries.
> - **Supervision**: I actively reviewed the changes in both workspaces to ensure they aligned perfectly—specifically making sure the bulk actions built on the frontend mapped seamlessly to the `BulkCompletePayload` data structure expected by the API.

d. (if applicable) Multi‑agent notes: roles, coordination strategy, and concurrency wins/risks/failures
> - **Roles**: One context functioned as the Frontend Developer creating the UI elements; the other acted as the Backend Engineer updating the API.
> - **Coordination Strategy**: We used a contract-first approach. We agreed on the exact JSON payload design for the `/action-items/bulk-complete` POST endpoint right at the start, which let both layers move forward independently without blocking each other.
> - **Concurrency Wins**: Building the UI layout at the exact same time the backend was being upgraded to parse Markdown checkboxes saved a ton of context-switching time.

e. How you used the automation (what pain point it resolves or accelerates)
> It completely removes development bottlenecks. By decoupling the interface code from the database logic, different parts of the task application could be built and tested simultaneously without conflicts or clobbering each other's work.
## Tasks Completed (Added in Week 6)
- **Task 8: List endpoint pagination for all collections** (Implemented pagination fallback query parameters on notes and action-items to support backend efficiency and clean frontend loading)
- **Task 9: Query performance and database indexes** (Added database index constraint to Note.title inside SQLAlchemy models to optimize search query executions)
