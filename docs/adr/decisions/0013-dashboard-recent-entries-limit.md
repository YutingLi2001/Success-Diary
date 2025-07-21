# ADR-0013: Dashboard Recent Entries Limit

## Status

Accepted

## Context

The Success-Diary dashboard was initially displaying all user entries in chronological order, which creates several UX and performance challenges:

- **Performance Impact**: Loading all entries on dashboard creates unnecessary database queries and page load time
- **Cognitive Overload**: Users face decision paralysis when confronted with extensive entry history immediately upon login
- **Mobile Experience**: Long scrolling lists on mobile devices create poor user experience
- **Dashboard Purpose**: Dashboard should provide quick overview and entry creation, not comprehensive history browsing
- **Navigation Clarity**: Users need clear distinction between "quick view" (dashboard) and "full history" (entries page)

## Decision

Limit dashboard recent entries display to **3 most recent entries only**:

- **Dashboard Query**: Modify database query to `.limit(3)` for recent entries section
- **Navigation Enhancement**: Add prominent "View all entries →" link to entries page
- **Clear Separation**: Dashboard becomes focused entry point, entries page handles full history
- **Performance Optimization**: Reduces initial page load time and database queries

## Considered Options

1. **Display all entries (Current)**: Show complete entry history on dashboard
2. **Configurable limit**: Allow users to set their own display preference (5-20 entries)
3. **Fixed limit of 5**: Show 5 most recent entries
4. **Fixed limit of 3 (Selected)**: Show 3 most recent entries with clear navigation
5. **Pagination**: Add pagination controls to dashboard

## Consequences

**Positive:**
- **Faster Load Times**: Significantly reduced database queries and page rendering time
- **Cleaner UI**: Dashboard becomes focused and less overwhelming for new users
- **Better Mobile Experience**: Minimal scrolling required on mobile devices
- **Clear Navigation**: Users understand dashboard vs. entries page purposes
- **Encourages Full History Usage**: Drives traffic to dedicated entries page with better tooling

**Negative:**
- **Reduced Immediate Visibility**: Users cannot quickly scan extensive history from dashboard
- **Extra Click Required**: Accessing older entries requires navigation to entries page
- **Potential User Confusion**: Users may initially expect full history on dashboard

**Neutral:**
- **Industry Standard**: Follows common dashboard design patterns (Twitter, Instagram, etc.)
- **Progressive Disclosure**: Aligns with UX best practices for information architecture

## Implementation Notes

**Backend Changes:**
```python
# app/main.py dashboard endpoint
entries = db.query(Entry)\
    .filter(Entry.user_id == str(user.id))\
    .order_by(Entry.entry_date.desc())\
    .limit(3)\
    .all()
```

**Frontend Enhancement:**
```html
<!-- templates/dashboard.html -->
<div class="flex justify-between items-center mb-4">
    <h2 class="text-xl font-semibold text-gray-900">Recent Entries</h2>
    <a href="/entries" class="text-blue-600 hover:text-blue-800 text-sm font-medium">
        View all entries →
    </a>
</div>
```

**User Experience:**
- Dashboard loads instantly with minimal data
- Clear visual hierarchy directs users to appropriate sections
- "View all →" link provides obvious path to full history
- Mobile users benefit from reduced scrolling and faster loading

## References

- Dashboard UX patterns in social applications
- Progressive disclosure principles in interface design
- Mobile-first design considerations
- Implementation: `app/main.py:159` and `templates/dashboard.html`