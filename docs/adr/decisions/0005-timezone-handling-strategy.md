# ADR-0005: User Timezone Handling Strategy

## Status

Accepted

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

## References

- JavaScript Intl.DateTimeFormat documentation
- Python pytz timezone handling
- Web timezone best practices
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 8)