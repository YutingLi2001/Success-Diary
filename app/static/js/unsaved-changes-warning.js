/**
 * Unsaved Changes Warning System
 * Prevents users from accidentally losing edits when navigating away
 */

class UnsavedChangesWarning {
    constructor() {
        this.hasUnsavedChanges = false;
        this.originalFormData = {};
        this.form = null;
        this.init();
    }
    
    init() {
        // Only initialize on pages with edit forms
        this.form = document.querySelector('#entry-form');
        if (!this.form) return;
        
        // Capture original form data
        this.captureOriginalData();
        
        // Setup change detection
        this.setupChangeDetection();
        
        // Setup navigation warnings
        this.setupNavigationWarnings();
        
        // Handle form submission (remove warning)
        this.setupFormSubmission();
    }
    
    captureOriginalData() {
        const formData = new FormData(this.form);
        this.originalFormData = {};
        
        for (let [key, value] of formData.entries()) {
            this.originalFormData[key] = value;
        }
    }
    
    setupChangeDetection() {
        // Monitor all form inputs for changes
        const inputs = this.form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.checkForChanges();
            });
            
            input.addEventListener('change', () => {
                this.checkForChanges();
            });
        });
    }
    
    checkForChanges() {
        const currentFormData = new FormData(this.form);
        let hasChanges = false;
        
        // Check if any field has changed
        for (let [key, value] of currentFormData.entries()) {
            const originalValue = this.originalFormData[key] || '';
            if (value !== originalValue) {
                hasChanges = true;
                break;
            }
        }
        
        // Also check if any original fields are now missing
        if (!hasChanges) {
            for (let [key, originalValue] of Object.entries(this.originalFormData)) {
                const currentValue = currentFormData.get(key) || '';
                if (currentValue !== originalValue) {
                    hasChanges = true;
                    break;
                }
            }
        }
        
        this.hasUnsavedChanges = hasChanges;
        this.updateUI();
    }
    
    updateUI() {
        // Add visual indication of unsaved changes
        const submitButton = this.form.querySelector('button[type="submit"]');
        if (submitButton) {
            if (this.hasUnsavedChanges) {
                submitButton.classList.add('bg-orange-600', 'hover:bg-orange-700');
                submitButton.classList.remove('bg-blue-600', 'hover:bg-blue-700');
                submitButton.setAttribute('data-unsaved', 'true');
            } else {
                submitButton.classList.remove('bg-orange-600', 'hover:bg-orange-700');
                submitButton.classList.add('bg-blue-600', 'hover:bg-blue-700');
                submitButton.removeAttribute('data-unsaved');
            }
        }
    }
    
    setupNavigationWarnings() {
        // Browser navigation warning
        window.addEventListener('beforeunload', (e) => {
            if (this.hasUnsavedChanges) {
                const message = 'You have unsaved changes. Are you sure you want to leave?';
                e.returnValue = message;
                return message;
            }
        });
        
        // Custom navigation warning for internal links
        document.addEventListener('click', (e) => {
            if (!this.hasUnsavedChanges) return;
            
            const link = e.target.closest('a[href]');
            if (!link) return;
            
            // Skip if it's the cancel button or form submission
            if (link.closest('form') || link.getAttribute('data-no-warning')) return;
            
            // Check if it's an internal navigation link
            const href = link.getAttribute('href');
            if (href && !href.startsWith('http') && !href.startsWith('mailto') && !href.startsWith('tel')) {
                e.preventDefault();
                
                if (confirm('You have unsaved changes. Are you sure you want to leave this page?')) {
                    // User confirmed, navigate
                    this.hasUnsavedChanges = false; // Prevent double warning
                    window.location.href = href;
                }
            }
        });
    }
    
    setupFormSubmission() {
        this.form.addEventListener('submit', () => {
            // Clear warning when form is submitted
            this.hasUnsavedChanges = false;
        });
    }
    
    // Public method to clear warnings (useful for programmatic navigation)
    clearWarning() {
        this.hasUnsavedChanges = false;
        this.updateUI();
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.unsavedChangesWarning = new UnsavedChangesWarning();
    });
} else {
    window.unsavedChangesWarning = new UnsavedChangesWarning();
}