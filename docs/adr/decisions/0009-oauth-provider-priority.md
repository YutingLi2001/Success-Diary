# ADR-0009: OAuth Provider Priority Strategy

## Status

Accepted

## Context

The Success-Diary application will implement OAuth integration in V3.0+ to reduce authentication friction and appeal to users preferring social login. Key considerations include:

- **Target Audience**: Personal growth enthusiasts aged 20-35, general consumers (not developers)
- **Device Usage**: Mobile + desktop cross-platform usage patterns
- **User Privacy**: Balance between convenience and privacy concerns
- **Implementation Resources**: Limited development time requires strategic provider selection
- **Market Adoption**: Provider popularity within target demographic

## Decision

Implement OAuth providers in strategic priority order:

1. **Google OAuth** (V3.0 initial release)
2. **Apple Sign-In** (V3.1 follow-up)
3. **GitHub OAuth** (V3.2 if needed based on user demand)

## Considered Options

1. **Google first**: Broad accessibility, familiar UX
2. **Apple first**: Privacy-focused, mobile-optimized
3. **GitHub first**: Developer-friendly but narrow appeal
4. **Multiple providers simultaneously**: Comprehensive but complex
5. **Facebook/Meta OAuth**: High adoption but privacy concerns

## Consequences

**Positive:**
- Google OAuth provides broad accessibility across all platforms
- Familiar authentication flow for target demographic
- Mobile-friendly implementation with excellent cross-platform support
- High adoption rate among general consumers
- Apple Sign-In adds privacy appeal for iOS users

**Negative:**
- Dependency on Google's OAuth infrastructure and policies
- Privacy concerns for users wanting to avoid Google ecosystem
- Additional complexity with multiple provider implementations

**Neutral:**
- Standard approach for consumer-facing applications
- Well-documented OAuth implementation patterns

## Implementation Notes

**Google OAuth Configuration:**
```python
# OAuth configuration
GOOGLE_OAUTH_CONFIG = {
    "client_id": os.getenv("GOOGLE_CLIENT_ID"),
    "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
    "scopes": ["openid", "email", "profile"],
    "redirect_uri": f"{BASE_URL}/auth/google/callback",
    "authorization_url": "https://accounts.google.com/o/oauth2/auth",
    "token_url": "https://oauth2.googleapis.com/token"
}

# FastAPI OAuth integration
@app.get("/auth/google")
async def google_oauth_login():
    return RedirectResponse(
        url=f"{GOOGLE_OAUTH_CONFIG['authorization_url']}?"
        f"client_id={GOOGLE_OAUTH_CONFIG['client_id']}&"
        f"redirect_uri={GOOGLE_OAUTH_CONFIG['redirect_uri']}&"
        f"scope={' '.join(GOOGLE_OAUTH_CONFIG['scopes'])}&"
        f"response_type=code&"
        f"state={generate_state_token()}"
    )

@app.get("/auth/google/callback")
async def google_oauth_callback(code: str, state: str):
    # Exchange code for access token
    # Create or link user account
    # Generate session token
    pass
```

**Apple Sign-In Configuration (V3.1):**
```python
# Apple Sign-In configuration
APPLE_OAUTH_CONFIG = {
    "client_id": os.getenv("APPLE_CLIENT_ID"),
    "team_id": os.getenv("APPLE_TEAM_ID"),
    "key_id": os.getenv("APPLE_KEY_ID"),
    "private_key": os.getenv("APPLE_PRIVATE_KEY"),
    "scopes": ["name", "email"],
    "redirect_uri": f"{BASE_URL}/auth/apple/callback"
}
```

**Database Schema:**
```sql
-- OAuth provider integration
CREATE TABLE oauth_accounts (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    provider VARCHAR(50) NOT NULL,        -- 'google', 'apple', 'github'
    provider_user_id VARCHAR(100) NOT NULL,
    email VARCHAR(255),
    name VARCHAR(255),
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User model updates
ALTER TABLE users ADD COLUMN oauth_only BOOLEAN DEFAULT FALSE;
```

**Frontend Integration:**
```javascript
// OAuth login buttons
const initiateOAuthLogin = (provider) => {
  window.location.href = `/auth/${provider}`;
};

// Social login UI
<div className="social-login">
  <button onClick={() => initiateOAuthLogin('google')} className="oauth-button google">
    <GoogleIcon /> Sign in with Google
  </button>
  
  <button onClick={() => initiateOAuthLogin('apple')} className="oauth-button apple">
    <AppleIcon /> Sign in with Apple
  </button>
</div>
```

**Implementation Timeline:**
- **V3.0**: Google OAuth implementation and testing
- **V3.1**: Apple Sign-In integration
- **V3.2**: GitHub OAuth (if user demand warrants)
- **Future**: Additional providers based on user feedback

## References

- Google OAuth 2.0 documentation
- Apple Sign-In implementation guide
- FastAPI OAuth integration patterns
- OAuth security best practices
- Original analysis: `docs/requirements/remaining_requirements_analysis.md` (Section 11)