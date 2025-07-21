# ADR-0014: Minimal Card Design with Single Preview

## Status

Accepted

## Context

The Success-Diary entry cards were initially displaying extensive content preview, creating significant UX challenges:

- **Information Overload**: Cards showing 3×3×255 characters = up to 2,295 characters per card
- **Mobile Usability Crisis**: Massive text blocks create unusable mobile experience
- **Visual Hierarchy Problems**: Users cannot quickly scan or differentiate entries
- **Cognitive Load**: Too much information prevents quick entry recognition
- **Performance Impact**: Large DOM elements with extensive text affect rendering performance
- **Design Inconsistency**: Variable card heights create chaotic visual layout

## Decision

Implement minimal card design with focused single preview approach:

- **Card Content**: Title + Date/Score + Single preview line (60 characters from success_1)
- **Preview Source**: Use first success field (success_1) as representative content
- **Character Limit**: 60 characters with smart word boundary truncation
- **Consistent Layout**: Fixed visual hierarchy with predictable card heights
- **Design Pattern**: Follow proven card designs from Apple Notes, Google Keep, Day One

## Considered Options

1. **Full content preview (Current)**: Display all three fields with 255+ chars each
2. **Rotating preview**: Cycle through different fields for preview content
3. **User-selected preview**: Allow users to choose which field appears in preview
4. **Two-line preview**: Show two fields with truncation
5. **Single line preview (Selected)**: 60 characters from primary success field
6. **No preview**: Title and metadata only

## Consequences

**Positive:**
- **Mobile Optimization**: Cards become highly scannable on mobile devices
- **Faster Recognition**: Users can quickly identify entries by title and brief content
- **Consistent Visual Hierarchy**: Predictable card heights create clean grid layouts
- **Reduced Cognitive Load**: Essential information only, following minimalist design principles
- **Better Performance**: Smaller DOM elements improve rendering and scrolling performance
- **Industry Alignment**: Matches user expectations from popular note-taking applications

**Negative:**
- **Reduced Context**: Users see less content without clicking through to full view
- **Preview Limitation**: Single field preview may not represent full entry content
- **Potential Truncation Issues**: Important content might be cut off at 60 characters

**Neutral:**
- **Follows Mobile-First**: Aligns with modern responsive design principles
- **Progressive Disclosure**: Users get overview first, details on demand

## Implementation Notes

**Template Logic:**
```html
<!-- Entry Card Preview Implementation -->
<div class="text-sm text-gray-600 mt-2">
    {{ entry.success_1[:60] }}{% if entry.success_1|length > 60 %}...{% endif %}
</div>
```

**Smart Truncation Strategy:**
- Use first 60 characters of success_1 field
- Add ellipsis (...) when content exceeds limit
- Maintain word boundaries where possible
- Graceful fallback for empty success_1 fields

**Card Layout Structure:**
```
┌─────────────────────────────────┐
│ [Title] - Auto-generated or Custom │
│ [Date] • [Score/10] • [Edit Icon]  │
│ [60-char preview from success_1]   │
└─────────────────────────────────┘
```

**Visual Design:**
- `bg-gradient-to-r from-blue-50 to-indigo-50` background
- `border-l-4 border-blue-400` left accent border
- Consistent padding and spacing
- Hover states with shadow and translation effects

**Responsive Considerations:**
- Cards adapt gracefully across breakpoints (375px to 1440px)
- Touch-friendly spacing on mobile devices
- Readable typography at all screen sizes

## References

- Apple Notes card design patterns
- Google Keep minimalist card approach
- Day One entry preview strategies
- Mobile-first design principles
- Implementation: `templates/dashboard.html:181-215`, `templates/entries.html:133-154`