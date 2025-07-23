# ADR-0016: Draft System & Auto-save Removal

**Date**: 2025-01-23  
**Status**: ✅ Accepted  
**Category**: Business Decision / Feature Scope  

## Context

The roadmap initially included a Draft System & Auto-save feature that would:
- Add `is_draft` field to entry model
- Implement auto-save every 30 seconds
- Create draft API endpoints: `/entries/draft`, `/entries/finalize`, `/entries/today/draft`
- Modify one-entry-per-day rule to apply only to finalized entries

After extensive development effort, the team determined this feature to be:
1. **Bug-prone**: Full of implementation complexity and edge cases
2. **Low impact**: Minimal user value relative to development cost
3. **Unnecessary complexity**: Current unsaved changes warning provides adequate data protection

## Analysis Conducted

### Code Impact Assessment
- **Database Models**: No draft fields implemented (is_draft, last_auto_saved missing)
- **API Endpoints**: No draft endpoints exist in current codebase
- **Frontend Code**: No auto-save functionality implemented
- **Business Logic**: Current one-entry-per-day logic works correctly without draft system

### Dependency Analysis
**Features that would NOT be impacted:**
- ✅ Entry creation and editing system
- ✅ One-entry-per-day constraint (current implementation correct)
- ✅ Unsaved changes warning system (independent data protection)
- ✅ All core journaling functionality

**Only impacted components:**
- 📋 Planning documentation references (safe to update)
- 📋 Architecture specifications (documentation only)

## Decision

**Remove Draft System & Auto-save feature entirely** from the Success Diary roadmap.

### Rationale

1. **Risk vs. Reward**: High implementation complexity for minimal user benefit
2. **Clean Architecture**: Simpler codebase without draft state management
3. **Adequate Protection**: Existing unsaved changes warning provides data loss prevention
4. **Zero Breaking Changes**: No implementation exists, so removal has no code impact
5. **Focus on Core Value**: Resources better spent on high-impact MVP features

### Alternative Solutions

**Current Data Protection Strategy:**
- ✅ Unsaved changes warning prevents accidental data loss
- ✅ Form validation provides real-time feedback
- ✅ Error handling ensures reliable saving
- ✅ Manual save with clear confirmation

## Implementation

### Immediate Actions
1. **Update Planning Documents**:
   - Remove draft system from `docs/planning/roadmap.md`
   - Update architecture specifications to remove draft references
   - Clean product requirements documentation

2. **Maintain Current Systems**:
   - Keep unsaved changes warning system (`unsaved-changes-warning.js`)
   - Preserve current one-entry-per-day constraint logic
   - Continue with existing entry editing workflow

### No Code Changes Required
- **Database**: No migration needed (no draft fields exist)
- **API**: No endpoint removal needed (none implemented)
- **Frontend**: No UI cleanup needed (no draft interface exists)

## Consequences

### Positive
- ✅ **Simplified Architecture**: Cleaner codebase without draft state complexity
- ✅ **Reduced Bug Risk**: Eliminates auto-save race conditions and draft synchronization issues
- ✅ **Faster Development**: Focus on high-impact MVP features
- ✅ **Better UX**: Single, clear save action vs. confusing draft/final states

### Neutral
- 📋 **Documentation Updates**: Minor effort to clean planning documents
- 📋 **User Expectations**: No user-facing impact (feature never announced)

### Negative
- ❌ **No Auto-save Convenience**: Users must manually save (mitigated by unsaved changes warning)

## Future Considerations

**If Auto-save Becomes Critical in Future:**
- Could implement simplified auto-save without draft system
- Browser localStorage could provide temporary data protection
- Progressive Web App offline capabilities could address data loss concerns

**Current Workaround Remains Adequate:**
- Unsaved changes warning prevents data loss
- Manual save provides clear user control
- Form validation ensures data quality before saving

## Stakeholder Impact

**Users**: No impact (feature never implemented or announced)  
**Developers**: Simplified development focus on core MVP features  
**Product**: Cleaner roadmap aligned with "must-have" vs "nice-to-have" prioritization  

---

**Decision Made By**: Development Team  
**Implementation Date**: 2025-01-23  
**Next Review**: Not scheduled (permanent removal)