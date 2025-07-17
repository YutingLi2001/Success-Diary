# Product Requirements

## Product Vision
SuccessDiary is a privacy-focused web application designed to support personal growth through structured daily reflection. Built for knowledge workers and personal growth enthusiasts who want to build positive mental health habits and track meaningful progress over time.

## Target User Profile

| Category | Description |
|----------|-------------|
| **Age Range** | 20–35 years old |
| **Background** | Knowledge workers, self-directed learners, recent graduates |
| **Typical Traits** | Interested in personal growth and habit-building; often use tools like Notion, Obsidian, or Google Sheets |
| **Primary Goals** | Build better habits, improve lifestyle consistency, develop self-confidence through tracking progress |
| **Pain Points** | - Existing tools (e.g., Google Sheets) are too manual and time-consuming<br>- Inconsistent check-ins lead to a loss of momentum<br>- Raw data lacks emotional reinforcement<br>- Rigid templates fail to adapt to evolving goals |
| **Motivations** | - To see their own progress clearly<br>- To feel encouraged by past achievements<br>- To discover trends and optimize behavior<br>- To affirm that meaningful change is happening |

## Product Philosophy

| Principle | Description |
|-----------|-------------|
| **Structured Flexibility** | Users can define and modify what they track—sleep, diet, mood, productivity, or any other metric that matters to them. |
| **Reinforcement Through Reflection** | The system highlights meaningful past achievements to help users stay grounded and motivated. |
| **Dynamic Goal Management** | Users can adjust their targets or focus areas over time while preserving data continuity. |
| **Long-Term Data Integrity** | All records can be exported and analyzed, ensuring personal data remains useful even years later. |

## Core Design Principles

### Human-Centered Design
- **Optional fields reduce pressure**: Only essential elements are required, encouraging authentic reflection over performance
- **Structured flexibility**: Users can define what they track while maintaining consistency
- **Encouraging experience**: Supportive language and visual cues guide reflection
- **Long-term growth**: Designed to support evolving goals while preserving data continuity

### Privacy & Data Ownership
- **Privacy-focused**: No data mining or advertising - user entries remain private
- **Data ownership**: Users maintain full ownership and export capability of their data
- **Local development**: All development and testing done locally with no external data transmission
- **User control**: Complete control over data retention and deletion

## Success Metrics & Validation

### Quantitative Success Criteria
| Metric | Definition | Success Threshold | Measurement Method |
|--------|------------|-------------------|-------------------|
| **Active Users** | Number of distinct accounts that create ≥1 entry | **> 10 users** by 4 weeks post-launch | Database query: `COUNT(DISTINCT user_id)` where `entries.count > 0` |
| **User Stickiness** | Average number of days each active user submits an entry within their first 45 days | **> 30 days** | Daily aggregation of entries per user |
| **System Stability** | Production error rate (uncaught exceptions logged per 1,000 requests) | **< 1%** | Monitoring and logging |
| **Self-Adoption** | Consecutive days the founder uses the app | **≥ 50 days** (covers full validation period) | Internal query on entries table |

### Qualitative Success Indicators
- Users report feeling more positive about their daily progress
- Interface feels intuitive and reduces friction for daily entry
- Users express confidence in data ownership through export functionality
- Daily reflection becomes a sustainable habit rather than a burden

## User Experience Requirements

### Core User Journey
1. **Onboarding**: Simple registration with email verification
   - **V3.0+ OAuth**: Google OAuth first (broad accessibility), Apple Sign-In second (V3.1), GitHub OAuth third (V3.2 if needed)
   - **Target Demographic**: Personal growth enthusiasts aged 20-35 (general consumers, not developers)
2. **Daily Entry**: Quick, structured reflection (< 5 minutes)
   - **Progressive UI**: Fields appear when content is non-empty AND meaningful (2+ characters, 300ms debounced)
   - **Entry Title**: Auto-generated using user's locale (e.g., "January 15, 2025" US, "15. Januar 2025" DE)
   - **Three Emotion Points**: Victory, Gratitude, Anxiety (255 chars each, counter at 150, highlight at 200)
   - **Overall Rating**: Radio buttons 1-5 plus "Skip rating today" option (stores NULL)
   - **Journal Content**: Main reflection area (8,000 char limit with progressive indicators at 90%/95%)
   - **Auto-save**: Draft system with 30-second intervals, finalize on user "Save Entry" action
3. **Historical Review**: Easy browsing of past entries for motivation
   - **Default Sort**: Newest first with user preference toggle ("Newest First" / "Oldest First")
   - **Entry Management**: Edit with one-level undo, Archive (hide without deletion), Delete (30-day recycle bin)
4. **Progress Recognition**: System helps users recognize patterns and growth
   - **Analytics**: Chart.js visualizations with pre-aggregated data from FastAPI endpoints
   - **Timezone Aware**: Auto-detection with manual override capability
5. **Data Ownership**: Users can export their complete history at any time
   - **Export Format**: CSV first (V3.0) for spreadsheet analysis, JSON later (V3.1) for power users

### Usability Standards
- **Mobile-first design**: Core functionality works seamlessly on mobile devices
  - **Responsive Breakpoints**: 375px (Mobile - iPhone SE+), 768px (Tablet), 1024px (Desktop), 1440px (Large desktop)
  - **Touch-optimized**: Form fields and buttons sized for touch interaction
- **Performance**: Website loads and functions correctly with focus on reliability over speed metrics
- **Accessibility**: Basic screen reader compatibility and keyboard navigation
  - **Overall Rating**: Radio buttons for 1-5 plus "Skip rating today" option for screen reader accessibility
- **Error handling**: HTMX-native error handling with contextual recovery guidance
  - **Validation**: Field-level inline errors with retry functionality
  - **Authentication**: Session expired with login redirect
  - **Network**: Connection issues with retry buttons
  - **Server**: Generic server errors with graceful fallback
- **Data safety**: Auto-save functionality prevents data loss
  - **Draft System**: Entries start as drafts, auto-save every 30 seconds, finalize on user action
  - **One-level Undo**: Previous content stored for 24-48 hours with "Undo last edit" button

## Business Model & Positioning

### Monetization Strategy
- **Simple Two-Tier Freemium**: Clear value differentiation eliminates choice paralysis
  - **Free Tier**: 30 days journal entries, basic entry form (all 11 fields), entry history viewing, basic search
  - **Premium Tier**: $4.99/month or $49.99/year
    - Unlimited journal entries
    - Advanced analytics and mood tracking
    - Data export (CSV format)
    - Multiple themes and customization
    - Priority customer support
    - Early access to new features
- **Market Positioning**: Competitive $4.99/month between Day One ($2.92/month) and Reflectly ($8.99/month)
- **Upgrade Trigger**: When users hit 30-day limit and want to keep their history
- **No advertising**: Maintains privacy and user trust in personal journaling space
- **Value proposition**: Privacy + simplicity + long-term data ownership

### Market Positioning
- **Primary differentiator**: Privacy-focused emotional reflection vs productivity-focused habit tracking
- **Competition advantage**: Human-centered design that reduces pressure vs rigid tracking systems
- **Target market**: Personal growth enthusiasts who want reflection tools, not performance optimization
- **Unique value**: Structured flexibility that adapts to user needs over time

## Product Validation Approach

### MVP Validation (Version 1.0)
- **Hypothesis**: Structured daily reflection builds sustainable positive habits
- **Key metrics**: User retention (30+ days), daily usage consistency, qualitative feedback
- **Success criteria**: 10+ active users with consistent daily entries
- **Learning goals**: Understand optimal reflection structure and user motivation patterns

### Feature Validation Framework
- **User feedback**: In-app feedback widget in settings/profile area
  - **Form Design**: "What's working well?" (500 chars), "What needs improvement?" (500 chars), "Feature request" (300 chars)
  - **Collection Method**: Non-intrusive, accessible when users want to provide input
  - **Storage**: UserFeedback model with structured data for analysis
- **Usage analytics**: Feature adoption rates and user engagement patterns
- **Retention analysis**: Which features correlate with long-term usage
- **Iteration approach**: Rapid iteration based on user behavior and feedback

---

*This document defines the product vision, user requirements, and success criteria. For feature specifications, see `core-functionality-overview.md`. For technical implementation, see `architecture.md`. For development timeline, see `roadmap.md`.*