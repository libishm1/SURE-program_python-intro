# GitHub Workflow — a beginner's cheat sheet

How to save your work and send it to GitHub. Written for this repo
(**SURE-program_python-intro**), but it works for any project.

> **The one-line mental model:** you edit files → **stage** the changes you want
> to keep (`add`) → **save a snapshot** with a message (`commit`) → **upload** it
> to GitHub (`push`).

```
   edit files        git add        git commit         git push
  (your folder)  ──►  (staged)  ──►  (saved locally) ──► (on GitHub)
```

---

## The everyday loop (you'll use this 95% of the time)

After you've changed some files:

```bash
git add -A                       # stage ALL your changes
git commit -m "describe what you changed"   # save a snapshot with a message
git push                         # upload to GitHub
```

That's it. Three commands, every time you want to save progress online.

### Example

```bash
git add -A
git commit -m "Add zig-zag toolpath strategy"
git push
```

---

## What each command does

| Command | What it does |
|---------|--------------|
| `git status` | Shows what changed and what's staged. **Run this often** — it tells you where you are. |
| `git add <file>` | Stage one file (e.g. `git add README.md`). |
| `git add -A` | Stage **everything** that changed (new, edited, deleted files). |
| `git commit -m "msg"` | Save a snapshot of the staged changes, with a short message. |
| `git push` | Send your commits up to GitHub. |
| `git pull` | Bring down changes others (or you, on another computer) pushed. |
| `git log --oneline` | See the history of commits. |

---

## Checking before you commit (good habit)

```bash
git status        # which files changed?
git diff          # what exactly changed inside them? (press q to exit)
```

Then stage and commit only when you're happy:

```bash
git add -A
git commit -m "Fix reach margin in placement optimiser"
git push
```

---

## Writing good commit messages

A commit message says **what changed and why**, in the present tense.

- ✅ `Add zig-zag toolpath on the dome`
- ✅ `Invert paraboloid and place it on the table`
- ✅ `Fix base-pan swing so the arm stops dancing`
- ❌ `stuff`, `update`, `asdf`  ← future-you won't know what these mean

---

## First-time-only setup (already done for this repo)

You only do these **once per new project**. They're here for reference / your
next repo:

```bash
git init                                 # turn a folder into a git repo
git add -A
git commit -m "first commit"
git branch -M main                       # name the main branch "main"
git remote add origin https://github.com/<you>/<repo>.git   # link to GitHub
git push -u origin main                  # first push (the -u remembers the link)
```

After that first `git push -u`, every later upload is just `git push`.

### Tell git who you are (once per computer)

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
```

---

## Common situations

**I made a typo in my last commit message** (before pushing):
```bash
git commit --amend -m "the corrected message"
```

**I staged a file by mistake** (before committing):
```bash
git restore --staged <file>     # unstage it (keeps your edits)
```

**Someone else pushed; my push was rejected:**
```bash
git pull        # get their changes first
git push        # then send yours
```

**I want to see what I'm about to push:**
```bash
git log origin/main..HEAD --oneline    # commits you have that GitHub doesn't
```

---

## Quick reference card

```bash
# --- save & upload (daily) ---
git status                 # what changed?
git add -A                 # stage everything
git commit -m "message"    # snapshot it
git push                   # upload

# --- get updates ---
git pull                   # download others' changes

# --- look around ---
git log --oneline          # history
git diff                   # uncommitted changes
```

---

See the main [README](README.md) for what's in this repository.
