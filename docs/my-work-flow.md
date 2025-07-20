three critical files：
"C:\Users\Yuting\Projects\Success-Diary\docs\planning\todo.md"：simple todo list for today, tasks pulled from roadmap
"C:\Users\Yuting\Projects\Success-Diary\docs\planning\roadmap.md": overall tasks needed to complete for this project. 
"C:\Users\Yuting\Projects\Success-Diary\docs\requirements\product-requirements.md" - overview of the entire project 

work flow:
start: empty what has been completed already, pull today's tasks from roadmap to todo. Roadmap has pre-identified tasks ordered based on priority, we always pull the ones with highest priority. But if needed to do breakdown to make sure 
during: update during development to todo, if tasks completed, we put tick, if new tasks created, we add onto todo.
finish: we sync road map with what we have finished with todo we do not put any technical details into our roadmap. We update development journal with the progress we made and eventually we do git related operations. 

Q: how much work should we be pulling from roadmap?
A: We follow a Vertical Slice development model, meaning that each task or feature we work on is developed end-to-end across all relevant layers of the system—from database to backend logic to frontend UI—so that the system becomes immediately usable, testable, and incrementally deliverable after each slice is complete.

In this model, we don’t just build isolated components (e.g., only the database or only the frontend). Instead, we aim to complete a full user-visible functionality that is:

Usable: the user can interact with it through the actual UI

Testable: it can be manually tested or validated end-to-end

Standalone: it does not rely on unfinished parts of the system to function

Incremental: the product improves visibly with each completed slice

For example, instead of building just the timezone database schema today and the UI next week, we build everything needed to allow a user to view, edit, and save their timezone setting, and validate that it works as expected in the real environment.

This approach aligns closely with agile principles and ensures we always have a working, testable system at the end of each development cycle, no matter how small the change.

## Emergency Snapshot Format

If Claude Code becomes unstable or the session is interrupted unexpectedly, manually add an Emergency Snapshot to todo.md:

```markdown
# Emergency Snapshot - YYYY-MM-DD HH:MM

## Current Feature: [feature name]

### Completed Tasks (tested and working)
- [x] Task A description (tested, working)
- [x] Task B description (tested, working)

### Partially Complete Tasks  
- [~] Task C description (coded but not tested)
- [~] Task D description (80% complete - needs UI polish)

### Incomplete Tasks
- [ ] Task E description (started but blocked on X)
- [ ] Task F description (not started)

### Context Notes
- Current implementation approach: [brief notes]
- Known issues: [any problems discovered]
- Next steps: [what to tackle next]
- Integration points: [dependencies on other features]
```

Upon recovery, use `session-recovery.md` prompt to analyze git history + Emergency Snapshot and reconstruct session state.