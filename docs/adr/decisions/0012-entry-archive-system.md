# ADR-0012: Entry Archive System - Three-State Management

## Status

Accepted

## Context

The Success-Diary application needs a nuanced entry management system that respects users' complex emotional relationship with their personal reflections. Key considerations include:

- **Emotional Complexity**: Users may want to hide painful memories without losing them permanently
- **UI Clarity**: Main views should focus on current/relevant entries without clutter
- **Data Preservation**: Important life events should never be lost, just organized by visibility
- **User Control**: Flexible organization allowing users to control what they see day-to-day
- **Existing System**: Current soft delete + recycle bin only supports eventual deletion

## Decision

Implement three-state entry management system:

- **Active**: Default state, visible in all standard views
- **Archived**: Hidden from default views, accessible via dedicated archive section
- **Deleted**: Soft deleted with 30-day recycle bin (existing system)

## Considered Options

1. **Two-state (Active/Deleted)**: Simple but insufficient for emotional complexity
2. **Tags/Categories**: Flexible but potentially overwhelming for users
3. **Three-state system (Selected)**: Balanced approach with clear use cases
4. **Folder system**: Organizational but complex for journaling context
5. **Visibility levels**: Granular control but decision fatigue

## Consequences

**Positive:**
- Emotional support for hiding painful memories without permanent loss
- UI clarity with main views focused on current/relevant entries
- Data preservation ensures important life events are never lost
- Flexible organization gives users control over visibility
- Batch operations for efficient management of multiple entries

**Negative:**
- Additional database complexity with three states
- More complex UI with archive management interface
- Potential user confusion about different states

**Neutral:**
- Standard pattern for content management systems
- Minimal performance impact with proper indexing

## Implementation Notes

**Database Schema Addition:**
```sql
-- Add to Entry model
ALTER TABLE entries ADD COLUMN is_archived BOOLEAN DEFAULT FALSE;
ALTER TABLE entries ADD COLUMN archived_at TIMESTAMP NULL;
ALTER TABLE entries ADD COLUMN archived_reason VARCHAR(100) NULL;

-- Archived reason categories (optional)
-- 'emotional_content', 'outdated', 'personal', 'seasonal', 'custom'
```

**User Interface Design:**
```
Entry Actions Menu:
├── Edit Entry
├── Archive Entry          ← New action
├── Delete Entry
└── ...

Navigation:
├── Dashboard
├── History
├── Archive                ← New section
├── Analytics
└── Settings

Archive Section:
├── View Archived Entries
├── Search Archived
├── Batch Unarchive
└── Export Archived
```

**Backend Query Logic:**
```python
# Default views exclude archived entries
@app.get("/entries")
async def get_entries(
    include_archived: bool = False,
    user: User = Depends(current_user)
):
    query = select(Entry).where(
        Entry.user_id == user.id,
        Entry.is_deleted == False
    )
    
    if not include_archived:
        query = query.where(Entry.is_archived == False)
    
    return await session.execute(query.order_by(Entry.created_at.desc()))

# Dedicated archive view
@app.get("/entries/archived")
async def get_archived_entries(user: User = Depends(current_user)):
    query = select(Entry).where(
        Entry.user_id == user.id,
        Entry.is_archived == True,
        Entry.is_deleted == False
    ).order_by(Entry.archived_at.desc())
    
    return await session.execute(query)

# Archive/Unarchive operations
@app.post("/entries/{entry_id}/archive")
async def archive_entry(
    entry_id: int,
    archive_data: ArchiveRequest,
    user: User = Depends(current_user)
):
    entry = await get_user_entry(entry_id, user.id)
    
    entry.is_archived = True
    entry.archived_at = datetime.utcnow()
    entry.archived_reason = archive_data.reason
    
    await session.commit()
    return {"status": "archived"}

@app.post("/entries/{entry_id}/unarchive")
async def unarchive_entry(
    entry_id: int,
    user: User = Depends(current_user)
):
    entry = await get_user_entry(entry_id, user.id)
    
    entry.is_archived = False
    entry.archived_at = None
    entry.archived_reason = None
    
    await session.commit()
    return {"status": "unarchived"}
```

**Frontend Implementation:**
```javascript
// Archive/Unarchive actions
const archiveEntry = async (entryId, reason = null) => {
  const response = await fetch(`/entries/${entryId}/archive`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ reason })
  });
  
  if (response.ok) {
    // Remove from current view
    removeEntryFromView(entryId);
    showToast('Entry archived successfully', 'success');
  }
};

const unarchiveEntry = async (entryId) => {
  const response = await fetch(`/entries/${entryId}/unarchive`, {
    method: 'POST'
  });
  
  if (response.ok) {
    // Move back to active entries
    refreshEntryList();
    showToast('Entry restored from archive', 'success');
  }
};

// Batch archive operations
const batchArchiveEntries = async (entryIds, reason) => {
  const promises = entryIds.map(id => archiveEntry(id, reason));
  await Promise.all(promises);
  
  showToast(`${entryIds.length} entries archived`, 'success');
};
```

**Archive Use Cases:**
- Difficult life periods (grief, breakups, trauma processing)
- Outdated goals or perspectives that have evolved
- Highly personal content for special occasions only
- Seasonal or periodic reflections (yearly reviews)
- Content that might be triggering but shouldn't be deleted

**User Experience Benefits:**
- **Emotional Intelligence**: Respects complex relationship with personal reflections
- **Organizational Clarity**: Clean main views with hidden storage option
- **Batch Management**: Efficiently organize multiple entries (e.g., archive difficult period)
- **Reversible Actions**: Unlike deletion, archiving is completely reversible
- **Contextual Reasons**: Optional categorization helps users organize archives

**Implementation Phases:**
1. **MVP 1.0**: Basic archive/unarchive functionality with simple UI
2. **V2.0**: Archive reasons/categories for better organization
3. **V3.0**: Advanced archive filters, smart suggestions, and analytics

## References

- Content management archive patterns
- User psychology in personal data management
- Database indexing for multi-state queries
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 15)