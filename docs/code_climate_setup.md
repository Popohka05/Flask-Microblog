# Code Climate setup

This repository is ready for Code Climate connection, but the badge itself can be added only after the repository owner authorizes GitHub access in the Code Climate web interface.

## What to do

1. Sign in to Code Climate with your GitHub account.
2. Add the repository `Popohka05/Flask-Microblog`.
3. Wait for the first maintainability analysis to finish.
4. Copy the Markdown badge from Code Climate.
5. Paste the badge near the top of `README.md`.
6. Commit and push the README update.

## Badge location in README

Place it directly under the project title:

```md
# Flask Microblog
[![Maintainability](CODE_CLIMATE_BADGE_URL)](CODE_CLIMATE_PROJECT_URL)
```

## Why this is not automated here

Code Climate requires owner-side authorization and generates repository-specific badge URLs after the project is connected. Those URLs are not available before web setup is completed.
