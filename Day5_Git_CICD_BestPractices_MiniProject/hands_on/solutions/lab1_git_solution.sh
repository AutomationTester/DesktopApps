#!/usr/bin/env bash
# =============================================================================
# lab1_git_solution.sh - reference solution for Lab 1 (Git) - LOCAL parts
# =============================================================================
# Re-creates ONLY  hands_on/solutions/sandbox_repo/  and inside it:
#   my-automation-repo/   the trainee's repository     (Tasks 1-6)
#   teammate-clone/       a clone of it = "a colleague" (Task 7: clone/fetch/pull)
#
# Task 8 (push to YOUR GitHub repo) needs your account, so the commands are
# PRINTED at the end, never executed by this script.
#
# Run:    bash lab1_git_solution.sh          (Git Bash)
# Clean:  bash lab1_git_solution.sh --clean
# =============================================================================
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SANDBOX="$HERE/sandbox_repo"
[ "$(basename "$SANDBOX")" = "sandbox_repo" ] || { echo "unexpected path"; exit 1; }

rm -rf -- "$SANDBOX"
if [ "${1:-}" = "--clean" ]; then echo "cleaned $SANDBOX"; exit 0; fi
mkdir -p "$SANDBOX/my-automation-repo"
cd "$SANDBOX/my-automation-repo" || exit 1

export GIT_PAGER=cat GIT_EDITOR=true GIT_MERGE_AUTOEDIT=no
say() { echo; echo "---------- $* ----------"; }
run() { echo "\$ $*"; "$@"; }

# --- Task 1: init + config ---------------------------------------------------
say "Task 1: init and configure"
run git init -b main
run git config --local user.name  "Trainee Tester"
run git config --local user.email "trainee@example.com"

# --- Task 2: professional repo skeleton + first commit -----------------------
say "Task 2: skeleton, .gitignore, first commit"
mkdir -p tests config
cat > README.md <<'EOF'
# My Automation Repo
Desktop + CLI automation practice.
## Run
    pip install -r requirements.txt
    pytest -m cli
EOF
printf 'pytest>=8.0\npytest-html>=4.0\nPyYAML>=6.0\n' > requirements.txt
printf 'reports/\nlogs/\nscreenshots/\n__pycache__/\n.venv/\n.env\n' > .gitignore
cat > config/config.yaml <<'EOF'
default_env: dev
timeout: 10
EOF
cat > tests/test_smoke.py <<'EOF'
def test_truth():
    assert 1 + 1 == 2
EOF
mkdir -p reports && echo "<html/>" > reports/report.html   # must NOT be committed
run git status --short
run git add .
run git status --short                    # reports/ is absent -> .gitignore works
run git commit -m "chore: initial project skeleton"

# --- Task 3: diff and a second commit ----------------------------------------
say "Task 3: diff, second commit, log"
echo "retries: 2" >> config/config.yaml
run git diff
run git commit -am "feat(config): add retries setting"
run git log --oneline

# --- Task 4: feature branch + merge (--no-ff keeps the branch visible) -------
say "Task 4: feature branch and merge"
run git switch -c feature/cli-test
cat > tests/test_cli.py <<'EOF'
import subprocess, sys

def test_python_version_cli():
    out = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
    assert out.returncode == 0
EOF
run git add tests/test_cli.py
run git commit -m "test: add CLI version test"
run git switch main
run git merge --no-ff -m "Merge branch 'feature/cli-test'" feature/cli-test
run git branch -d feature/cli-test

# --- Task 5: merge conflict and resolution -----------------------------------
say "Task 5: create and resolve a merge conflict"
run git switch -c feature/timeout-qa
sed -i 's/^timeout: 10$/timeout: 30/' config/config.yaml
run git commit -am "feat(config): timeout 30 for slow QA machines"
run git switch main
sed -i 's/^timeout: 10$/timeout: 15/' config/config.yaml
run git commit -am "feat(config): timeout 15"
echo "\$ git merge feature/timeout-qa     # expected: CONFLICT"
git merge feature/timeout-qa || echo ">>> conflict, as planned"
run git diff --name-only --diff-filter=U  # list conflicted files
cat config/config.yaml
# Team decision: keep the bigger timeout (30)
cat > config/config.yaml <<'EOF'
default_env: dev
timeout: 30
retries: 2
EOF
run git add config/config.yaml
run git commit -m "merge: resolve timeout conflict (keep 30)"
run git branch -d feature/timeout-qa

# --- Task 6: rebase basics + tag ---------------------------------------------
say "Task 6: rebase a short-lived branch, then tag a release"
run git switch -c feature/docs
echo "## Branching: feature/* -> PR -> main" >> README.md
run git commit -am "docs: describe branching"
run git switch main
echo "# tests live in tests/" > tests/README.md   # someone else's change lands on main
run git add tests/README.md
run git commit -m "docs: tests folder readme"
run git switch feature/docs
run git rebase main                     # replay our commit on top of main -> linear history
run git switch main
run git merge --ff-only feature/docs    # fast-forward, no merge commit
run git branch -d feature/docs
run git tag -a v1.0.0 -m "Lab 1 release"
run git log --oneline --graph --decorate --all

# --- Task 7: clone / fetch / pull between two local folders ------------------
say "Task 7: a teammate clones, we commit, teammate fetches and pulls"
cd "$SANDBOX" || exit 1
run git clone my-automation-repo teammate-clone
cd "$SANDBOX/my-automation-repo" || exit 1
echo "log_level: INFO" >> config/config.yaml
run git commit -am "feat(config): add log_level"
cd "$SANDBOX/teammate-clone" || exit 1
run git remote -v                       # origin points to my-automation-repo
run git fetch origin                    # download, do NOT touch working files
run git status -sb                      # 'behind 1'
run git log --oneline main..origin/main # what is new on the remote
run git pull                            # fetch + merge (fast-forward here)
run git log --oneline -3

# --- Task 8: push to GitHub (printed only) -----------------------------------
say "Task 8: push to YOUR GitHub repository (run these yourself)"
cat <<'EOF'
  # 1. On github.com: New repository -> name: my-automation-repo -> NO README -> Create
  # 2. In my-automation-repo:
  git remote add origin https://github.com/<your-user>/my-automation-repo.git
  git push -u origin main          # first push sets 'upstream'
  git push origin v1.0.0           # tags are pushed separately (or: git push --tags)
  # 3. Refresh the GitHub page - commits, files and the tag are there.
EOF
echo
echo "Done. Sandbox: $SANDBOX"
