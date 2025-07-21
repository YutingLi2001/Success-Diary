# Todo Update: Uncommitted Work Progress

## 🎯 Objective
Update `docs/planning/todo.md` to reflect **uncommitted work** from current session. Committed work is automatically considered complete.

## 🔒 Key Principle
✅ **Committed code = completed tasks** (no verification needed)
🔄 **Only focus on uncommitted changes** and newly discovered work

## 📋 Simple Process

### Step 1: Check Git Status
```bash
git status                    # See uncommitted changes
git log --oneline -n 3       # Check recent commits for completed tasks
```

### Step 2: Update Todo.md Based on Uncommitted Work
1. **Mark completed tasks**: If task appears in recent commits → mark `- [x]`
2. **Update incomplete tasks**: For uncommitted work, ask user about current status:
   - Still working on it? → leave `- [ ]`
   - Blocked on something? → mark `- [~] Task name (blocked: reason)`
   - Partially done? → add progress note `- [ ] Task name (current state: X)`

### Step 3: Add New Discovered Tasks
1. **Add new tasks** discovered during this session as `- [ ]` items
2. **Include timestamp**: `(added at HH:MM)` for context
3. **Focus on current feature**: Only add tasks related to today's work

### Step 4: Preserve Context for Tomorrow
For any incomplete work:
1. **Add brief context** about current state
2. **Note next steps** needed to continue
3. **Flag blockers** or dependencies

**Deliverable**: Updated todo.md reflecting current uncommitted work status.