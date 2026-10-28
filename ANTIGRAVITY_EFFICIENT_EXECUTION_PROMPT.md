# Antigravity execution prompt — low usage / high efficiency

Read `PROJECT_BRIEF_FOR_ANTIGRAVITY.md` once and treat it as the full requirements source. Then execute the project, not another long planning conversation.

## Resource rules
- Minimize quota usage: short reasoning, short final reports, no repeated plans, no duplicate summaries, no broad workspace rescans, and no unnecessary background agents.
- Inspect the workspace once. Use a concise file inventory, then work only with relevant files.
- Never print the CSV or large query results. Use Python/SQL summaries, small samples, and targeted checks only.
- Reuse valid prepared assets. Do not regenerate the dataset/database or reinstall packages unless a specific test proves it is necessary.
- Do not install plugins/MCP servers or new packages just to explore. Install only a required dependency, once.
- Run tests in one grouped command where possible. If an issue fails twice, stop retrying, record the blocker, and continue with other deliverables.
- Make changes directly and save progress often. Keep original data and the old workspace untouched.
- Final report: maximum 200 words, with file paths, actual test results, blockers, and only the manual actions still required.

## Critical Tableau rule
The deliverable must be a real, native Tableau Public workbook. Do NOT hand-generate, patch, or fabricate `.twb`/`.twbx` XML. The prior generated workbook failed in Tableau. Quickly determine whether you have reliable GUI automation that can operate the actual Tableau Public Desktop application (not merely launch it or inspect XML).

- If real GUI control is available, build in Tableau itself and verify the workbook opens, charts render, dashboard filters work, and story scenes navigate.
- If real GUI control is not available, say so plainly in one short message and do not burn quota trying XML hacks. Complete/verify the SQL, data quality, Flask code, documentation, and evidence matrix; then give the user the shortest exact manual Tableau steps.
- Do not claim a workbook is valid just because a file exists, XML parses, a process starts, or a test script says PASS. Actual Tableau open/render verification is the success condition.

## Priority order
1. Verify files/schema and the existing SQLite/SQL pipeline with targeted tests.
2. Deliver at least 9 genuinely distinct Tableau chart worksheets, covering all seven analysis areas listed in the brief; create a readable interactive dashboard, useful filters, calculated fields, and at least 3 stakeholder-based story scenes.
3. Reuse and test the Flask app. Keep dashboard/story URLs configurable placeholders until the user publishes real Tableau Public URLs.
4. Complete concise documentation, measured performance evidence, video script, and requirement-to-evidence matrix. Never fabricate results or mark untested work as complete.

Start now. Do not ask the user for approval for routine choices. Ask only if a real credential, publishing action, or necessary decision requires the user. Prefer the simplest reliable solution that meets the brief over cosmetic extras.
