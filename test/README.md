# Skill tests

Checks that the skills make a model behave the way they describe. Each scenario gives a small coding task to a fresh headless Claude Code session and then checks three things: the session loaded the skill, it read every file the `SKILL.md` table lists for that task, and the code it wrote follows the rules.

Run it after changing a `SKILL.md` description, a routing table, a rule, or what lives in `references/details/`.

## Requirements

- Claude Code installed and logged in, with `claude` on the `PATH`.
- The skills installed from this working copy, so the sessions read the files you are editing: `~/.claude/skills/moxwel-code-style` and `~/.claude/skills/moxwel-standard-react-frontend` must resolve to the folders in `skills/`.
- Python 3.9 or newer. No packages to install.

## Usage

```bash
python3 test/run_scenarios.py round1                    # every scenario once
python3 test/run_scenarios.py round1 cut2 robust        # only these scenarios
python3 test/run_scenarios.py round1 robust:1 robust:2  # the same scenario twice
python3 test/run_scenarios.py --self-check              # tests the alignment check, starts no session
```

The first argument names the round. Each session works in its own folder under the system temp folder (`/tmp/moxwel-skill-tests/<round>/` on Linux), outside this repo so that its `CLAUDE.md` does not tell the session which style to follow. The session log is the `.jsonl` file next to each folder. Running a round name again replaces the folders of the scenarios you run.

All sessions of a round run at the same time with `--model sonnet` and stop after 9 minutes. In the 51 sessions used to tune the skill, one session cost between 0.11 and 0.29 USD.

## Reading the output

```text
[PASS] cut2: skill=yes references=['comments-and-docs', 'copy', 'naming', 'readability'] details=[] words=2177
[PASS] robust: skill=yes references=['comments-and-docs', 'copy', 'naming', 'readability', 'robustness'] details=['comments-and-docs', 'naming', 'readability'] words=4582
2/2 passed, 0.34 USD. Outputs and logs: /tmp/moxwel-skill-tests/verify
```

- `skill` says whether the session loaded `moxwel-code-style`.
- `references` and `details` list the skill files the session read. A read that was denied or failed does not count.
- `words` is the size of those files, to compare how much a task loads before and after a change.

A run that fails lists its problems below its line:

```text
[FAIL] robust:1: skill=yes references=['comments-and-docs', 'copy', 'naming', 'readability', 'robustness'] details=['comments-and-docs', 'naming', 'readability'] words=4541
    constants: group [(9, 11)] padded past its widest item (missed the 8-column cut?)
```

- A `required files not read` line names the files the `SKILL.md` table lists for the task that the session never opened.
- The other lines are rules the code breaks. An alignment group is a list of `(name width, spaces before the value)` pairs: here a 9-column name got 11 spaces to line up with a name 8 or more columns wider.

The command exits with 1 when a run fails.

A model does not answer the same way twice. Repeat a scenario (`cut2:1 cut2:2 cut2:3`) before trusting a pass or a failure, and read the file the session wrote before changing the skill: a check can be stricter than the rule.

## Scenarios

| Scenario | Task | What it checks |
|---|---|---|
| `align` | Add two constants to a TypeScript file | Alignment of the new constants, a unit in the name, existing lines untouched |
| `cut` | Add two fields to an aligned object | The 8-column cut between field names, existing fields untouched |
| `cut2` | Create four constants with names of very different width | The 8-column cut in new code |
| `imports` | Add a function that needs three new imports | Import groups and order, type-only import, named conditions |
| `robust` | Write a Python client for a flaky API | Timeout, domain error with its cause, `Retry-After`, docstring tags, and that it read `robustness.md` and the Python details |
| `naming` | Add a predicate and a slug function | Boolean prefix, named constant, short doc comments |
| `doc` | Add a function with a hidden outcome to a Python file | `:returns:` tag, existing unaligned constants untouched |
| `bash` | Write a Bash script | Shebang, header with usage, predicate functions, line width |
| `tsdoc` | Add a function with a hidden outcome to a TypeScript file | `@returns` tag, no echo `@param`, command name |
| `mindiff` | Add a function to a file that breaks several rules | Every existing line stays as it was |
| `react` | Add a component to a Next.js app | Only that the session loaded the React skill and read its references |

## Files

- `scenarios.py`: the scenarios. Edit this one to change a prompt, a starting file or the files a session must read.
- `checks.py`: the check of each scenario, registered in `CHECKS` under the scenario name.
- `alignment.py`: the alignment check shared by the scenarios.
- `session_log.py`: reads a session log to find the skills loaded and the files read.
- `run_scenarios.py`: starts the sessions and prints the verdicts.

To add a scenario, add an entry to `SCENARIOS` in `scenarios.py` and a `check_<name>` function to `CHECKS` in `checks.py`.
