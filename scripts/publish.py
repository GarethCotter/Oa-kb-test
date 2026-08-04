"""Publish a content change: rebuild, check, commit, push.

No shebang line, deliberately, and it matches build.py and checks.py. The Windows
py launcher reads shebangs, so "#!/usr/bin/env python" sends it looking for
`python` on PATH - which on a normal Windows machine is the Microsoft Store stub,
and the script dies with "Python was not found" before running a line.

    py scripts/publish.py "Corrected the reviewer assignment steps"

Written for the way the help centre is actually edited now - somebody describes a
change to Claude, Claude edits the markdown, and then this runs. It exists so that
the three things that must happen in order cannot happen out of order, or partly:

  1. Rebuild. The site is served from committed HTML. Editing corpus/*.md and
     pushing without rebuilding publishes nothing - the change is in the repo and
     invisible on the site, which looks exactly like the edit not working.
  2. Check. All the standing checks must pass. If any fails, nothing is committed
     and nothing is pushed. A broken link is easier to fix before it is live.
  3. Commit and push. main deploys automatically, so this is the publish step.

Nothing is pushed unless every check passes. There is no --force and there should
not be one: the way to publish past a failing check is to fix the check.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def run(cmd, capture=False):
    return subprocess.run(cmd, cwd=ROOT, shell=isinstance(cmd, str),
                          capture_output=capture, text=True)


def out(cmd):
    return run(cmd, capture=True).stdout.strip()


def main():
    args = [a for a in sys.argv[1:] if a != "--dry-run"]
    # --dry-run goes as far as the checks and stops before touching git. Added
    # after a "let's just test the guards" run committed and pushed for real,
    # because the working tree was not as clean as assumed.
    dry = "--dry-run" in sys.argv[1:]
    message = " ".join(args).strip()
    if not message and not dry:
        sys.exit('Say what changed, in quotes:\n    py scripts/publish.py "what you changed"')

    if not (ROOT / "build.py").exists():
        sys.exit("Run this from the help centre repository.")

    branch = out(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    print(f"Branch: {branch}")
    if branch == "main":
        print("main is the live site - this will publish.\n")

    print("1/4  Rebuilding the pages from the markdown...")
    if run([sys.executable, "build.py"]).returncode != 0:
        sys.exit("\nThe build failed. Nothing has been committed or pushed.")

    print("\n2/4  Running the checks...")
    if run([sys.executable, "scripts/checks.py"]).returncode != 0:
        sys.exit("\nA check failed, so nothing has been committed or pushed.\n"
                 "Fix what it reported and run this again. Your edits are still here.")

    print("\n3/4  Recording the change...")
    if not out(["git", "status", "--porcelain"]):
        print("Nothing has changed - there is nothing to publish.")
        return
    print(out(["git", "status", "--short"]))
    if dry:
        print("\n--dry-run: stopping here. Nothing committed, nothing published.")
        return
    run(["git", "add", "-A"])
    if run(["git", "commit", "-m", message]).returncode != 0:
        sys.exit("\nThe commit failed. Nothing has been pushed.")

    print("\n4/4  Publishing...")
    if run(["git", "push"]).returncode != 0:
        sys.exit("\nThe push failed - the change is committed here but not published.\n"
                 "Usually this means someone else changed the site too. Ask Claude to "
                 "'pull and try publishing again'.")

    print("\nDone. The site rebuilds itself within about a minute.")
    print("Look at https://help.oxfordabstracts.com to see it.")


if __name__ == "__main__":
    main()
