# Git Workflow Strategy - Success Diary

## ✅ Status: Branch Structure Complete (July 15, 2025)

**All branches created and ready for development:**
- Core branches: `main`, `develop` 
- MVP 1.0 features: 6 feature branches ready
- Infrastructure: `feature/aws-deployment` ready
- **Next step**: Begin development with `git checkout feature/entry-editing`

## Overview
This document defines the version control strategy aligned with our development roadmap phases. The workflow balances development speed with code stability, supporting both rapid AI-assisted development and production deployment requirements.

## Branch Strategy

### Core Branches

#### `main` (Production-Ready)
- **Purpose**: Stable, production-ready code only
- **Protection**: Protected branch with required reviews
- **Deploy Target**: Production AWS environment (post-August 17, 2025)
- **Merge Source**: Only from release branches via Pull Requests
- **Naming**: `main` (GitHub default)

#### `develop` (Integration Branch)
- **Purpose**: Integration branch for completed release phases
- **Stability**: Should always be functional but may have minor bugs
- **Deploy Target**: Development/staging environment
- **Merge Source**: Release branches via Pull Requests
- **Naming**: `develop`

### Release Branches (Major Phases)

#### `release/mvp-1.0-foundation` - Foundational Systems
- **Purpose**: All foundational systems that enable core features
- **Includes**: Error handling, validation, timezone handling, mobile responsive foundation
- **Dependencies**: None (foundational layer)
- **Merge Target**: `develop` when foundation complete

#### `release/mvp-1.0-core` - Core Features
- **Purpose**: Main user-facing functionality for MVP
- **Includes**: Entry management, dynamic UI, history enhancements
- **Dependencies**: Foundation phase must be complete
- **Merge Target**: `develop` when core features complete

#### `release/mvp-1.0-production` - Production Deployment
- **Purpose**: Infrastructure and deployment preparation
- **Includes**: AWS setup, database migration, production configuration
- **Dependencies**: Foundation and core phases complete
- **Merge Target**: `main` for production deployment

### Feature Branches (Multi-Feature Approach)

#### Foundation Phase Feature Branches
- `feature/form-validation` ✅ **COMPLETED** - Enhanced validation, error handling, script organization
- `feature/timezone-handling` - User timezone detection, settings, and display logic
- `feature/mobile-responsive` - Mobile optimization and responsive design foundation

#### Core Phase Feature Branches
- `feature/entry-management` - Entry editing, titles, archive system, draft/autosave
- `feature/dynamic-ui` - Progressive field display, user feedback systems, UX enhancements
- `feature/history-enhancement` - Enhanced history view, sorting, search functionality

#### Production Phase Feature Branches
- `feature/aws-deployment` - Production infrastructure setup, database migration, email service

#### Version 2.0+ Feature Branches (Future)
- `feature/health-tracking` - Complete health modules (diet, exercise, sleep, productivity)
- `feature/advanced-analytics` - Data visualization, insights, export functionality
- `feature/custom-fields` - User-defined fields and advanced customization

### Hotfix Branches
- `hotfix/critical-bug-name` - Critical production fixes
- Merged directly to `main` and back-merged to `develop`

## Workflow Process

### 1. Phase-Based Development Workflow

```bash
# Start new feature within a release phase
git checkout release/mvp-1.0-foundation
git pull origin release/mvp-1.0-foundation
git checkout -b feature/timezone-handling

# Work on feature (may include multiple related components)
# ... implement timezone detection ...
# ... add settings UI ...
# ... update date display logic ...
git add .
git commit -m "implement timezone handling system

- Add browser timezone detection with fallback
- Create user settings for manual timezone override
- Update all date displays to use user timezone
- Add timezone persistence to user model

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

# Push feature branch
git push -u origin feature/timezone-handling
```

### 2. Feature Completion Workflow

```bash
# Create Pull Request to release branch (using GitHub CLI)
gh pr create --base release/mvp-1.0-foundation --title "Complete timezone handling system" --body "$(cat <<'EOF'
## Summary
- Implements comprehensive timezone handling for global users
- Adds browser detection with manual override capability
- Updates all date/time displays to respect user timezone
- Provides foundation for entry titles and history sorting

## Multi-Feature Changes
- Browser timezone detection with Intl.DateTimeFormat API
- User settings UI for manual timezone selection
- Database schema updates for timezone preferences
- Date display logic updated across all templates
- Timezone-aware entry title generation preparation

## Test Plan
- [ ] Timezone detection works across different browsers
- [ ] Manual timezone override saves and persists
- [ ] All date displays reflect user timezone correctly
- [ ] Settings UI is intuitive and accessible
- [ ] Foundation ready for entry titles feature

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

### Current Phase: MVP 1.0 Foundation (🔄 In Progress)
**Active Release Branches**:
- ✅ `main` (stable foundation with comprehensive documentation)
- ✅ `develop` (phase integration branch)
- ✅ `release/mvp-1.0-foundation` (foundational systems development)
- 📋 `release/mvp-1.0-core` (will be created after foundation complete)
- 📋 `release/mvp-1.0-production` (will be created after core complete)

**Foundation Phase Status**:
- ✅ `feature/form-validation` (COMPLETED - validation + script organization)
- 🔄 `feature/timezone-handling` (NEXT PRIORITY - user timezone system)
- 📋 `feature/mobile-responsive` (PLANNED - responsive design foundation)

**Phase Workflow**:
1. ✅ Foundation release branch created from `develop`
2. 🔄 Complete foundational features (form validation DONE, timezone handling NEXT)
3. 📋 Integrate foundation phase to `develop` when complete
4. 📋 Begin core phase with entry management features
5. 📋 Final production phase for AWS deployment

### Future Phase: Production Deployment
**Additional Branches**:
- `release/mvp-1.0` (pre-production testing - will be created when MVP features complete)
- ✅ `feature/aws-deployment` (infrastructure setup - ready for development)
- `feature/postgresql-migration` (database transition - will be created when needed)

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

## 🔄 Branch Structure Evolution

### Current Multi-Feature Branch Structure (Updated 2025-07-17)

**Core Branches:**
- ✅ `main` - Production-ready code with comprehensive documentation
- ✅ `develop` - Phase integration branch

**Foundation Phase (🔄 In Progress):**
- ✅ `release/mvp-1.0-foundation` - Foundational systems development
- ✅ `feature/form-validation` - **COMPLETED** (validation + error handling + script organization)
- 🔄 `feature/timezone-handling` - **NEXT** (timezone detection + settings + display logic)
- 📋 `feature/mobile-responsive` - **PLANNED** (responsive foundation + mobile optimization)

**Core Phase (📋 Planned):**
- 📋 `release/mvp-1.0-core` - Core feature development (created after foundation)
- 📋 `feature/entry-management` - Entry editing + titles + archive + drafts
- 📋 `feature/dynamic-ui` - Progressive display + feedback + UX enhancements
- 📋 `feature/history-enhancement` - Sorting + search + enhanced views

**Production Phase (📋 Future):**
- 📋 `release/mvp-1.0-production` - Production deployment preparation
- 📋 `feature/aws-deployment` - Infrastructure + migration + production config

**Branch Status:**
- ✅ Hierarchical release structure implemented
- ✅ Multi-feature approach adopted for realistic development
- ✅ Foundation phase active with form validation completed
- 🔄 Ready for timezone handling development

### Next Steps: Start Development

```bash
# Begin with highest priority MVP feature
git checkout feature/entry-editing

# Work on the feature
# ... make changes ...

# Commit and push
git add .
git commit -m "implement entry editing core functionality

- Add edit route for historical entries
- Implement entry update validation
- Add edit button to history view

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin feature/entry-editing

# Create PR when ready
gh pr create --base develop --title "Add entry editing functionality"
```

### Recommended Development Order
Based on roadmap priorities:

1. **`feature/entry-editing`** (Highest Priority)
2. **`feature/history-enhancement`** (Supports editing)
3. **`feature/entry-titles`** (User experience)
4. **`feature/dynamic-ui`** (User experience)
5. **`feature/form-validation`** (Data integrity)
6. **`feature/mobile-responsive`** (Final polish)

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