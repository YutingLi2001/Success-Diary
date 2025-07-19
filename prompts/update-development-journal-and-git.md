# update-development-journal-and-git

## Goal  
Update today's dev journal **and** execute complete Git workflow including committing and pushing current work to the appropriate branch.

---

## Inputs to Review  
1. `docs/planning/roadmap.md` – long‑term development path  
2. `docs/planning/todo.md` – today's completed tasks  
3. `docs/git-workflow.md` – branch strategy (if available, otherwise use default strategy)

---

## Required Outputs

### A. Journal Entry  
Append **one** entry to `docs/logs/development-journal.md` following all rules in `update-development-journal.md`:  
- ≤ 200 words  
- Human‑centred, high‑level, no deep tech details  
- Use the exact header & section template below  
- Auto-increment the Dev Log number  
- Place the entry after the file header but before previous entries (chronological order)

### B. Git Action Plan & Execution  
Based on roadmap + today's todo + git-workflow.md:  
1. Decide which **branch** today's work should be pushed to  
2. If none fits, propose a new branch (e.g., `feature/<kebab-case-name>`) and explain why  
3. **Execute the complete Git workflow**: commit changes and push to appropriate branch  
4. Provide **Git CLI commands** with brief rationale after each command

---

## Step-by-Step for Claude Code

1. Load the 3 input files listed above  
2. Review what progress was made today (todo.md)  
3. Cross-check against the roadmap to understand what features or milestones progressed  
4. Draft a **journal entry** using the template below  
5. Review the current git branch strategy (or use default if git-workflow.md unavailable)  
6. Decide the correct branch to push work to  
7. If needed, create a new branch based on the rules in git-workflow.md  
8. **Execute git workflow** (run all commands that apply to current situation):  
   - Switch/create branch (if needed)
   - Stage all changes (`git add .`)
   - Commit changes with descriptive message
   - **Push to origin** with upstream tracking
   - Create pull request (if needed)
   - (Optional) Merge  
9. Justify each decision briefly  
10. Include rollback plan if git operations fail  

---

## Journal Entry Template

### Header Format
```
## YYYY-MM-DD – Dev Log #X: [Brief Session Title]
```

### Section 1: Focus
```
### Focus
[Single sentence describing session's main objective or theme]
```

### Section 2: Progress
```
### Progress
- [Brief accomplishment 1]
- [Brief accomplishment 2] 
- [Brief accomplishment 3] (if applicable)
```

### Section 3: Next Steps (Optional)
```
### Next Steps
- [Next priority 1]
- [Next priority 2]
```

## Writing Guidelines

### Keep It Concise
- **Single sentences** for most points
- **No technical implementation details**
- **Focus on outcomes**, not process
- **Skip obvious or minor details**

### Human-Centered Content
- Planning decisions made
- Architecture choices reviewed
- Workflow improvements
- Strategic insights
- Process observations

### What to AVOID
- Detailed coding explanations
- Technical troubleshooting steps
- Library/framework specifics
- File structure details
- Configuration minutiae

## Example Entry (98 words)
```
## 2025-07-15 – Dev Log #6: OAuth Integration

### Focus
Complete OAuth authentication and fix redirect issues.

### Progress
- Reviewed OAuth flow architecture and approved implementation approach
- Tested authentication end-to-end with successful user verification
- Resolved redirect bug through configuration review
- Validated email verification integration with Mailpit

### Next Steps
- Test production deployment configuration
- Review user onboarding flow
```

## Git Branch Decision
Target branch: <branch-name>
Reason: <one sentence summary>

## Git Commands
```bash
# Only execute commands that apply to your current situation:
git checkout <base-branch>                    # Reason: switch to base branch
git pull origin <base-branch>                 # Reason: update to latest base state
git checkout -b <new-branch>                  # Reason: create new feature branch (if needed)
git add .                                      # Reason: stage all current work
git commit -m "<type>: <message>"             # Reason: descriptive commit message
git push -u origin <branch-name>              # Reason: push branch and track upstream (REQUIRED)
gh pr create --base <target> --title "<title>" --body "<summary>"  # Reason: initiate review process
```

## Rollback Plan
```bash
# If git operations fail:
git reset --soft HEAD~1                       # Undo last commit (keep changes staged)
git checkout <original-branch>                # Return to original branch
git branch -D <failed-branch>                 # Delete failed branch (if created)
```


---

## Verification Checklist

- ✅ Journal entry ≤ 200 words  
- ✅ Total output prompt ≤ 600 words  
- ✅ Branching logic aligns with `docs/git-workflow.md`  
- ✅ File paths verified:  
  - `docs/planning/roadmap.md`  
  - `docs/planning/todo.md`  
  - `docs/logs/development-journal.md`  
  - `docs/git-workflow.md` (or fallback to default strategy)

---
