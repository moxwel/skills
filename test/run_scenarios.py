"""
Skill test harness: runs each scenario in a fresh headless `claude -p` session, then checks which skill files
the session read and whether the code it wrote follows the rules. Usage is in README.md.
"""

from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback

from alignment import self_check
from checks import output_problems
from scenarios import SCENARIOS
from session_log import missing_skill_files, session_facts

USAGE = "Usage: python3 test/run_scenarios.py <round-name> [scenario[:repetition] ...] | --self-check"
MODEL = "sonnet"
# Read is allowed everywhere because the skill files live outside the session folder.
PERMISSION_FLAGS = ["--permission-mode", "acceptEdits", "--allowedTools", "Read", "Glob", "Grep"]
OUTPUT_FLAGS     = ["--output-format", "stream-json", "--verbose"]
BASE_SKILL       = "moxwel-code-style"
# Sessions run outside the repo, so its CLAUDE.md cannot tell them which style to follow.
RUNS_DIR = Path(tempfile.gettempdir()) / "moxwel-skill-tests"
# All sessions of a round share this limit; the ones still running when it ends are killed.
ROUND_TIMEOUT_SEC = 540

# Round names and repetitions become folder names, so they take no path separators.
ROUND_NAME = re.compile(r"[\w-]+")
RUN_ID     = re.compile(r"(\w+)(:\w+)?")


def scenario_name(run_id: str) -> str:
    return run_id.split(":")[0]


def work_dir_of(run_id: str, round_dir: Path) -> Path:
    return round_dir / run_id.replace(":", "_")


def log_path_of(work_dir: Path) -> Path:
    return work_dir.with_name(work_dir.name + ".jsonl")


def is_valid_run_id(run_id: str) -> bool:
    match = RUN_ID.fullmatch(run_id)
    return match is not None and match.group(1) in SCENARIOS


def start_session(run_id: str, round_dir: Path) -> subprocess.Popen:
    """Writes the starting files of the scenario to a fresh folder and starts a headless session in it."""
    scenario = SCENARIOS[scenario_name(run_id)]
    work_dir = work_dir_of(run_id, round_dir)
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)
    for file_name, content in scenario["files"].items():
        file_path = work_dir / file_name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
    command = ["claude", "-p", scenario["prompt"], "--model", MODEL, *PERMISSION_FLAGS, *OUTPUT_FLAGS]
    with log_path_of(work_dir).open("w", encoding="utf-8") as log_file:
        return subprocess.Popen(command, cwd=work_dir, stdout=log_file, stderr=subprocess.STDOUT)


def wait_for_sessions(sessions: dict[str, subprocess.Popen]) -> list[str]:
    """Waits until every session ends or the round times out. Returns the run ids it had to kill."""
    deadline  = time.monotonic() + ROUND_TIMEOUT_SEC
    timed_out = []
    for run_id, session in sessions.items():
        remaining_sec = max(0, deadline - time.monotonic())
        try:
            session.wait(timeout=remaining_sec)
        except subprocess.TimeoutExpired:
            session.kill()
            session.wait()
            timed_out.append(run_id)
    return timed_out


def evaluate(run_id: str, round_dir: Path, has_timed_out: bool) -> tuple[bool, float]:
    """Prints the verdict of one run. Returns whether it passed and what its session cost in USD."""
    name     = scenario_name(run_id)
    work_dir = work_dir_of(run_id, round_dir)
    facts    = session_facts(log_path_of(work_dir))
    missing  = missing_skill_files(SCENARIOS[name], facts)
    try:
        problems = output_problems(name, work_dir)
    except OSError as error:
        problems = [f"expected file missing: {error.filename}"]
    except Exception:
        # one broken check must not stop the round: show the trace and fail this run only
        traceback.print_exc()
        problems = ["the check crashed, see the trace above"]
    if has_timed_out:
        problems.insert(0, f"session killed after {ROUND_TIMEOUT_SEC} s")
    elif not facts["is_finished"]:
        problems.insert(0, "session ended with an error, see its log")
    is_loaded = BASE_SKILL in facts["skills"]
    is_pass   = is_loaded and not missing and not problems
    verdict   = "PASS" if is_pass else "FAIL"
    loaded    = "yes" if is_loaded else "NO"
    print(f"[{verdict}] {run_id}: skill={loaded} references={sorted(facts['references'])} "
          f"details={sorted(facts['details'])} words={facts['words']}")
    if missing:
        print(f"    required files not read: {missing}")
    for problem in problems:
        print(f"    {problem}")
    return is_pass, facts["cost_usd"]


def main() -> None:
    arguments     = sys.argv[1:]
    is_self_check = arguments == ["--self-check"]
    if is_self_check:
        self_check()
        return
    if not arguments:
        sys.exit(USAGE)
    round_name = arguments[0]
    run_ids    = arguments[1:] or list(SCENARIOS)
    unknown_run_ids     = [run_id for run_id in run_ids if not is_valid_run_id(run_id)]
    is_round_name_valid = ROUND_NAME.fullmatch(round_name) is not None
    has_claude = shutil.which("claude") is not None
    if not is_round_name_valid:
        sys.exit(f"Invalid round name: {round_name}. Use letters, digits, - and _ only.")
    if unknown_run_ids:
        sys.exit(f"Unknown scenarios: {', '.join(unknown_run_ids)}. Pick from: {', '.join(SCENARIOS)}.")
    if not has_claude:
        sys.exit("The claude command is not on the PATH. Install Claude Code and run this again.")
    round_dir      = RUNS_DIR / round_name
    sessions       = {run_id: start_session(run_id, round_dir) for run_id in run_ids}
    timed_out      = wait_for_sessions(sessions)
    outcomes       = [evaluate(run_id, round_dir, run_id in timed_out) for run_id in run_ids]
    passed_count   = sum(is_pass for is_pass, cost_usd in outcomes)
    total_cost_usd = sum(cost_usd for is_pass, cost_usd in outcomes)
    has_failures   = passed_count < len(run_ids)
    print(f"{passed_count}/{len(run_ids)} passed, {total_cost_usd:.2f} USD. Outputs and logs: {round_dir}")
    sys.exit(1 if has_failures else 0)


if __name__ == "__main__":
    main()
