# Git Workflow Strategy - Success Diary

## Overview
This document defines the version control strategy aligned with our development roadmap phases. The workflow balances development speed with code stability, supporting both rapid AI-assisted development and production deployment requirements.

## Branch Strategy

### Core Branches

#### `main` (Production-Ready)
- **Purpose**: Stable, production-ready code only
- **Protection**: Protected branch with required reviews
- **Deploy Target**: Production AWS environment (post-August 17, 2025)
- **Merge Source**: Only from `develop` branch via Pull Requests
- **Naming**: `main` (GitHub default)

#### `develop` (Integration Branch)
- **Purpose**: Integration branch for completed features
- **Stability**: Should always be functional but may have minor bugs
- **Deploy Target**: Development/staging environment
- **Merge Source**: Feature branches via Pull Requests
- **Naming**: `develop`

### Feature Branches

#### MVP 1.0 Feature Branches
Based on current roadmap priorities:

- `feature/entry-editing` - Edit historical entries functionality
- `feature/entry-titles` - Custom titles with auto-generated fallback
- `feature/dynamic-ui` - Progressive field display
- `feature/form-validation` - Enhanced validation and error handling
- `feature/mobile-responsive` - Mobile optimization
- `feature/history-enhancement` - Enhanced history view (Date|Title|Rating table)

#### Version 2.0+ Feature Branches (Future)
- `feature/health-tracking` - Health modules implementation
- `feature/diet-tracking` - Diet tracking light/standard modes
- `feature/exercise-tracking` - Exercise logging functionality
- `feature/sleep-tracking` - Sleep duration and quality tracking

#### Infrastructure Branches
- `feature/aws-deployment` - Production deployment setup
- `feature/postgresql-migration` - Database migration from SQLite
- `feature/email-production` - Production email service integration

### Hotfix Branches
- `hotfix/critical-bug-name` - Critical production fixes
- Merged directly to `main` and back-merged to `develop`

## Workflow Process

### 1. Daily Development Workflow

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/entry-editing

# Work on feature
# ... make changes ...
git add .
git commit -m "implement entry editing core functionality

- Add edit route for historical entries
- Implement entry update validation
- Add edit button to history view

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push feature branch
git push -u origin feature/entry-editing
```

### 2. Feature Completion Workflow

```bash
# Create Pull Request (using GitHub CLI)
gh pr create --title "Add entry editing functionality" --body "$(cat <<'EOF'
## Summary
- Implements full editing capability for historical entries
- Adds entry update validation and error handling
- Integrates edit functionality with existing history view

## Changes
- New edit route in app/main.py
- Entry update validation in models
- Edit button and form in history template
- Enhanced error handling for concurrent edits

## Test Plan
- [ ] Edit historical entries successfully saves changes
- [ ] Validation prevents invalid data submission
- [ ] Edit button appears correctly in history view
- [ ] Form pre-fills with existing entry data

🤖 Generated with Claude Code
EOF
)"

# Merge after review
gh pr merge --squash
```

### 3. Release Preparation Workflow

```bash
# Prepare release from develop to main
git checkout develop
git pull origin develop

# Create release branch
git checkout -b release/mvp-1.0
git push -u origin release/mvp-1.0

# Final testing and bug fixes on release branch
# ... fix any issues ...

# Create Pull Request to main
gh pr create --base main --title "Release MVP 1.0" --body "$(cat <<'EOF'
## MVP 1.0 Release

### ✅ Completed Features
- Entry editing for historical entries
- Custom entry titles with auto-generated fallback
- Dynamic UI with progressive field display
- Enhanced form validation and error handling
- Mobile-responsive design optimization
- Enhanced history view with Date|Title|Rating table

### 🧪 Testing
- [ ] All MVP features functional
- [ ] Cross-platform compatibility verified
- [ ] Database schema stable
- [ ] No critical bugs detected

### 📊 Success Criteria Met
- [ ] Core emotional reflection workflow complete
- [ ] User experience polished and intuitive
- [ ] Ready for production deployment preparation

🤖 Generated with Claude Code
EOF
)"
```

## Branch Naming Conventions

### Feature Branches
- **Format**: `feature/brief-description`
- **Examples**: 
  - `feature/entry-editing` (implements entry editing)
  - `feature/mobile-responsive` (mobile optimization)
  - `feature/aws-deployment` (production deployment)

### Hotfix Branches
- **Format**: `hotfix/brief-description`
- **Examples**:
  - `hotfix/login-redirect-loop` (fixes authentication bug)
  - `hotfix/database-connection-timeout` (fixes DB connection issues)

### Release Branches
- **Format**: `release/version-name`
- **Examples**:
  - `release/mvp-1.0` (MVP 1.0 release preparation)
  - `release/v2.0-health-tracking` (Version 2.0 release)

## Commit Message Standards

### Format
```
type: brief description in lowercase

- Detailed change 1
- Detailed change 2
- Detailed change 3

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Commit Types
- **feat**: New feature implementation
- **fix**: Bug fixes
- **refactor**: Code restructuring without functionality changes
- **docs**: Documentation updates
- **style**: Formatting, missing semicolons, etc.
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates

### Examples
```bash
# Feature commit
git commit -m "feat: add entry editing functionality

- Implement edit route for historical entries
- Add entry update validation
- Create edit form template
- Handle concurrent edit scenarios

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Bug fix commit
git commit -m "fix: resolve mobile responsive layout issues

- Fix entry form width on mobile devices
- Correct button spacing on small screens
- Improve touch target sizes for mobile

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## Development Phase Alignment

### Current Phase: MVP 1.0 Development
**Active Branches**:
- `main` (stable foundation)
- `develop` (MVP integration)
- `feature/entry-editing` (current priority)
- `feature/entry-titles` (next priority)
- `feature/dynamic-ui` (next priority)

**Workflow**:
1. Create feature branches from `develop`
2. Complete individual MVP features
3. Merge to `develop` via Pull Requests
4. Test integrated functionality
5. Prepare release branch for production deploy

### Future Phase: Production Deployment
**Additional Branches**:
- `release/mvp-1.0` (pre-production testing)
- `feature/aws-deployment` (infrastructure setup)
- `feature/postgresql-migration` (database transition)

### Future Phase: Version 2.0+ Development
**Expanded Strategy**:
- Long-running feature branches for major modules
- `feature/health-tracking` (umbrella for health features)
- Sub-branches: `feature/diet-tracking`, `feature/exercise-tracking`

## Pull Request Standards

### Template
```markdown
## Summary
Brief description of changes and motivation

## Changes Made
- Specific change 1
- Specific change 2
- Specific change 3

## Testing
- [ ] Manual testing completed
- [ ] Cross-platform compatibility verified
- [ ] Database schema changes tested
- [ ] No breaking changes introduced

## Documentation
- [ ] Code comments added where needed
- [ ] Documentation updated if applicable
- [ ] CLAUDE.md updated if workflow changes

## Reviewer Notes
Any specific areas that need attention during review

🤖 Generated with Claude Code
```

### Review Requirements
- **MVP Features**: Self-review with AI assistance (solo development)
- **Production Releases**: Thorough testing checklist completion
- **Breaking Changes**: Extra validation and documentation

## Emergency Procedures

### Hotfix Process
```bash
# Critical bug in production
git checkout main
git pull origin main
git checkout -b hotfix/critical-login-issue

# Fix the issue
# ... make minimal changes ...
git commit -m "hotfix: resolve critical login redirect loop

- Fix authentication redirect logic
- Add error handling for edge cases
- Restore proper user flow

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"

# Deploy to production
git checkout main
git merge hotfix/critical-login-issue
git push origin main

# Back-merge to develop
git checkout develop
git merge main
git push origin develop

# Clean up
git branch -d hotfix/critical-login-issue
git push origin --delete hotfix/critical-login-issue
```

### Rollback Process
```bash
# If deployment fails, rollback main
git checkout main
git reset --hard HEAD~1  # Go back one commit
git push --force-with-lease origin main
```

## Branch Protection Rules

### Main Branch
- Require pull request reviews
- Require status checks to pass
- Require branches to be up to date before merging
- Restrict pushes that create files larger than 100 MB
- Require signed commits (recommended for production)

### Develop Branch
- Require pull request reviews (can be bypassed for urgent fixes)
- Allow force pushes (for development flexibility)
- Delete head branches automatically after merge

## Tools and Automation

### Recommended GitHub CLI Commands
```bash
# Quick PR creation
gh pr create --title "feat: implement feature name" --body-file pr-template.md

# View PR status
gh pr status

# Merge with squash
gh pr merge --squash --delete-branch

# Create release
gh release create v1.0.0 --title "MVP 1.0 Release" --notes-file release-notes.md
```

### Git Aliases (Optional)
```bash
# Add to ~/.gitconfig
[alias]
    co = checkout
    br = branch
    ci = commit
    st = status
    cp = cherry-pick
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
    tree = log --graph --pretty=format:'%h -%d %s (%cr) <%an>' --abbrev-commit
```

## Migration from Current State

### Step 1: Create Develop Branch
```bash
git checkout -b develop
git push -u origin develop
```

### Step 2: Protect Main Branch
1. Go to GitHub repository settings
2. Navigate to Branches
3. Add protection rule for `main`
4. Enable "Require pull request reviews"

### Step 3: Start Feature Development
```bash
# Begin with highest priority MVP feature
git checkout develop
git checkout -b feature/entry-editing
# ... continue with feature development
```

## Success Metrics

### Development Velocity
- **Target**: Complete MVP 1.0 features within 8-10 hours
- **Measure**: Time from feature branch creation to merge
- **Goal**: Maintain AI-assisted development speed while improving code quality

### Code Quality
- **Target**: Zero critical bugs in production
- **Measure**: Issues reported post-deployment
- **Goal**: Comprehensive testing before release merges

### Process Adoption
- **Target**: 100% feature work done in feature branches
- **Measure**: Commits directly to main (should be 0 after transition)
- **Goal**: Smooth workflow adoption without development speed loss

---

## Quick Reference

### Common Commands
```bash
# Start new feature
git checkout develop && git pull origin develop && git checkout -b feature/name

# Update feature branch with latest develop
git checkout feature/name && git merge develop

# Create PR
gh pr create --title "feat: description" --body "Brief description"

# Merge PR
gh pr merge --squash --delete-branch

# Deploy to production
git checkout main && git merge develop && git push origin main
```

### Branch Status Quick Check
```bash
# View all branches
git branch -a

# See commit differences
git log develop..main --oneline
git log feature/branch-name..develop --oneline
```

*Last updated: 2025-07-15*  
*This workflow supports the Success Diary roadmap phases and production deployment requirements.*