/**
 * Shared error handling JavaScript functions
 * Used across inline, toast, and modal error templates
 */

// Store last HTMX request for retry functionality
let lastHtmxRequest = null;

// Track HTMX requests for retry functionality
document.addEventListener('htmx:configRequest', function(event) {
    lastHtmxRequest = {
        verb: event.detail.verb,
        path: event.detail.path,
        target: event.target,
        headers: event.detail.headers,
        parameters: event.detail.parameters
    };
});

/**
 * Redirect to login page
 */
function redirectToLogin() {
    // Store current page for redirect after login
    const currentPath = window.location.pathname + window.location.search;
    if (currentPath !== '/login') {
        sessionStorage.setItem('redirect_after_login', currentPath);
    }
    window.location.href = '/login';
}

/**
 * Retry the last HTMX request
 */
function retryLastRequest() {
    if (typeof htmx !== 'undefined' && lastHtmxRequest) {
        // Show loading state if possible
        const target = lastHtmxRequest.target;
        if (target) {
            target.classList.add('htmx-request');
        }
        
        // Retry the request
        htmx.ajax(lastHtmxRequest.verb, lastHtmxRequest.path, {
            target: lastHtmxRequest.target,
            headers: lastHtmxRequest.headers,
            values: lastHtmxRequest.parameters
        });
    } else {
        // Fallback: reload the page
        window.location.reload();
    }
}

/**
 * Focus on the first invalid field in the form
 */
function focusInvalidField() {
    // Look for fields with validation errors in order of preference
    const selectors = [
        '[data-invalid="true"]',
        '.border-red-300',
        '.border-red-500', 
        'input:invalid',
        '.error input',
        '.has-error input'
    ];
    
    let invalidInput = null;
    for (const selector of selectors) {
        invalidInput = document.querySelector(selector);
        if (invalidInput) break;
    }
    
    if (invalidInput) {
        // Focus and scroll to the field
        invalidInput.focus();
        invalidInput.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        
        // Highlight the field briefly for visual feedback
        const originalClasses = invalidInput.className;
        invalidInput.className += ' ring-2 ring-red-300 ring-opacity-50 transition-all duration-200';
        
        setTimeout(() => {
            invalidInput.className = originalClasses;
        }, 2000);
    }
}

/**
 * Show a success message (useful for positive feedback)
 */
function showSuccessMessage(message, duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 z-50 bg-green-50 border border-green-200 text-green-800 p-4 rounded-lg shadow-lg transform transition-all duration-300 ease-out';
    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <span class="text-lg">✅</span>
            <p class="font-medium">${message}</p>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-green-400 hover:text-green-600">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        </div>
    `;
    
    // Start off-screen
    toast.style.transform = 'translateX(100%)';
    toast.style.opacity = '0';
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
        toast.style.opacity = '1';
    }, 100);
    
    // Auto-dismiss
    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        toast.style.opacity = '0';
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300);
    }, duration);
}

/**
 * Handle form validation display
 */
function displayValidationError(fieldName, message) {
    const field = document.querySelector(`[name="${fieldName}"]`);
    if (!field) return;
    
    // Remove existing error
    const existingError = field.parentElement.querySelector('.validation-error');
    if (existingError) {
        existingError.remove();
    }
    
    // Add error styling to field
    field.classList.add('border-red-300', 'focus:border-red-500', 'focus:ring-red-500');
    field.setAttribute('data-invalid', 'true');
    field.setAttribute('aria-invalid', 'true');
    
    // Create error message element
    const errorElement = document.createElement('div');
    errorElement.className = 'validation-error mt-1 text-sm text-red-600';
    errorElement.textContent = message;
    errorElement.setAttribute('role', 'alert');
    
    // Insert error message after the field
    field.parentElement.appendChild(errorElement);
    
    // Remove error styling when field is corrected
    field.addEventListener('input', function clearValidation() {
        field.classList.remove('border-red-300', 'focus:border-red-500', 'focus:ring-red-500');
        field.removeAttribute('data-invalid');
        field.removeAttribute('aria-invalid');
        
        const errorMsg = field.parentElement.querySelector('.validation-error');
        if (errorMsg) {
            errorMsg.remove();
        }
        
        field.removeEventListener('input', clearValidation);
    }, { once: true });
}

/**
 * Clear all validation errors from a form
 */
function clearValidationErrors(formElement = document) {
    // Remove error styling from fields
    const invalidFields = formElement.querySelectorAll('[data-invalid="true"]');
    invalidFields.forEach(field => {
        field.classList.remove('border-red-300', 'focus:border-red-500', 'focus:ring-red-500');
        field.removeAttribute('data-invalid');
        field.removeAttribute('aria-invalid');
    });
    
    // Remove error messages
    const errorMessages = formElement.querySelectorAll('.validation-error');
    errorMessages.forEach(error => error.remove());
}

/**
 * Utility function to check if user is online
 */
function isOnline() {
    return navigator.onLine;
}

/**
 * Handle network status changes
 */
window.addEventListener('online', function() {
    showSuccessMessage('Connection restored');
});

window.addEventListener('offline', function() {
    const toast = document.createElement('div');
    toast.className = 'fixed top-4 right-4 z-50 bg-yellow-50 border border-yellow-200 text-yellow-800 p-4 rounded-lg shadow-lg';
    toast.innerHTML = `
        <div class="flex items-center gap-3">
            <span class="text-lg">⚠️</span>
            <p class="font-medium">You appear to be offline</p>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Remove when back online
    function removeOfflineToast() {
        if (toast.parentElement) {
            toast.remove();
        }
        window.removeEventListener('online', removeOfflineToast);
    }
    window.addEventListener('online', removeOfflineToast);
});