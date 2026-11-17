# AI Usage Disclosure

**Did you use AI tools for this exercise?** Yes

## Tools and models
Claude Opus 5.5 (`claude-opus-5-5`) via Claude Code (CLI agent).

## Prompts
> go through the readme.md file and understand the assessment and complete it both RewardService and RewardUI

## How you used them
* Claude read the root, RewardsService and RewardsUI READMEs and the existing code, then implemented the solution
  on the `feature/rewards-service-and-ui` story branch in incremental commits:
  1. The pure rewards calculation algorithm and its unit tests.
  2. The Tornado endpoints (`POST /orders`, `GET /customers/{email}`, `GET /customers`), an async Motor
     repository, JSON error handling, and handler tests that use an in-memory fake repository.
  3. The Django dashboard: service client, forms, views, styled template, and view/client tests.
  4. API docs in the READMEs and this file.
* Claude ran the unit tests locally. Docker was not running in that environment, so Claude did not run the
  end-to-end Docker setup.

## What you changed or rejected
<!-- TODO (candidate): describe anything you reviewed, changed, or rejected in the AI's output. -->
