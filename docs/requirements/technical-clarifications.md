# Technical Clarifications & Planning Questions

## 🚨 Critical - Must Answer Before Coding

### **Database Session Management Architecture**
**Impact**: High - Foundation for all data operations
- How exactly will we handle async (FastAPI-Users) vs sync (SQLModel Entry operations) session coordination?
- Will we use dependency injection for session handling? 
- How do we manage transaction boundaries between auth and business logic?
- Should we standardize on async-only or create clear separation patterns?

### **Entry Model Business Logic**
**Impact**: High - Core feature correctness
- **One Entry Per Day Rule**: Database constraint, application logic, or both?
- **Time Zone Handling**: User's local time vs server time for "daily" entries?
- **Entry Editing Constraints**: Can users edit any historical date? Time limits? Audit trail?

### **MVP Scope & Timeline Realism**
**Impact**: High - Project success
- Are estimates realistic for remaining MVP 1.0 features?
  - Entry editing (2-3 hours) - UI + backend + validation + testing
  - Entry titles (1 hour) - Custom titles with auto-generated fallback
  - Dynamic UI enhancement (2-3 hours) - Progressive field display
  - Enhanced validation (1-2 hours) - Comprehensive form validation
  - Mobile optimization (2 hours) - Responsive design improvements
- Total estimated: 8-11 hours for MVP completion
- What's our definition of "MVP 1.0 complete"? Feature completeness vs polish level?

### **Entry Editing User Experience**
**Impact**: High - Core user interaction
- **Edit Interface**: Inline editing, modal popup, or dedicated page?
- **Validation Strategy**: Same strict validation as creation or more permissive for historical entries?
- **Destructive Actions**: Confirmation dialogs for delete? Soft delete vs hard delete?
- **Autosave**: Should editing have autosave to prevent data loss?

---

## ⚠️ Important - Should Answer During Implementation

### **HTMX Integration Strategy**
**Impact**: Medium - Development approach consistency
- Which specific interactions use HTMX vs full page reloads?
- Entry form submission, editing interface, daily highlights display?
- Performance strategy: HTMX for enhancements or core functionality?

### **Entry Titles Implementation**
**Impact**: Medium - MVP feature quality
- **Title Length Limits**: Maximum character count for custom titles?
- **Auto-generation Logic**: Date format for default titles ("January 15, 2025 Journal")?
- **Validation Rules**: Character restrictions, special characters allowed?
- **Display Strategy**: How to handle very long titles in lists?

### **Dynamic UI Progressive Display**
**Impact**: Medium - User experience quality
- **Field Show Logic**: Exactly when does next field appear (on focus, on content, on blur)?
- **Performance Considerations**: JavaScript approach vs server-side rendering?
- **Mobile Behavior**: Different logic for touch interfaces?
- **Accessibility**: Screen reader compatibility with dynamic field appearance?

### **Session Management Details**
**Impact**: Medium - Security & UX
- **Session Duration**: How long should sessions last? Remember me functionality?
- **Multi-Device Support**: Concurrent sessions or single session enforcement?
- **Session Invalidation**: Triggers for session expiry (password change, etc.)?

### **Error Handling Philosophy**
**Impact**: Medium - User experience quality
- **User Messaging**: Technical error details vs user-friendly messages?
- **Recovery Actions**: What can users do when operations fail?
- **Graceful Degradation**: Behavior when external services are unavailable?

### **Mobile Experience Priorities**
**Impact**: Medium - User accessibility
- **Critical Mobile Flows**: Which features must work flawlessly on mobile?
- **Performance Targets**: Page load times for mobile networks?
- **Touch Interface**: Swipe gestures, optimal touch target sizing?

---

## 📋 Nice to Know - Can Address Later

### **Version 2.0 - Health Tracking Features**
**Impact**: Low - Future development phase
- **Health Module Architecture**: Enable/disable entire sections, sub-module toggles?
- **Diet Tracking Modes**: Light mode (satisfaction) vs Standard mode (macros) implementation?
- **Exercise Tracking Logic**: "Did you work out?" branching UI design?
- **Data Storage**: Additional database tables vs extended Entry model?

### **Version 3.0+ - Advanced Features**
**Impact**: Low - Long-term roadmap
- **Data Export Specifications**: All-time data, date range selection, file size management?
- **Custom Fields System**: Database schema for user-defined fields?
- **Advanced Analytics**: Trend calculation algorithms, pattern recognition logic?
- **API Design**: REST endpoints structure, authentication for third-party access?

### **Daily Highlight Feature (V3.0+)**
**Impact**: Low - Future feature
- **Selection Algorithm**: Random positive entries, recent entries, or weighted by rating?
- **Display Logic**: Daily refresh, login-based, or user-configurable?
- **Content Strategy**: Full entry display or just success highlights?

### **OAuth Integration (Future)**
**Impact**: Low - Enhancement feature
- **Provider Selection**: Google/GitHub priority, scope requirements?
- **Account Linking**: Merging OAuth with existing email accounts?
- **Fallback Strategy**: Behavior when OAuth services unavailable?

### **Production Deployment Architecture**
**Impact**: Low - Infrastructure concern
- **AWS Service Selection**: EC2 vs ECS vs Lambda for hosting?
- **Database Sizing**: PostgreSQL instance size for user base estimation?
- **Cost Estimation**: Monthly AWS infrastructure costs planning?
- **Backup Strategy**: Database backups, disaster recovery procedures?

### **Email System Production Setup**
**Impact**: Low - Production infrastructure
- **SMTP Provider**: SendGrid, AWS SES, or alternative service selection?
- **Template Management**: File-based vs database-stored email templates?
- **Production Testing**: Email flow testing strategy for production environment?

### **Testing Strategy Details**
**Impact**: Low - Process improvement
- **Unit Test Coverage**: Which components need comprehensive unit testing?
- **Integration Test Scope**: Authentication flows, database operations?
- **E2E Test Automation**: Critical user journeys to automate?
- **Performance Testing**: Load testing for AWS instance sizing?

### **Monitoring & Observability**
**Impact**: Low - Operational maturity
- **Application Monitoring**: Error tracking, performance metrics setup?
- **Business Analytics**: User engagement, feature usage tracking?
- **Alerting Strategy**: Conditions requiring immediate attention?

### **Data Privacy & Compliance**
**Impact**: Low - Legal/compliance
- **GDPR Compliance**: Account deletion, data export, right to be forgotten?
- **Data Retention**: Entry preservation after account deletion?
- **Audit Logging**: Entry modification tracking, access pattern logging?

### **Production Transition Planning**
**Impact**: Low - Deployment logistics
- **Cross-Platform Development**: Software version consistency, platform differences?
- **Documentation Requirements**: Complete setup guides for production deployment?
- **AWS Account Structure**: Account setup, billing, access management planning?

---

## 🎯 Strategic Decision Points

### **Quality vs Speed Trade-offs**
- **Technical Debt Tolerance**: Acceptable shortcuts for MVP that we'll refactor in V2.0?
- **Feature Depth**: Deep implementation of fewer features vs basic implementation of more features?

### **User Feedback Strategy**
- **MVP Testing**: Plan for gathering user feedback before Calgary?
- **Iteration Approach**: How will we incorporate feedback during development?

### **Scalability Preparation**
- **Architecture Decisions**: How much should we architect for future scale vs current MVP needs?
- **Performance Baseline**: What performance characteristics do we need to establish?

---

## 📝 Next Steps

1. **Critical Questions**: Address all items in "Must Answer Before Coding" section
2. **Implementation Planning**: Create detailed technical specifications for core features
3. **Timeline Validation**: Refine estimates based on architectural decisions
4. **Risk Assessment**: Identify potential blockers and mitigation strategies

---

*Created: July 14, 2025*
*Purpose: Ensure comprehensive planning before implementation to minimize rework*