# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired directly by the Anthropic Claude Code best practices documentation regarding repository context grounding. A structured `CLAUDE.md` file provides clear, systemic boundaries for the agent upon every session initialization, ensuring it doesn’t attempt to use forbidden package managers or break existing linting gates.

b. Design of each automation, including goals, inputs/outputs, steps
> *   **Goal:** Provide an immediate execution and style guardrail for Claude Code so it adheres to our project's environment and architectural layout without guessing.
> *   **Inputs:** Read automatically by Claude Code at startup from the workspace root.
> *   **Outputs:** Highly aligned code generation, consistent styling matching our linters, and predictable test execution commands.
> *   **Steps:** 
>     1. Define the core project technology stack (FastAPI, SQLite, Python).
>     2. Establish execution commands utilizing the project `Makefile`.
>     3. Impose explicit guardrails enforcing code quality checks (`black` and `ruff`) before any feature completion.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> *   **Exact Command:** Simply start Claude Code in the repository root terminal: `claude`
> *   **Expected Output:** Claude will output that it has loaded and initialized context from `CLAUDE.md`. When asked to add an endpoint or modify code, it will automatically run formatting and linting scripts from our `Makefile`.
> *   **Rollback/Safety Notes:** To modify or remove rules, simply edit or delete the `CLAUDE.md` file. It acts as an idempotent systemic prompt layer with no dangerous side effects on the source code.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> *   **Manual Workflow:** Developers must manually remind the agent to run `make format` and `make lint`, or fix broken imports and random code style anomalies that fail the `pre-commit` hooks right before trying to commit code.
> *   **Automated Workflow:** Claude automatically respects the formatting tools (`black`, `ruff`), points directly to correct router paths, and proactively ensures local changes don't violate our design limits before completing a task.

e. How you used the automation to enhance the starter application
> Used `CLAUDE.md` to cleanly direct the agent to backend routing paths, forcing it to preserve database seeding protocols while expanding the app feature set without breaking our `pytest` setups.


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> Inspired by the Anthropic Claude Code Custom Slash Commands documentation. This encapsulates repeated multi-stage developer validation workflows into a single headless execution target, minimizing context-switching overhead.

b. Design of each automation, including goals, inputs/outputs, steps
> *   **Goal:** Streamline the developer validation cycle by stringing together test runners, test verification, and automated error explanation.
> *   **Inputs:** Triggered via the custom markdown token command interface using `.claude/commands/test-coverage.md`.
> *   **Outputs:** A structured analysis terminal log summarizing success metrics or highlighting precise stack traces with AI-assisted structural refactor recommendations.
> *   **Steps:** 
>     1. Execute `make test` inside the terminal environment.
>     2. Read execution output flags.
>     3. If tests pass, execute automated script linting checks (`make lint`).
>     4. If failure occurs, isolate the error trace and output a bulleted checklist of debugging remediations.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> *   **Exact Command:** Inside the active Claude Code interactive terminal prompt, type: `/test-coverage`
> *   **Expected Output:** A clean, processed output log showing the status of the `pytest` suite along with a summarized validation checkmark confirming our format and code sanity checks pass.
> *   **Rollback/Safety Notes:** This command operates purely on a read/test execution layer. It does not write destructive updates to code files directly, making it completely risk-free to run repeatedly.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> *   **Manual Workflow:** A developer must break away from the prompt, run `make test`, read the long text block, manually copy the error, paste it back to the agent, run `make lint`, and evaluate manually.
> *   **Automated Workflow:** Running `/test-coverage` handles the compilation, testing, and lint cycle all in one execution block, automatically interpreting code faults on the fly.

e. How you used the automation to enhance the starter application
> Used this automation while developing endpoints for the developer center app. It immediately caught missing dependencies and unformatted patterns in real-time, drastically reducing the turnaround time needed to pass pre-commit checks.