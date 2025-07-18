/**
 * Progressive Validation Engine for Success-Diary
 * 
 * Provides real-time form validation with character counting, debounced validation,
 * and integration with the existing error handling system.
 */

class ValidationEngine {
    constructor(formElement, config) {
        this.form = formElement;
        this.config = config;
        this.debounceTimers = new Map();
        this.validationState = new Map();
        this.characterCounters = new Map();
        
        this.init();
    }
    
    init() {
        this.setupCharacterCounters();
        this.setupFieldValidation();
        this.setupFormValidation();
        
        console.log('ValidationEngine initialized for form:', this.form.id || 'unnamed');
    }
    
    /**
     * Setup character counters for fields with character limits
     */
    setupCharacterCounters() {
        Object.entries(this.config.characterLimits || {}).forEach(([fieldName, limitConfig]) => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (!field) return;
            
            // Create counter element
            const counter = this.createCharacterCounter(fieldName, limitConfig);
            this.insertCharacterCounter(field, counter);
            
            // Setup real-time character counting
            field.addEventListener('input', (event) => {
                this.updateCharacterCounter(fieldName, event.target.value, limitConfig);
            });
            
            // Initial counter update
            this.updateCharacterCounter(fieldName, field.value, limitConfig);
            
            this.characterCounters.set(fieldName, counter);
        });
    }
    
    /**
     * Create character counter element
     */
    createCharacterCounter(fieldName, limitConfig) {
        const counter = document.createElement('div');
        counter.id = `char-counter-${fieldName}`;
        counter.className = 'character-counter text-sm mt-1 transition-all duration-200';
        counter.setAttribute('data-testid', `char-counter-${fieldName}`);
        counter.style.display = 'none'; // Initially hidden
        
        return counter;
    }
    
    /**
     * Insert character counter after field
     */
    insertCharacterCounter(field, counter) {
        // Insert counter after the field's parent container or after the field itself
        const container = field.closest('.form-field') || field.parentElement;
        container.appendChild(counter);
    }
    
    /**
     * Update character counter display and styling with improved UX
     */
    updateCharacterCounter(fieldName, value, limitConfig) {
        const counter = this.characterCounters.get(fieldName);
        if (!counter) return;
        
        const length = value.length;
        const maxLength = limitConfig.maxLength;
        const showCounterAt = limitConfig.showCounterAt || (maxLength * 0.85); // Default to 85%
        const warningAt = maxLength * limitConfig.warningThreshold;   // 90%
        const dangerAt = maxLength * limitConfig.highlightThreshold;  // 95%
        
        // Show counter only when approaching limits (85%+)
        if (length >= showCounterAt) {
            counter.style.display = 'block';
            
            // Format counter text cleanly - prioritizing readability
            if (maxLength >= 1000) {
                // For large numbers (journal), use comma formatting
                const formattedLength = length.toLocaleString();
                const formattedMax = maxLength.toLocaleString();
                counter.textContent = `${formattedLength} / ${formattedMax}`;
            } else {
                counter.textContent = `${length} / ${maxLength}`;
            }
        } else {
            counter.style.display = 'none';
            return; // Exit early if counter is hidden
        }
        
        // Apply clean, minimal styling - respecting the wellness app context
        counter.className = 'character-counter text-sm mt-1 text-right transition-all duration-300 ease-in-out';
        
        if (length >= maxLength) {
            // At limit - clear but not alarming red
            counter.className += ' text-red-600 font-semibold';
            counter.setAttribute('aria-label', 'Character limit reached');
        } else if (length >= dangerAt) {
            // 95%+ - gentle warning red
            counter.className += ' text-red-500 font-medium';
            counter.setAttribute('aria-label', 'Approaching character limit');
        } else if (length >= warningAt) {
            // 90%+ - subtle amber caution
            counter.className += ' text-amber-600';
            counter.setAttribute('aria-label', 'Character limit warning');
        } else {
            // 85-89% - very subtle gray, barely noticeable
            counter.className += ' text-gray-400';
            counter.setAttribute('aria-label', 'Character count');
        }
        
        // Prevent text overflow with user feedback
        if (length > maxLength) {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                // Truncate to limit
                field.value = value.substring(0, maxLength);
                
                // Show brief feedback that limit was reached
                counter.style.transform = 'scale(1.05)';
                setTimeout(() => {
                    counter.style.transform = 'scale(1)';
                }, 200);
                
                // Trigger input event to update counter
                field.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    }
    
    /**
     * Setup field-level validation with appropriate triggers
     */
    setupFieldValidation() {
        const rules = this.config.rules || {};
        
        Object.entries(rules).forEach(([fieldName, fieldRules]) => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (!field) return;
            
            // Group rules by trigger type
            const rulesByTrigger = {};
            fieldRules.forEach(rule => {
                if (!rulesByTrigger[rule.trigger]) {
                    rulesByTrigger[rule.trigger] = [];
                }
                rulesByTrigger[rule.trigger].push(rule);
            });
            
            // Setup event listeners for each trigger type
            Object.entries(rulesByTrigger).forEach(([trigger, triggerRules]) => {
                if (trigger === 'input') {
                    field.addEventListener('input', (event) => {
                        this.debouncedValidate(fieldName, triggerRules, event.target.value);
                    });
                } else if (trigger === 'blur') {
                    field.addEventListener('blur', (event) => {
                        this.validateField(fieldName, triggerRules, event.target.value);
                    });
                } else if (trigger === 'change') {
                    field.addEventListener('change', (event) => {
                        this.validateField(fieldName, triggerRules, event.target.value);
                    });
                }
            });
        });
    }
    
    /**
     * Debounced validation for input events
     */
    debouncedValidate(fieldName, rules, value) {
        // Clear existing timer
        if (this.debounceTimers.has(fieldName)) {
            clearTimeout(this.debounceTimers.get(fieldName));
        }
        
        // Set new timer
        const timer = setTimeout(() => {
            this.validateField(fieldName, rules, value);
            this.debounceTimers.delete(fieldName);
        }, this.config.debounceMs || 300);
        
        this.debounceTimers.set(fieldName, timer);
    }
    
    /**
     * Validate a single field against its rules
     */
    validateField(fieldName, rules, value) {
        const errors = [];
        
        rules.forEach(rule => {
            const error = this.validateRule(fieldName, rule, value);
            if (error) {
                errors.push(error);
            }
        });
        
        // Update validation state
        this.validationState.set(fieldName, {
            isValid: errors.length === 0,
            errors: errors
        });
        
        // Display validation results
        this.displayFieldValidation(fieldName, errors);
        
        return errors.length === 0;
    }
    
    /**
     * Validate a single rule
     */
    validateRule(fieldName, rule, value) {
        switch (rule.type) {
            case 'required':
                if (rule.value && (!value || value.trim() === '')) {
                    return { message: rule.message, severity: rule.severity };
                }
                break;
                
            case 'min_length':
                if (value && value.length < rule.value) {
                    return { message: rule.message, severity: rule.severity };
                }
                break;
                
            case 'max_length':
                if (value && value.length > rule.value) {
                    return { message: rule.message, severity: rule.severity };
                }
                break;
                
            case 'range':
                const numValue = parseFloat(value);
                if (!isNaN(numValue) && (numValue < rule.value[0] || numValue > rule.value[1])) {
                    return { message: rule.message, severity: rule.severity };
                }
                break;
                
            case 'format':
                if (rule.value === 'email' && value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(value)) {
                        return { message: rule.message, severity: rule.severity };
                    }
                }
                break;
        }
        
        return null;
    }
    
    /**
     * Display validation results for a field
     */
    displayFieldValidation(fieldName, errors) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        if (!field) return;
        
        // Clear existing validation display
        this.clearFieldValidation(fieldName);
        
        if (errors.length > 0) {
            // Show first error (most important)
            const error = errors[0];
            this.showFieldError(fieldName, error.message, error.severity);
        } else {
            // Field is valid - remove error styling
            this.showFieldValid(fieldName);
        }
    }
    
    /**
     * Clear validation display for a field
     */
    clearFieldValidation(fieldName) {
        // Use existing error handling function
        if (typeof clearValidationErrors === 'function') {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                clearValidationErrors(field.parentElement);
            }
        }
    }
    
    /**
     * Show error for a field
     */
    showFieldError(fieldName, message, severity = 'error') {
        // Use existing error display function
        if (typeof displayValidationError === 'function') {
            displayValidationError(fieldName, message);
        }
    }
    
    /**
     * Show field as valid
     */
    showFieldValid(fieldName) {
        const field = this.form.querySelector(`[name="${fieldName}"]`);
        if (!field) return;
        
        // Remove error styling
        field.classList.remove('border-red-300', 'focus:border-red-500', 'focus:ring-red-500');
        field.removeAttribute('data-invalid');
        field.removeAttribute('aria-invalid');
        
        // Add subtle valid styling (optional)
        if (field.value.trim()) {
            field.classList.add('border-green-300');
            setTimeout(() => {
                field.classList.remove('border-green-300');
            }, 2000);
        }
    }
    
    /**
     * Setup form-level validation
     */
    setupFormValidation() {
        this.form.addEventListener('submit', (event) => {
            if (!this.validateForm()) {
                event.preventDefault();
                this.focusFirstInvalidField();
            }
        });
    }
    
    /**
     * Validate entire form
     */
    validateForm() {
        let isValid = true;
        const rules = this.config.rules || {};
        
        Object.entries(rules).forEach(([fieldName, fieldRules]) => {
            const field = this.form.querySelector(`[name="${fieldName}"]`);
            if (!field) return;
            
            const fieldValid = this.validateField(fieldName, fieldRules, field.value);
            if (!fieldValid) {
                isValid = false;
            }
        });
        
        return isValid;
    }
    
    /**
     * Focus first invalid field
     */
    focusFirstInvalidField() {
        // Use existing function if available
        if (typeof focusInvalidField === 'function') {
            focusInvalidField();
        } else {
            // Fallback implementation
            const invalidField = this.form.querySelector('[data-invalid="true"]');
            if (invalidField) {
                invalidField.focus();
                invalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
    }
    
    /**
     * Get validation state for a field
     */
    getFieldValidationState(fieldName) {
        return this.validationState.get(fieldName) || { isValid: true, errors: [] };
    }
    
    /**
     * Get overall form validation state
     */
    getFormValidationState() {
        const states = Array.from(this.validationState.values());
        const isValid = states.every(state => state.isValid);
        const allErrors = states.flatMap(state => state.errors);
        
        return { isValid, errors: allErrors };
    }
    
    /**
     * Reset validation state
     */
    reset() {
        // Clear all validation state
        this.validationState.clear();
        
        // Clear all timers
        this.debounceTimers.forEach(timer => clearTimeout(timer));
        this.debounceTimers.clear();
        
        // Clear all validation displays
        Object.keys(this.config.rules || {}).forEach(fieldName => {
            this.clearFieldValidation(fieldName);
        });
        
        // Reset character counters
        this.characterCounters.forEach((counter, fieldName) => {
            const limitConfig = this.config.characterLimits[fieldName];
            if (limitConfig) {
                this.updateCharacterCounter(fieldName, '', limitConfig);
            }
        });
    }
}

// Global validation instances
window.validationEngines = window.validationEngines || new Map();

/**
 * Initialize validation for a form
 */
function initializeValidation(formSelector, config) {
    const form = document.querySelector(formSelector);
    if (!form) {
        console.warn(`Validation: Form not found: ${formSelector}`);
        return null;
    }
    
    const engine = new ValidationEngine(form, config);
    window.validationEngines.set(formSelector, engine);
    
    return engine;
}

/**
 * Get validation engine for a form
 */
function getValidationEngine(formSelector) {
    return window.validationEngines.get(formSelector);
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { ValidationEngine, initializeValidation, getValidationEngine };
}