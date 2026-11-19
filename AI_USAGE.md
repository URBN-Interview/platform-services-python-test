# AI Usage Disclosure

**Did you use AI tools for this exercise?** Yes

## Tools and models
* **Claude Opus 5.5** (`claude-opus-5-5`) via **Claude Code**, Anthropic's agentic coding CLI, which ran with access to this repository and a local shell.



## How you used them
I gave Claude the assessment as a whole and let it plan and implement the solution end to end, then reviewed and verified the result.

* **Requirements analysis:** Claude read the root, RewardsService, and RewardsUI READMEs and the existing code to identify the required endpoints, the rewards algorithm, and the dashboard features.
* **Implementation in incremental commits** on the `feature/rewards-service-and-ui` story branch:
  1. A pure, I/O-free rewards calculation module with unit tests (points per whole dollar, tier lookup, top-tier cap, next-tier progress, input validation).
  2. RESTful Tornado endpoints: `POST /orders`, `GET /customers/{email}`, and `GET /customers`. They use an async Motor repository with atomic, capped point updates and a unique email index, return consistent JSON errors (400/404/405/503), and have handler tests that run against an in-memory fake repository.
  3. The Django Customer Rewards Dashboard: a service client with timeouts and error mapping, form validation, Post/Redirect/Get order submission, filtering by email, a styled responsive template, graceful handling when the service is down, and view and client tests.
  4. API and test documentation in the READMEs.
* **Verification:** with Docker running, Claude built and started both stacks and checked every endpoint with `curl` against the real MongoDB. This covered the README example, accumulating points, the top-tier cap, validation errors, 404s, and 20 orders sent at the same time to confirm no points are lost. It also ran both test suites inside the containers (23 service tests and 13 UI tests, all passing).

## What you changed or rejected
I reviewed the code, the commit history, and the documentation, and checked the dashboard manually in the browser (adding orders, validation errors, filtering, and the behaviour when the service is down). Everything met the requirements, so I made no changes to the AI-generated output.

Design decisions I reviewed and accepted:
* Points accumulate across orders and are capped at the top tier (1000), so no further rewards can be earned after tier J.
* `nextTierProgress` is `points / nextTier.points`, which matches the README example (100 of 200 → 0.5).
* Emails are normalised to lower case so that one customer cannot get duplicate records.
* One mistake was caught and fixed during the session: `__pycache__` files were committed by accident. A follow-up commit removed them and added them to `.gitignore`.
