# Development Notes & Findings

*Small discoveries, blockers, and ideas collected during development*

---

## 🔐 OAuth Implementation Status (July 13, 2025)

### Current Implementation
- ✅ **Code Complete**: Google OAuth and GitHub OAuth fully implemented
- ✅ **UI Updated**: Beautiful OAuth buttons added to login/register pages
- ✅ **Dependencies**: httpx-oauth installed and configured
- ✅ **Backend Routes**: `/auth/google/` and `/auth/github/` endpoints ready

### 🚧 **Deployment Blockers Found**

#### Google OAuth Limitations
- **Issue**: Google OAuth free service only lasts **90 days**
- **Impact**: Not suitable for long-term production without paid plan
- **Status**: Code implemented but not activated
- **Recommendation**: Consider for post-launch when revenue justifies cost

#### GitHub OAuth Requirements
- **Issue**: GitHub OAuth requires the service to be **already deployed**
- **Impact**: Cannot test locally, needs production URL first
- **Status**: Code implemented but not testable until deployment
- **Recommendation**: Activate after AWS deployment is complete

### 🎯 **Current Decision**
- Keep OAuth code in place for future activation
- Focus on email authentication for MVP launch
- Revisit OAuth after successful deployment and user traction

---

## 💡 Ideas & Future Enhancements

### Authentication
- [ ] Consider alternative OAuth providers (Discord, Twitter) for free options
- [ ] Implement social login after paid plan consideration
- [ ] Add "Remember Me" functionality for email login

### User Experience
- [ ] Add password strength indicator on registration
- [ ] Implement "Login with Magic Link" as email-only alternative
- [ ] Add profile picture support (when OAuth is activated)

---

## 🐛 Known Issues & Workarounds

*None currently documented*

---

## 📝 Development Insights

### FastAPI-Users OAuth Integration
- OAuth implementation is straightforward with fastapi-users
- `associate_by_email=True` automatically links accounts with same email
- `is_verified_by_default=True` skips email verification for OAuth users

### Frontend OAuth Buttons
- Google and GitHub SVG icons embedded for consistent styling
- Tailwind CSS grid layout works well for multiple OAuth options
- "Or continue with" divider provides clear visual separation

---

*Last Updated: July 13, 2025*
*Next Review: Post-AWS deployment*