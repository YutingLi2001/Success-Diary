# ADR-0004: Entry Title Auto-Generation with User Locale

## Status

Accepted

## Context

The Success-Diary application needs an automatic entry title generation system that feels natural and personalized to users. Key considerations include:

- **User Experience**: Reduce cognitive load while maintaining personalization
- **Internationalization**: Support users across different countries and languages
- **Consistency**: Predictable title format that aids in entry organization
- **Localization**: Respect user's cultural date format preferences
- **Fallback Strategy**: Robust handling when locale detection fails

## Decision

Implement user locale-based entry title generation using browser timezone and language detection:

- **Detection Method**: `Intl.DateTimeFormat()` with `navigator.language`
- **Format**: Full date format (e.g., "January 15, 2025", "15 January 2025", "15. Januar 2025")
- **Fallback**: US English format if locale detection fails
- **Auto-generation**: Default behavior with manual override capability

## Considered Options

1. **Fixed US format**: "January 15, 2025" for all users
2. **User setting**: Manual locale selection in preferences
3. **Browser locale detection (Selected)**: Automatic with manual override
4. **Timezone-based format**: Use timezone for date format inference
5. **Short format**: "Jan 15" or "1/15/25" for brevity

## Consequences

**Positive:**
- Respects user cultural preferences automatically
- International-friendly out of the box
- Feels personalized without requiring setup
- Maintains simplicity with robust fallback
- Reduces user cognitive load during entry creation

**Negative:**
- Slight complexity in frontend implementation
- Edge cases with VPN/proxy usage affecting detection
- Different formats may confuse users switching devices

**Neutral:**
- Standard web internationalization practice
- Consistent with modern web application expectations

## Implementation Notes

**Frontend Implementation:**
```javascript
const formatEntryTitle = (date, locale = navigator.language) => {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long', 
    day: 'numeric'
  }).format(date);
};

// Usage examples:
// US English: "January 15, 2025"
// UK English: "15 January 2025"  
// German: "15. Januar 2025"
// French: "15 janvier 2025"
```

**Fallback Strategy:**
```javascript
const safeFormatEntryTitle = (date) => {
  try {
    return formatEntryTitle(date);
  } catch (error) {
    // Fallback to US format
    return formatEntryTitle(date, 'en-US');
  }
};
```

**Database Storage:**
- Store generated title as default
- Allow manual title editing/override
- Maintain consistency across entry history

**User Experience:**
- Auto-generated titles appear immediately
- Users can edit titles inline if desired
- Clear indication of auto-generated vs. manual titles

## References

- MDN Intl.DateTimeFormat documentation
- Web internationalization best practices
- Browser locale detection standards
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 1)