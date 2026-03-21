# GIT GUIDE — RAG Demo Team

## First Time Setup (everyone does this once)

### Step 1 — Install Git
Download from https://git-scm.com/downloads and install.

### Step 2 — Configure your name and email
Open terminal and run:
```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### Step 3 — Accept the GitHub invitation
Dev 1 will share a GitHub link.
Check your email for the collaboration invite and accept it.

### Step 4 — Clone the project
```bash
git clone https://github.com/yourteam/rag-demo.git
cd rag-demo
```

### Step 5 — Create your branch

Dev 1 runs this:
```bash
git checkout -b dev1/rag-core
git push origin dev1/rag-core
```

Dev 2 runs this (AFTER Dev 1 pushes):
```bash
git checkout -b dev2/ui origin/dev1/rag-core
git push origin dev2/ui
```

Dev 3 runs this (AFTER Dev 1 pushes):
```bash
git checkout -b dev3/pipeline origin/dev1/rag-core
git push origin dev3/pipeline
```

---

## Every Single Day

### When you START working
```bash
git pull origin your-branch-name
```

Examples:
```bash
# Dev 1
git pull origin dev1/rag-core

# Dev 2
git pull origin dev2/ui

# Dev 3
git pull origin dev3/pipeline
```

### When you STOP working (or any time you want to save)
```bash
git add .
git commit -m "describe what you did"
git push origin your-branch-name
```

Examples:
```bash
# Dev 1
git add .
git commit -m "feat: completed loader.py and chunker.py"
git push origin dev1/rag-core

# Dev 2
git add .
git commit -m "feat: added file upload and chat input"
git push origin dev2/ui

# Dev 3
git add .
git commit -m "feat: completed logger.py"
git push origin dev3/pipeline
```

---

## Checking Your Status (run this anytime)
```bash
# See what files you changed
git status

# See which branch you are on
git branch

# See your commit history
git log --oneline
```

---

## The Only 5 Commands You Need

| Command | What it does |
|---|---|
| `git add .` | Stage all your changed files |
| `git commit -m "message"` | Save a snapshot with a description |
| `git push origin branch-name` | Upload your work to GitHub |
| `git pull origin branch-name` | Download latest from GitHub |
| `git checkout branch-name` | Switch to a different branch |

---

## Integration Day (Dev 1 does this alone)

When everyone is done and has pushed their branches:
```bash
# Step 1 — switch to main
git checkout main

# Step 2 — pull latest main
git pull origin main

# Step 3 — merge everyone's work
git merge dev1/rag-core
git merge dev2/ui
git merge dev3/pipeline

# Step 4 — push final version
git push origin main
```

Then tell Dev 2 and Dev 3 to run:
```bash
git checkout main
git pull origin main
```

Now everyone has the complete working project.

---

## Branch Rules — Read This Once
```
✅ Always work on YOUR branch only
✅ Always pull before you start working
✅ Always push before you stop working
✅ Commit often — at least once a day
✅ Write clear commit messages

❌ Never work directly on main
❌ Never edit files outside your folder
❌ Never push without committing first
❌ Never share your .env file
```

---

## Your Branch Names

| Person | Branch name | Folder they own |
|---|---|---|
| Dev 1 | dev1/rag-core | rag/, core/, main.py |
| Dev 2 | dev2/ui | ui/ |
| Dev 3 | dev3/pipeline | utils/, prompts/, data/ |

---

## What To Do If Something Goes Wrong

### "I edited the wrong file by mistake"
```bash
# Undo changes to a specific file
git checkout -- filename.py
```

### "I want to undo my last commit"
```bash
git revert HEAD
```

### "I don't know what branch I'm on"
```bash
git branch
# the branch with * next to it is your current branch
```

### "I got a merge conflict"
Don't panic. Just message Dev 1 on the group chat.
Dev 1 will fix it — that's what the integration lead is for.

---

## Commit Message Examples
```bash
# Good commit messages
git commit -m "feat: completed loader.py"
git commit -m "feat: added file upload to UI"
git commit -m "fix: fixed PDF parsing error"
git commit -m "wip: working on chunker, not done yet"
git commit -m "docs: updated README with setup steps"

# Bad commit messages
git commit -m "stuff"
git commit -m "changes"
git commit -m "aaa"
git commit -m "idk"
```

---

## Quick Reference Card
```
START OF DAY         END OF DAY
─────────────        ──────────────
git pull             git add .
                     git commit -m "what I did"
                     git push
```

---

## Group Chat Template

When you finish a file, message the team:
```
✅ Done: [filename]
Branch: [your branch name]
What it does: [one sentence]
Ready for: [who needs this next]

Example:
✅ Done: rag/retriever.py
Branch: dev1/rag-core
What it does: returns top-5 relevant chunks for any query
Ready for: Dev 3 can now build pipeline.py
```

This keeps everyone in sync without needing to check GitHub constantly.