# Character Limits Specification

## Overview

This specification defines the character limit strategy for journaling entries in the Success-Diary application, balancing user freedom with system constraints.

## Requirements

### Character Limit Configuration

**Backend Hard Limit**: 8,000 characters
- **Rationale**: ~1,200 words ≈ 2 pages typed
- **Coverage**: Accommodates single daily entry with multiple sections
- **Emotional Space**: Handles significant life events requiring detailed processing
- **Psychological Comfort**: Users never feel restricted during important moments

**Frontend Progressive Indicators**:
- **90% threshold**: 7,200 characters - Show character counter
- **95% threshold**: 7,600 characters - Show warning indicator
- **100% threshold**: 8,000 characters - Prevent additional typing

## Technical Implementation

### Backend Validation

```python
# Database schema
class Entry(SQLModel, table=True):
    # Text fields with character limits
    victory: Optional[str] = Field(max_length=8000)
    gratitude: Optional[str] = Field(max_length=8000)
    anxiety: Optional[str] = Field(max_length=8000)
    journal_text: Optional[str] = Field(max_length=8000)

# API validation
from pydantic import validator

class EntryCreate(BaseModel):
    victory: Optional[str] = None
    gratitude: Optional[str] = None
    anxiety: Optional[str] = None
    journal_text: Optional[str] = None
    
    @validator('victory', 'gratitude', 'anxiety', 'journal_text')
    def validate_text_length(cls, v):
        if v and len(v) > 8000:
            raise ValueError('Text exceeds maximum length of 8,000 characters')
        return v

# Error response for limit exceeded
@app.exception_handler(ValueError)
async def character_limit_handler(request: Request, exc: ValueError):
    if "maximum length" in str(exc):
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "CHARACTER_LIMIT_EXCEEDED",
                    "message": "Entry text exceeds the 8,000 character limit",
                    "limit": 8000,
                    "recoverable": True
                }
            }
        )
```

### Frontend Implementation

```javascript
// Character counting component
const CharacterCounter = ({ text, maxLength = 8000 }) => {
  const length = text?.length || 0;
  const percentage = (length / maxLength) * 100;
  
  // Show counter at 90% threshold
  if (percentage < 90) return null;
  
  const getCounterStyle = () => {
    if (percentage >= 100) return 'counter-error';
    if (percentage >= 95) return 'counter-warning';
    return 'counter-info';
  };
  
  return (
    <div className={`character-counter ${getCounterStyle()}`}>
      <span className="count">{length.toLocaleString()}</span>
      <span className="separator">/</span>
      <span className="limit">{maxLength.toLocaleString()}</span>
      {percentage >= 95 && (
        <span className="remaining">
          ({(maxLength - length).toLocaleString()} remaining)
        </span>
      )}
    </div>
  );
};

// Text area with character limiting
const LimitedTextArea = ({ value, onChange, maxLength = 8000, ...props }) => {
  const handleChange = (e) => {
    const newValue = e.target.value;
    
    // Prevent typing beyond limit
    if (newValue.length > maxLength) {
      return;
    }
    
    onChange(e);
  };
  
  return (
    <div className="limited-textarea-container">
      <textarea
        value={value}
        onChange={handleChange}
        maxLength={maxLength}
        {...props}
      />
      <CharacterCounter text={value} maxLength={maxLength} />
    </div>
  );
};

// Usage in journal form
const JournalForm = () => {
  const [formData, setFormData] = useState({
    victory: '',
    gratitude: '',
    anxiety: '',
    journal_text: ''
  });
  
  return (
    <form>
      <LimitedTextArea
        value={formData.victory}
        onChange={(e) => setFormData({...formData, victory: e.target.value})}
        placeholder="What victory or success did you experience today?"
        rows={3}
      />
      
      <LimitedTextArea
        value={formData.gratitude}
        onChange={(e) => setFormData({...formData, gratitude: e.target.value})}
        placeholder="What are you grateful for today?"
        rows={3}
      />
      
      <LimitedTextArea
        value={formData.anxiety}
        onChange={(e) => setFormData({...formData, anxiety: e.target.value})}
        placeholder="What anxiety or concern would you like to process?"
        rows={3}
      />
      
      <LimitedTextArea
        value={formData.journal_text}
        onChange={(e) => setFormData({...formData, journal_text: e.target.value})}
        placeholder="Free-form journaling space..."
        rows={8}
      />
    </form>
  );
};
```

### CSS Styling

```css
/* Character counter styles */
.character-counter {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  margin-top: 0.5rem;
  justify-content: flex-end;
}

.counter-info {
  color: #6b7280; /* Gray */
}

.counter-warning {
  color: #f59e0b; /* Amber */
}

.counter-error {
  color: #ef4444; /* Red */
  font-weight: 600;
}

.limited-textarea-container {
  position: relative;
}

.limited-textarea-container textarea {
  width: 100%;
  resize: vertical;
  min-height: 120px;
}

/* Visual feedback for approaching limit */
.limited-textarea-container textarea:focus {
  outline: 2px solid #3b82f6;
}

.counter-warning + textarea:focus {
  outline-color: #f59e0b;
}

.counter-error + textarea:focus {
  outline-color: #ef4444;
}
```

## User Experience Guidelines

### Progressive Disclosure
- **0-90% of limit**: No visual indicators (clean interface)
- **90-95% of limit**: Subtle character counter appears
- **95-100% of limit**: Warning color and "remaining" text
- **100% of limit**: Prevent additional typing, error styling

### Error Handling
- **Client-side**: Immediate feedback with character counter
- **Server-side**: Graceful error response with recovery guidance
- **User guidance**: Clear messaging about character limits and editing options

### Accessibility
- **Screen readers**: Announce character count changes
- **Keyboard navigation**: Counter updates don't interrupt typing flow
- **Visual indicators**: Color changes accompanied by text changes

## Testing Requirements

### Unit Tests
```javascript
describe('Character Limits', () => {
  test('prevents typing beyond 8000 characters', () => {
    const longText = 'a'.repeat(8001);
    // Test that component rejects input
  });
  
  test('shows counter at 90% threshold', () => {
    const text = 'a'.repeat(7200);
    // Test that counter becomes visible
  });
  
  test('shows warning at 95% threshold', () => {
    const text = 'a'.repeat(7600);
    // Test that warning styling appears
  });
});
```

### Integration Tests
- Form submission with various text lengths
- Server validation of character limits
- Error handling for exceeded limits
- Character counter accuracy across different text inputs

## Configuration

### Environment Variables
```bash
# Backend configuration
MAX_ENTRY_LENGTH=8000
CHARACTER_LIMIT_WARNING_THRESHOLD=0.95
CHARACTER_LIMIT_INFO_THRESHOLD=0.90

# Frontend configuration
REACT_APP_MAX_ENTRY_LENGTH=8000
```

### Database Considerations
- **Text vs VARCHAR**: Use TEXT type for PostgreSQL production
- **Indexing**: No full-text indexing needed for character limits
- **Migration**: Existing entries longer than 8000 chars grandfathered

## References

- User experience research on text input constraints
- Accessibility guidelines for form validation
- Performance considerations for real-time character counting