# ADR-0010: User Feedback Collection Strategy

## Status

Accepted

## Context

The Success-Diary application needs a systematic approach to collect user feedback from early adopters to guide product development. Key considerations include:

- **User Experience**: Feedback collection should be non-intrusive and optional
- **Response Quality**: Structured feedback provides more actionable insights than open-ended comments
- **User Journey**: Feedback timing should align with user engagement patterns
- **Development Priority**: Simple implementation that provides valuable product insights
- **Privacy**: Users should feel comfortable sharing honest feedback

## Decision

Implement in-app feedback widget with structured form design:

- **Location**: Subtle feedback button in settings/profile area
- **Design**: Non-intrusive, accessible when users want to provide input
- **Form Structure**: Short, focused questions with optional sections
- **Storage**: Backend database with analytics dashboard for team review

## Considered Options

1. **Email surveys**: External but low response rates
2. **Pop-up feedback requests**: High visibility but potentially intrusive
3. **In-app feedback widget (Selected)**: Contextual and user-controlled
4. **Third-party feedback tools**: Feature-rich but data privacy concerns
5. **User interview scheduling**: Deep insights but resource-intensive

## Consequences

**Positive:**
- Low friction, contextual feedback collection
- Higher response rates from motivated users
- Immediate submission without leaving application
- Structured data enables analysis and feature prioritization
- User-controlled timing reduces annoyance

**Negative:**
- May miss feedback from users who don't discover the feature
- Requires backend development and data management
- Feedback volume may be lower than proactive approaches

**Neutral:**
- Standard pattern for mature web applications
- Integrates naturally with existing user settings flow

## Implementation Notes

**Feedback Form Design:**
```html
<!-- Feedback modal component -->
<div className="feedback-modal" id="feedback-modal">
  <form id="feedback-form" onSubmit={handleFeedbackSubmit}>
    <h3>Help us improve your journaling experience</h3>
    
    <div className="form-group">
      <label>What's working well for you?</label>
      <textarea 
        name="working_well"
        maxLength="500" 
        placeholder="What features do you love? What makes journaling easier?"
        rows="3"
      ></textarea>
    </div>
    
    <div className="form-group">
      <label>What needs improvement?</label>
      <textarea 
        name="needs_improvement"
        maxLength="500" 
        placeholder="What's frustrating or confusing? What slows you down?"
        rows="3"
      ></textarea>
    </div>
    
    <div className="form-group">
      <label>Feature request (optional)</label>
      <textarea 
        name="feature_request"
        maxLength="300" 
        placeholder="What would make this even better for you?"
        rows="2"
      ></textarea>
    </div>
    
    <div className="form-actions">
      <button type="button" onClick={closeFeedbackModal}>Cancel</button>
      <button type="submit" className="primary">Send Feedback</button>
    </div>
  </form>
</div>
```

**Backend Storage:**
```python
# Database model
class UserFeedback(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    working_well: Optional[str] = Field(max_length=500)
    needs_improvement: Optional[str] = Field(max_length=500)
    feature_request: Optional[str] = Field(max_length=300)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Optional metadata
    app_version: Optional[str] = Field(max_length=20)
    user_agent: Optional[str] = Field(max_length=500)
    session_duration: Optional[int] = None  # minutes since login

# API endpoint
@app.post("/feedback")
async def submit_feedback(
    feedback: UserFeedbackCreate,
    user: User = Depends(current_user)
):
    db_feedback = UserFeedback(
        user_id=user.id,
        working_well=feedback.working_well,
        needs_improvement=feedback.needs_improvement,
        feature_request=feedback.feature_request,
        app_version=feedback.app_version,
        user_agent=feedback.user_agent
    )
    
    session.add(db_feedback)
    await session.commit()
    
    return {"status": "success", "message": "Thank you for your feedback!"}
```

**Frontend Integration:**
```javascript
// Feedback widget trigger
const FeedbackButton = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  return (
    <div className="feedback-widget">
      <button 
        onClick={() => setIsOpen(true)}
        className="feedback-trigger"
        aria-label="Send feedback"
      >
        💬 Feedback
      </button>
      
      {isOpen && (
        <FeedbackModal 
          onClose={() => setIsOpen(false)}
          onSubmit={handleFeedbackSubmit}
        />
      )}
    </div>
  );
};

// Feedback submission
const handleFeedbackSubmit = async (formData) => {
  const response = await fetch('/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      ...formData,
      app_version: process.env.REACT_APP_VERSION,
      user_agent: navigator.userAgent
    })
  });
  
  if (response.ok) {
    showSuccessMessage('Thank you for your feedback!');
    closeFeedbackModal();
  }
};
```

**Analytics Dashboard:**
```python
# Internal analytics endpoint for team review
@app.get("/admin/feedback/analytics")
async def get_feedback_analytics(admin_user: User = Depends(require_admin)):
    # Aggregate feedback data
    feedback_summary = await session.execute(
        select(
            func.count(UserFeedback.id).label('total_feedback'),
            func.count(UserFeedback.working_well).label('positive_feedback'),
            func.count(UserFeedback.needs_improvement).label('improvement_feedback'),
            func.count(UserFeedback.feature_request).label('feature_requests')
        )
    )
    
    return {
        "summary": feedback_summary.first(),
        "recent_feedback": await get_recent_feedback(limit=50),
        "common_themes": await analyze_feedback_themes()
    }
```

## References

- User feedback collection best practices
- In-app feedback widget design patterns
- Feedback analysis and prioritization methods
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 12)