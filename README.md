# Smart PR Checks with Automated PullRequest Linter (GitHub Actions)

This project helps teams write better pull requests by checking titles, descriptions, and labels automatically.
It gently reminds contributors to follow a standard format and gives helpful feedback if something is missing or unclear.

---

## Why This Project?

A good pull request tells a clear story:  
- What changed  
- Why it changed  
- How it was tested  
- Which issue it solves

This linter encourages all of that.

---

## What It Does

Whenever someone opens or updates a pull request, this linter:

- Checks if the PR **title** is long enough and descriptive
- Makes sure the **description** has all required sections
- Verifies if either **"Risk: Low"** or **"Risk: High"** label is added
- Detects if the description is just empty lines or bullet points
- Skips checks for **draft PRs** until they’re marked ready
- Adds a comment with all issues found
- Fails the check if required info is missing

---

## Technology Used

- [GitHub Actions](https://docs.github.com/en/actions)  
- Python 3.x  
- GitHub REST API  
- Markdown (for the PR template)

---

## Files in This Repo

```
.github/
├── workflows/
│   └── pr-lint.yml          → GitHub Actions workflow
└── pull_request_template.md → Pre-filled PR description format

scripts/
└── pr_linter.py             → Python script that runs validations
```

---

## Pull Request Template Preview

Every new PR starts with this:

```md
### 1. Issue
Closes:
Related:

### 2. Description of change
-
-

### 3. Testing that was done
- [ ] Unit tests
- [ ] Manual testing
      
### 4. Don’t forget
Before merging:
- [ ] Review approved
- [ ] Docs updated
      
### 5. Additional Notes
- 
```

---

## What It Catches

- ❌ PR title is too short or copied from the branch name  
- ❌ PR has no risk label (`Risk: Low` or `Risk: High`)  
- ❌ Missing or vague issue references  
- ❌ Description has only dots or empty lines  
- ❌ Required sections like `Issue` or `Description of change` are missing  
- ⚠️ Optional sections like `Testing` , `Don’t forget` or `Additional Notes` are skipped

---

## Future Ideas

- Auto-suggest title and description based on changed files 
- Enforce title formats like `doc:`, `fix:`, etc.
- Link Multiple PRs
- Issue/ Ticket reference can be slack discussion too 
- Let reviewers override checks in emergencies (but still fix later)
Auto-suggest title and description based on changed files

---

## How to Add This to Another Repo

1. Copy these files:
    - `.github/workflows/pr-lint.yml`  
    - `.github/pull_request_template.md`  
    - `scripts/pr_linter.py`  

2. Enable GitHub Actions and Modify Action --> General Settings accordingly

3. That’s it — the linter will run on every pull request.

To customize:
- Edit the PR template to match your team’s needs
- Change rules inside `pr_linter.py` (e.g. title length, section names)

---

## Built With Care  
By **Snigdha Kanchana**  
April–May 2025
