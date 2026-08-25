# Environment variables

## Strategy

- Local values and secrets go in `.env` (gitignored, never committed).
- `.envrc` is used only for direnv shell setup and non-secret developer
  tooling. It is committed to Git, so never place credentials, tokens,
  passwords, or API keys in it.
- Application code reads configuration from the process environment via
  `Settings` in `src/shuhari_cli/core/config.py`, and must not depend on
  `.env`/`.envrc` existing.
- Require variables via `Settings` fields with no default when they're
  actually needed; never log secret values.

## Current variables

| Variable | Read by | Default | Purpose |
|---|---|---|---|
| `APP_NAME` | `Settings.app_name` | `shuhari-cli` | Display name used in CLI output. |
| `ENVIRONMENT` | `Settings.environment` | `development` | Current run environment. |

## Adding a new variable

1. Add the field to `Settings` in `src/shuhari_cli/core/config.py`.
2. Add it to `.env.example` with a comment explaining what it's for.
3. Add a row to the table above.
4. If it's a secret, make sure it has no default and is never logged.
