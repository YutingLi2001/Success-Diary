# Error Handling Specification

## Overview

This specification defines the error handling strategy for the Success-Diary application, emphasizing HTMX-native patterns with progressive enhancement capabilities.

## Requirements

### Error Handling Strategy

**HTMX-First Approach**:
- Return HTML fragments for HTMX requests
- JSON fallback for standard API calls
- Single error handler prevents dual maintenance
- Progressive enhancement for future UI improvements

**Error Categories**:
- **Validation**: Field-level inline errors with retry guidance
- **Authentication**: Session expired with login redirect
- **Network**: Connection issues with retry functionality
- **Server**: Generic server errors with graceful fallback

## Technical Implementation

### Core Error Handler

```python
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# Error data structure
class ErrorData:
    def __init__(
        self,
        code: str,
        message: str,
        severity: str = "error",
        ui_hint: str = "inline",
        recoverable: bool = True,
        context: str = "general"
    ):
        self.code = code
        self.message = message
        self.severity = severity  # error, warning, info
        self.ui_hint = ui_hint    # inline, toast, modal
        self.recoverable = recoverable
        self.context = context

# Unified error handler
async def handle_error(request: Request, error: ErrorData, status_code: int = 400):
    error_dict = {
        "code": error.code,
        "message": error.message,
        "severity": error.severity,
        "ui_hint": error.ui_hint,
        "recoverable": error.recoverable,
        "context": error.context
    }
    
    # HTMX request detection
    if request.headers.get("HX-Request"):
        return templates.TemplateResponse(
            "fragments/error.html",
            {
                "request": request,
                "error": error_dict
            },
            status_code=status_code
        )
    
    # Standard JSON response
    return JSONResponse(
        content={"error": error_dict},
        status_code=status_code
    )

# Application error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_data = ErrorData(
        code=f"HTTP_{exc.status_code}",
        message=exc.detail,
        severity="error",
        recoverable=exc.status_code < 500
    )
    
    return await handle_error(request, error_data, exc.status_code)

@app.exception_handler(ValueError)
async def validation_error_handler(request: Request, exc: ValueError):
    error_data = ErrorData(
        code="VALIDATION_ERROR",
        message=str(exc),
        severity="warning",
        ui_hint="inline",
        recoverable=True,
        context="validation"
    )
    
    return await handle_error(request, error_data, 400)
```

### Specific Error Types

```python
# Authentication errors
class AuthenticationError(Exception):
    def __init__(self, message: str = "Authentication required"):
        self.message = message
        super().__init__(self.message)

@app.exception_handler(AuthenticationError)
async def auth_error_handler(request: Request, exc: AuthenticationError):
    error_data = ErrorData(
        code="AUTHENTICATION_REQUIRED",
        message=exc.message,
        severity="warning",
        ui_hint="modal",
        recoverable=True,
        context="auth"
    )
    
    return await handle_error(request, error_data, 401)

# Network/connectivity errors
class NetworkError(Exception):
    def __init__(self, message: str = "Network connection failed"):
        self.message = message
        super().__init__(self.message)

@app.exception_handler(NetworkError)
async def network_error_handler(request: Request, exc: NetworkError):
    error_data = ErrorData(
        code="NETWORK_ERROR",
        message=exc.message,
        severity="error",
        ui_hint="toast",
        recoverable=True,
        context="network"
    )
    
    return await handle_error(request, error_data, 503)

# Server errors
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    # Log the actual error for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    error_data = ErrorData(
        code="INTERNAL_ERROR",
        message="Something went wrong. Please try again.",
        severity="error",
        ui_hint="toast",
        recoverable=True,
        context="server"
    )
    
    return await handle_error(request, error_data, 500)
```

### Frontend Error Templates

```html
<!-- templates/fragments/error.html -->
<div class="error-container" 
     data-error-code="{{ error.code }}"
     data-error-severity="{{ error.severity }}"
     data-error-context="{{ error.context }}">
  
  {% if error.ui_hint == "inline" %}
    <div class="error-inline {{ error.severity }}">
      <div class="error-icon">
        {% if error.severity == "error" %}⚠️{% endif %}
        {% if error.severity == "warning" %}⚠️{% endif %}
        {% if error.severity == "info" %}ℹ️{% endif %}
      </div>
      <div class="error-content">
        <p class="error-message">{{ error.message }}</p>
        {% if error.recoverable %}
          <div class="error-actions">
            {% if error.context == "validation" %}
              <button type="button" onclick="focusInvalidField()">Review Input</button>
            {% elif error.context == "auth" %}
              <button type="button" onclick="redirectToLogin()">Sign In</button>
            {% elif error.context == "network" %}
              <button type="button" onclick="retryRequest()">Try Again</button>
            {% endif %}
          </div>
        {% endif %}
      </div>
    </div>
  {% endif %}
  
  {% if error.ui_hint == "toast" %}
    <div class="error-toast {{ error.severity }}" id="error-toast">
      <div class="toast-content">
        <span class="toast-message">{{ error.message }}</span>
        {% if error.recoverable %}
          <button type="button" class="toast-action" onclick="handleToastAction('{{ error.context }}')">
            {% if error.context == "network" %}Retry{% else %}Dismiss{% endif %}
          </button>
        {% endif %}
      </div>
    </div>
  {% endif %}
  
  {% if error.ui_hint == "modal" %}
    <div class="error-modal-overlay" id="error-modal">
      <div class="error-modal {{ error.severity }}">
        <div class="modal-header">
          <h3>{{ error.message }}</h3>
          <button type="button" class="modal-close" onclick="closeErrorModal()">&times;</button>
        </div>
        <div class="modal-content">
          {% if error.context == "auth" %}
            <p>Your session has expired. Please sign in again to continue.</p>
            <div class="modal-actions">
              <button type="button" onclick="redirectToLogin()" class="primary">Sign In</button>
              <button type="button" onclick="closeErrorModal()">Cancel</button>
            </div>
          {% endif %}
        </div>
      </div>
    </div>
  {% endif %}
  
</div>

<script>
// Error handling JavaScript
function focusInvalidField() {
  const invalidInput = document.querySelector('[data-invalid]');
  if (invalidInput) {
    invalidInput.focus();
    invalidInput.scrollIntoView({ behavior: 'smooth' });
  }
}

function redirectToLogin() {
  window.location.href = '/auth/login';
}

function retryRequest() {
  // Retry the last HTMX request
  const lastRequest = htmx.lastRequest;
  if (lastRequest) {
    htmx.ajax(lastRequest.verb, lastRequest.path, lastRequest.target);
  }
}

function handleToastAction(context) {
  switch(context) {
    case 'network':
      retryRequest();
      break;
    default:
      dismissToast();
  }
}

function dismissToast() {
  const toast = document.getElementById('error-toast');
  if (toast) {
    toast.remove();
  }
}

function closeErrorModal() {
  const modal = document.getElementById('error-modal');
  if (modal) {
    modal.remove();
  }
}

// Auto-dismiss toasts after 5 seconds
setTimeout(() => {
  const toast = document.getElementById('error-toast');
  if (toast) {
    toast.classList.add('fade-out');
    setTimeout(() => dismissToast(), 300);
  }
}, 5000);
</script>
```

### CSS Styling

```css
/* Error container base styles */
.error-container {
  margin: 1rem 0;
}

/* Inline error styles */
.error-inline {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}

.error-inline.error {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.error-inline.warning {
  background-color: #fffbeb;
  border: 1px solid #fed7aa;
  color: #92400e;
}

.error-inline.info {
  background-color: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1e40af;
}

.error-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.error-content {
  flex: 1;
}

.error-message {
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.error-actions {
  display: flex;
  gap: 0.5rem;
}

.error-actions button {
  padding: 0.25rem 0.75rem;
  border: 1px solid currentColor;
  background: transparent;
  color: inherit;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.error-actions button:hover {
  background: currentColor;
  color: white;
}

/* Toast error styles */
.error-toast {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
  min-width: 300px;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  animation: slideIn 0.3s ease-out;
}

.error-toast.error {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.error-toast.warning {
  background-color: #fffbeb;
  border: 1px solid #fed7aa;
  color: #92400e;
}

.toast-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.toast-action {
  padding: 0.25rem 0.75rem;
  border: 1px solid currentColor;
  background: transparent;
  color: inherit;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.875rem;
  white-space: nowrap;
}

.error-toast.fade-out {
  animation: slideOut 0.3s ease-in;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOut {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(100%);
    opacity: 0;
  }
}

/* Modal error styles */
.error-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.error-modal {
  background: white;
  border-radius: 0.5rem;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
}

.modal-content {
  padding: 1.5rem;
}

.modal-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.modal-actions button {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.25rem;
  cursor: pointer;
}

.modal-actions button.primary {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}
```

## Error Recovery Patterns

### Validation Errors
- **Inline feedback**: Show error next to invalid field
- **Focus management**: Scroll to and focus invalid input
- **Progressive validation**: Real-time feedback as user types
- **Clear recovery**: Specific guidance on fixing the error

### Authentication Errors
- **Session expiration**: Modal with login redirect
- **Permission denied**: Clear explanation and alternative actions
- **Rate limiting**: Temporary restriction with retry timing

### Network Errors
- **Connection failed**: Retry button with exponential backoff
- **Timeout**: Clear timeout message with manual retry
- **Server errors**: Generic message with retry option

## Testing Requirements

### Unit Tests
```python
def test_error_handler_htmx_request():
    # Test HTMX request returns HTML fragment
    pass

def test_error_handler_json_request():
    # Test standard request returns JSON
    pass

def test_error_categories():
    # Test different error types return appropriate responses
    pass
```

### Integration Tests
- Error handling across different request types
- Template rendering for error fragments
- JavaScript error recovery functions
- Accessibility of error messages

## References

- HTMX error handling patterns
- Web accessibility guidelines for error messages
- User experience best practices for error recovery