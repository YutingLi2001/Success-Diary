# ADR-0002: Authentication System - Email Verification Implementation

## Status

Accepted

## Context

The Success-Diary application requires a secure authentication system that balances security with user experience. Key considerations include:

- **User Base**: Personal growth enthusiasts aged 20-35
- **Security Requirements**: Email verification for account validation
- **Development Constraints**: FastAPI-Users framework already selected
- **User Experience**: Minimize friction while maintaining security
- **Email Infrastructure**: Development vs. production email delivery

## Decision

Implement email verification using FastAPI-Users with 6-digit verification codes:
- **Framework**: FastAPI-Users 14.0.1 for core authentication
- **Verification Method**: 6-digit numeric codes sent via email
- **Code Expiration**: 10-minute validity window
- **Email Service**: Mailpit for development, production SMTP for deployment
- **Session Management**: JWT-based with secure cookies

## Considered Options

1. **Password-only authentication**: Simple but less secure
2. **Social OAuth only**: Convenient but limits user control
3. **Email verification with codes (Selected)**: Balanced security and UX
4. **SMS verification**: More secure but adds complexity and cost
5. **Magic links**: User-friendly but potential email client issues

## Consequences

**Positive:**
- Strong account security with email ownership verification
- Familiar user experience with verification codes
- FastAPI-Users provides robust, tested authentication foundation
- Mailpit enables full email testing in development
- Scalable architecture supports future OAuth integration

**Negative:**
- Additional development complexity compared to password-only
- Dependency on email delivery reliability
- User friction during account creation process
- Email configuration required for both development and production

**Neutral:**
- Standard practice for modern web applications
- Well-documented FastAPI-Users patterns
- Mixed async/sync database sessions required

## Implementation Notes

**Technical Architecture:**
```python
# Core authentication components
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

# Email verification system
class EmailVerificationCode:
    code: str  # 6-digit numeric
    expiry: datetime  # 10-minute window
    user_id: int
```

**Development Environment:**
- **Email Server**: Mailpit running on localhost:8025
- **Email Interface**: Web UI at http://localhost:8025
- **SMTP Config**: localhost:1025 for development

**Production Environment:**
- **Email Service**: Production SMTP provider (AWS SES, SendGrid, etc.)
- **SSL/TLS**: Secure email transmission
- **Monitoring**: Email delivery and bounce tracking

**Security Considerations:**
- Code expiration prevents replay attacks
- Rate limiting on verification attempts
- Secure session management with JWT
- Email ownership validation

## References

- FastAPI-Users documentation
- Email verification best practices
- JWT authentication patterns
- Mailpit development email testing
- Original planning: Authentication system requirements