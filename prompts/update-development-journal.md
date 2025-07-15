# Development Journal Update Prompt

## Instructions
Please add a **concise** development journal entry to `docs/logs/development-journal.md` using the structure below.

## CRITICAL REQUIREMENTS
- **Maximum 200 words total** (aim for under 100 words)
- **Minimal technical details** - focus on high-level progress
- **Human perspective** - decisions, planning, insights, not coding specifics

## User Must Provide
- **Date**: Session date and time range
- **Focus**: Primary objectives or theme
- **Key accomplishments**: What was achieved

## Required Entry Structure

### Header Format
```
## YYYY-MM-DD (time range) – Dev Log #X: [Brief Session Title]
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
## 2025-07-15 (2:00-4:00 PM) – Dev Log #6: OAuth Integration

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

## Example Usage
*User says:* "Read the prompt in `prompts/update-development-journal.md` and update the journal for today's 90-minute session focused on database optimization where we improved query performance and updated the user model."

*Claude creates:* Brief, focused entry following the concise format above.