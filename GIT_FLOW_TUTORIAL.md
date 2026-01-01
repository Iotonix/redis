# Git Flow Tutorial - Interactive Learning Guide

Welcome! This tutorial will teach you Git Flow hands-on using your Redis project.

## What is Git Flow?

Git Flow is a branching model that defines a strict branching structure designed around project releases. It uses specific branch types for different purposes:

- **main** (or master): Production-ready code
- **develop**: Integration branch for features
- **feature/** branches: New features
- **release/** branches: Prepare for production release
- **hotfix/** branches: Quick fixes for production

## Prerequisites

Before starting, make sure you have:

- Git CLI installed ✓
- VSCode ✓
- PowerShell 7 ✓
- Python environment (activate with: `C:\Users\ralf\SRC\redis\.venv\Scripts\Activate.ps1`)

---

## Tutorial Structure

We'll go through a complete Git Flow cycle:

1. **Setup**: Initialize Git Flow branches
2. **Feature Development**: Add a new feature
3. **Release**: Prepare and deploy a release
4. **Hotfix**: Fix a critical bug in production

---

## Part 1: Initial Setup

### Step 1: Create the develop branch

Currently you're on `main`. Git Flow requires a `develop` branch.

**Command to run:**

```powershell
git checkout -b develop
```

This creates and switches to a new `develop` branch.

**Verify:**

```powershell
git branch
```

You should see both `main` and `develop` branches, with `develop` active (marked with *).

---

## Part 2: Feature Development

### Step 2: Create a feature branch

Let's add a statistics feature to track Redis operations.

**Command to run:**

```powershell
git checkout -b feature/statistics-tracker
```

This creates a feature branch from `develop`.

**Naming convention:** `feature/<descriptive-name>`

### Step 3: Implement the feature

I'll provide the code for a new `statistics.py` file. You can create it manually or I can create it for you.

After creating the file, check the status:

```powershell
git status
```

### Step 4: Commit the feature

Add and commit your changes:

```powershell
git add statistics.py
git commit -m "Add statistics tracker for Redis operations"
```

**Best practice:** Commit messages should be clear and descriptive.

### Step 5: Finish the feature (merge to develop)

Switch back to develop and merge the feature:

```powershell
git checkout develop
git merge feature/statistics-tracker
```

Delete the feature branch (cleanup):

```powershell
git branch -d feature/statistics-tracker
```

**Verify:**

```powershell
git branch
git log --oneline
```

---

## Part 3: Release Management

### Step 6: Create a release branch

When develop has enough features, create a release branch:

```powershell
git checkout -b release/1.0.0
```

**Naming convention:** `release/<version-number>`

### Step 7: Prepare the release

Update version numbers, documentation, etc. We'll update the README.

After making changes:

```powershell
git add README.md
git commit -m "Bump version to 1.0.0"
```

### Step 8: Finish the release

Merge to main (production):

```powershell
git checkout main
git merge release/1.0.0
git tag -a v1.0.0 -m "Release version 1.0.0"
```

Merge back to develop:

```powershell
git checkout develop
git merge release/1.0.0
```

Delete the release branch:

```powershell
git branch -d release/1.0.0
```

**Verify:**

```powershell
git tag
git log --oneline --graph --all
```

---

## Part 4: Hotfix (Emergency Bug Fix)

### Step 9: Create a hotfix branch

Hotfixes branch from `main` (not develop) because they fix production bugs.

```powershell
git checkout main
git checkout -b hotfix/fix-connection-timeout
```

**Naming convention:** `hotfix/<bug-description>`

### Step 10: Fix the bug

Make your fix (I'll provide example code).

```powershell
git add redis_tester.py
git commit -m "Fix connection timeout issue in Redis client"
```

### Step 11: Finish the hotfix

Merge to main:

```powershell
git checkout main
git merge hotfix/fix-connection-timeout
git tag -a v1.0.1 -m "Hotfix: connection timeout"
```

Merge to develop:

```powershell
git checkout develop
git merge hotfix/fix-connection-timeout
```

Delete the hotfix branch:

```powershell
git branch -d hotfix/fix-connection-timeout
```

---

## Part 5: Another Feature (Practice)

Let's practice the full cycle again with a second feature!

### Step 12: Create another feature

```powershell
git checkout develop
git checkout -b feature/retry-mechanism
```

### Step 13: Implement and commit

(I'll provide code for retry logic)

```powershell
git add redis_tester.py
git commit -m "Add retry mechanism for failed Redis operations"
```

### Step 14: Merge to develop

```powershell
git checkout develop
git merge feature/retry-mechanism
git branch -d feature/retry-mechanism
```

---

## Visual Overview

Here's what your Git history will look like:

```
* (main, tag: v1.0.1) Merge hotfix/fix-connection-timeout
* (develop) Merge feature/retry-mechanism
* Add retry mechanism
* Merge hotfix/fix-connection-timeout (to develop)
* Fix connection timeout
* (tag: v1.0.0) Merge release/1.0.0
* Bump version to 1.0.0
* Merge feature/statistics-tracker
* Add statistics tracker
* Initial commit
```

---

## Key Concepts Summary

### Branch Lifecycle:

1. **Feature**: `develop` → `feature/xxx` → `develop`
2. **Release**: `develop` → `release/x.x.x` → `main` + `develop`
3. **Hotfix**: `main` → `hotfix/xxx` → `main` + `develop`

### Important Rules:

- Never commit directly to `main`
- Never commit directly to `develop` (except merges)
- Always work in feature/release/hotfix branches
- Always merge releases and hotfixes to BOTH `main` AND `develop`
- Use tags for releases on `main`

---

## Common Commands Quick Reference

```powershell
# Check current branch
git branch

# Check status
git status

# View commit history
git log --oneline --graph --all

# View all branches including visual tree
git log --oneline --graph --decorate --all

# Switch branches
git checkout <branch-name>

# Create and switch to new branch
git checkout -b <branch-name>

# Merge branch into current branch
git merge <branch-name>

# Delete branch
git branch -d <branch-name>

# Create tag
git tag -a <tag-name> -m "message"

# View tags
git tag
```

---

## Test Your Python Code

Remember to activate your virtual environment first:

```powershell
C:\Users\ralf\SRC\redis\.venv\Scripts\Activate.ps1
```

Then run your code:

```powershell
python main.py
```

---

## Ready to Start?

Tell me when you're ready and I'll guide you through each step! Start with:

```powershell
git checkout -b develop
```

And let me know what you see!
