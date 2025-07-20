# ADR-0005: User Timezone Handling Strategy

## Status

Accepted - **Updated 2025-07-19** with One Entry Per Day refinement

## Context

The Success-Diary application needs robust timezone handling to ensure daily entries are properly organized and displayed according to user's local time. Key considerations include:

- **Daily Entry Logic**: Entries should be organized by user's local date, not server time
- **Global User Base**: Users may be in different timezones than the server
- **Travel Scenarios**: Users may travel frequently and need appropriate timezone handling
- **User Experience**: Timezone handling should be transparent and automatic
- **Technical Complexity**: Balance between accuracy and implementation simplicity

## Decision

Implement hybrid auto-detection with manual override capability:

- **Primary Method**: Browser-based timezone detection using `Intl.DateTimeFormat().resolvedOptions().timeZone`
- **Manual Override**: User settings allow timezone preference that takes priority
- **Session-based**: Auto-detection occurs on each session start
- **Fallback Chain**: Manual setting → Auto-detection → UTC fallback

## Considered Options

1. **Server timezone only**: Simple but poor UX for global users
2. **Manual timezone selection**: Accurate but requires user setup
3. **Browser detection only**: Automatic but no user control
4. **Hybrid approach (Selected)**: Auto-detection with manual override
5. **IP-based detection**: Automatic but privacy concerns and VPN issues

## Consequences

**Positive:**
- Zero friction for new users (automatic detection)
- User control for power users and edge cases
- Travel-friendly with automatic adaptation
- Reliable fallback for complex scenarios
- Transparent operation requiring no user configuration

**Negative:**
- Additional complexity in frontend and backend
- Edge cases with VPN/proxy usage
- Potential confusion if detection differs from user expectation

**Neutral:**
- Standard practice for modern web applications
- Well-supported browser APIs

## Implementation Notes

**Database Schema:**
```sql
-- User timezone preferences
user_timezone VARCHAR(50) NULL                    -- Manual preference (e.g., 'America/New_York')
timezone_auto_detect BOOLEAN DEFAULT TRUE         -- User allows auto-detection
last_detected_timezone VARCHAR(50) NULL           -- Cache of last detected timezone
```

**Frontend Implementation:**
```javascript
// Session timezone detection
const detectedTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
const effectiveTimezone = userPreference || detectedTimezone || 'UTC';

// Send to backend for date calculations
await fetch('/api/session/timezone', {
    method: 'POST',
    body: JSON.stringify({ 
        timezone: effectiveTimezone, 
        detected: detectedTimezone 
    })
});
```

**Backend Processing:**
```python
# Daily entry date calculation
def get_user_date(user_timezone: str) -> date:
    user_tz = pytz.timezone(user_timezone)
    return datetime.now(user_tz).date()

# Entry retrieval with timezone context
def get_entries_for_date(user_id: int, target_date: date, timezone: str):
    # Convert user date to UTC range for database query
    user_tz = pytz.timezone(timezone)
    start_utc = user_tz.localize(datetime.combine(target_date, time.min)).astimezone(pytz.UTC)
    end_utc = user_tz.localize(datetime.combine(target_date, time.max)).astimezone(pytz.UTC)
    
    return query.filter(Entry.created_at.between(start_utc, end_utc))
```

**User Experience Flow:**
1. **New Users**: Auto-detection enabled, timezone applied immediately
2. **Settings Control**: Manual timezone preference in user settings
3. **Travel Scenarios**: Auto-detection continues unless manual preference set
4. **Edge Cases**: Users can override detection for VPN/proxy scenarios

## Update: One Entry Per Day Strategy (2025-07-19)

### Additional Context

The application enforces a "one entry per day" constraint to support habit building and structured emotional reflection. This constraint requires careful timezone handling to prevent gaming while supporting legitimate travel scenarios.

### Refined Decision for One Entry Per Day

**Simplified Auto-Detection Approach:**
- Use browser auto-detection as the primary timezone source
- Remove manual override complexity for MVP simplicity  
- Implement straightforward daily constraint logic

**Travel Logic:**
- **Forward Travel**: Allow entry creation when traveling to later timezone (new date)
- **Backward Travel**: Block entry creation when traveling to earlier timezone (existing date occupied)
- **Rationale**: Prevents gaming while allowing natural "new day" progression

### Updated Implementation

**Simplified Business Logic:**
```python
def can_create_entry_today(user: User) -> bool:
    """Simple one-entry-per-day validation with auto-detected timezone"""
    today_local = get_user_local_date(user)  # Auto-detected timezone
    existing_entry = get_entry_for_date(user, today_local)
    return existing_entry is None

def get_user_local_date(user: User) -> date:
    """Get current date in user's auto-detected timezone"""
    user_timezone = get_user_effective_timezone(user)  # Auto-detection priority
    user_tz = pytz.timezone(user_timezone)
    return datetime.now(user_tz).date()
```

**User Experience:**
- **New Date Available**: "Create today's entry" 
- **Date Occupied**: "You already journaled today. [View/Edit Entry]"
- **No Complex Gaming Prevention**: Keep simple, handle abuse if it becomes actual problem

### Decision Rationale

1. **Simplicity**: Avoid over-engineering complex anti-gaming systems for MVP
2. **User Mental Model**: "New day = new entry" matches natural expectation
3. **MVP Focus**: Solve 90% of use cases with minimal complexity
4. **Gaming Tolerance**: Personal journal apps don't need fortress-level security
5. **Roadmap Alignment**: Matches planned draft system integration

### Updated Consequences

**Additional Positive:**
- Dramatically simplified implementation (3 lines of core logic)
- Clear user experience without confusing edge case handling
- Faster development velocity for MVP features

**Additional Negative:**
- Westward travel temporarily blocks journal creation
- Potential for timezone gaming (accepted risk for MVP)

**Mitigation:**
- Monitor user feedback for actual pain points vs. theoretical concerns
- Draft system (planned V1.1) will provide workaround for edge cases

## References

- JavaScript Intl.DateTimeFormat documentation
- Python pytz timezone handling
- Web timezone best practices
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 8)
- Implementation decision discussion: `docs/planning/todo.md` (2025-07-19)