# ADR-0006: History View Sorting Strategy

## Status

Accepted

## Context

The Success-Diary application needs a flexible entry history sorting system that accommodates different user viewing patterns. Key considerations include:

- **User Preferences**: Some users want recent entries first, others prefer chronological journey view
- **Default Behavior**: Need sensible default that matches modern app expectations
- **Persistence**: User preferences should be remembered across sessions
- **UI Clarity**: Sorting controls should be intuitive and discoverable
- **Performance**: Sorting should not impact page load performance

## Decision

Implement user preference-based sorting with smart default:

- **Default Sorting**: Newest first (descending chronological order)
- **User Control**: Toggle button with "Newest First" / "Oldest First" options
- **Persistence**: Save preference per user in database
- **UI Location**: Prominent sort toggle in history view header

## Considered Options

1. **Fixed newest first**: Simple but inflexible for journey-style viewing
2. **Fixed oldest first**: Logical but conflicts with modern app patterns
3. **User preference with smart default (Selected)**: Flexible with good defaults
4. **Multiple sort options**: More complex (date, mood, title) but potentially confusing
5. **Auto-detection based on usage**: Intelligent but complex implementation

## Consequences

**Positive:**
- Accommodates both "recent progress" and "journey story" viewing patterns
- Modern default meets user expectations from other apps
- Persistent preference improves UX over time
- Simple toggle provides immediate user control
- Clear visual feedback on current sort order

**Negative:**
- Additional database field and logic complexity
- Need to handle preference migration for existing users
- UI space required for sort controls

**Neutral:**
- Standard pattern in modern applications
- Minimal performance impact with proper indexing

## Implementation Notes

**Database Schema Addition:**
```sql
-- Add to User model
entry_sort_preference VARCHAR(20) DEFAULT 'newest_first'  -- 'newest_first' | 'oldest_first'
```

**Frontend Implementation:**
```javascript
// History view component
const sortEntries = (entries, preference) => {
  return preference === 'oldest_first' 
    ? entries.sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
    : entries.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
};

// Sort preference toggle
const toggleSortPreference = async (currentPreference) => {
  const newPreference = currentPreference === 'newest_first' ? 'oldest_first' : 'newest_first';
  
  await fetch('/api/user/preferences', {
    method: 'PATCH',
    body: JSON.stringify({ entry_sort_preference: newPreference })
  });
  
  // Update UI immediately
  updateHistoryView(newPreference);
};
```

**Backend API:**
```python
# Get user's entries with preferred sorting
@app.get("/entries/history")
async def get_entry_history(user: User = Depends(current_user)):
    query = select(Entry).where(Entry.user_id == user.id, Entry.is_deleted == False)
    
    if user.entry_sort_preference == 'oldest_first':
        query = query.order_by(Entry.created_at.asc())
    else:
        query = query.order_by(Entry.created_at.desc())
    
    return await session.execute(query)

# Update sort preference
@app.patch("/api/user/preferences")
async def update_sort_preference(
    preferences: UserPreferences,
    user: User = Depends(current_user)
):
    user.entry_sort_preference = preferences.entry_sort_preference
    await session.commit()
    return {"status": "updated"}
```

**UI Design:**
- Toggle button in history view header
- Clear visual indication of current sort order
- Smooth transition when preference changes
- Consistent with other app sorting patterns

## References

- Modern mobile app sorting patterns
- User preference persistence best practices
- Database indexing for chronological queries
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 4)