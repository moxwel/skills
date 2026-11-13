# Copy: details

Details and gotchas for the rules in [../copy.md](../copy.md).

## Details

- **Before and after:**

| Before | After |
|---|---|
| `Unlock seamless collaboration` | `Work with your team in one shared space` |
| `Get Started` | `Create account` |
| `No data available` | `No jobs yet. Run a sync to see results here` |
| `Something went wrong` | `The upload failed. Check your connection and try again` |
| `The password was updated` | `Password updated` |

- **Placeholders** in fields and cells say what goes there (`Your name`, `email@example.com`) instead of fake but plausible data (`John Doe`, `johndoe@example.com`).
- **Quotation marks and capitals:** quotes only for real quotations, titles and dialogue; no sentence in ALL CAPS for emphasis.
- **Unfinished text:** a loading message is `Loading items...` with three periods, never the single ellipsis character. A truncated value is cut by the layout (`text-overflow`), not by typing an ellipsis.
- **The project's own voice wins:** a project `CLAUDE.md`/`AGENTS.md` or a writing sample from the user sets the tone. If that voice uses an em dash or a generic label on purpose, name the rule and ask before keeping or cutting it.

## Gotchas

- **Rules 2 and 6 are about UI.** A comment or a README is not a button or an error message, so they do not apply there. Rules 1, 3, 4, 5 and 7 do.
- **Agent files are out of scope.** Skills, `CLAUDE.md`/`AGENTS.md`, memory and plans keep whatever shape suits the agent, and so do these reference files.
- **A real number is fine.** Rule 4 bans invented facts, not facts that come from the data or a named source.
