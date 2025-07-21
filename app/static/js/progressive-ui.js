/**
 * Progressive UI System for Success-Diary
 * Implements progressive field display and character counting
 */

class ProgressiveUI {
    constructor() {
        this.debounceTimers = new Map();
        this.DEBOUNCE_DELAY = 300;
        this.MIN_TRIGGER_LENGTH = 2;
        
        // Character limits from spec
        this.LIMITS = {
            emotion_fields: 255, // Three emotion points fields
            journal: 8000,       // Daily journal field
            title: 100           // Entry title field
        };
        
        // Threshold percentages
        this.THRESHOLDS = {
            show_counter: 0.85,  // 85% threshold to show counter
            warning: 0.95,       // 95% threshold for amber warning
            error: 1.0           // 100% threshold for red error
        };
        
        this.init();
    }
    
    init() {
        this.setupProgressiveFields();
        this.setupCharacterLimits();
    }
    
    /**
     * Setup progressive field display - shows subsequent fields after 2+ characters
     */
    setupProgressiveFields() {
        // Success fields progressive display
        this.setupFieldGroup('success', ['success_1', 'success_2', 'success_3']);
        
        // Gratitude fields progressive display  
        this.setupFieldGroup('gratitude', ['gratitude_1', 'gratitude_2', 'gratitude_3']);
        
        // Anxiety fields progressive display
        this.setupFieldGroup('anxiety', ['anxiety_1', 'anxiety_2', 'anxiety_3']);
    }
    
    setupFieldGroup(groupName, fieldNames) {
        if (!fieldNames || fieldNames.length < 2) return;
        
        // Initially evaluate which fields should be visible based on content
        this.evaluateInitialFieldVisibility(fieldNames);
        
        // Setup triggers for each field in sequence
        fieldNames.forEach((fieldName, index) => {
            const field = document.querySelector(`input[name="${fieldName}"]`);
            if (!field) return;
            
            field.addEventListener('input', (e) => {
                this.debounce(`${groupName}_${fieldName}_trigger`, () => {
                    this.handleSequentialTrigger(fieldNames, index);
                });
            });
        });
    }
    
    evaluateInitialFieldVisibility(fieldNames) {
        // Show fields sequentially based on content
        for (let i = 0; i < fieldNames.length; i++) {
            const field = document.querySelector(`input[name="${fieldNames[i]}"]`);
            if (!field) continue;
            
            const container = field.closest('.form-field');
            if (!container) continue;
            
            if (i === 0) {
                // First field is always visible
                container.style.display = 'block';
            } else {
                // Check if previous field has content
                const prevField = document.querySelector(`input[name="${fieldNames[i-1]}"]`);
                const hasPreviousContent = prevField && prevField.value.trim().length >= this.MIN_TRIGGER_LENGTH;
                
                if (hasPreviousContent || field.value.trim()) {
                    // Show this field if previous has content OR this field has content
                    container.style.display = 'block';
                } else {
                    // Hide this field and all subsequent fields
                    for (let j = i; j < fieldNames.length; j++) {
                        const subsequentField = document.querySelector(`input[name="${fieldNames[j]}"]`);
                        if (subsequentField) {
                            const subsequentContainer = subsequentField.closest('.form-field');
                            if (subsequentContainer) {
                                subsequentContainer.style.display = 'none';
                            }
                        }
                    }
                    break;
                }
            }
        }
    }
    
    handleSequentialTrigger(fieldNames, changedFieldIndex) {
        // Check each field in sequence and show/hide the next one accordingly
        for (let i = changedFieldIndex; i < fieldNames.length - 1; i++) {
            const currentField = document.querySelector(`input[name="${fieldNames[i]}"]`);
            const nextField = document.querySelector(`input[name="${fieldNames[i + 1]}"]`);
            
            if (!currentField || !nextField) continue;
            
            const currentContent = currentField.value.trim();
            const shouldShowNext = currentContent.length >= this.MIN_TRIGGER_LENGTH;
            const nextContainer = nextField.closest('.form-field');
            
            if (!nextContainer) continue;
            
            if (shouldShowNext) {
                // Show the next field if current field has enough content
                if (nextContainer.style.display === 'none') {
                    this.showFieldWithAnimation(nextContainer);
                }
            } else {
                // Hide the next field and all subsequent fields if current field doesn't have enough content
                this.hideFieldsFromIndex(fieldNames, i + 1);
                break; // Stop checking further fields
            }
        }
    }
    
    showFieldWithAnimation(container) {
        container.style.display = 'block';
        container.style.opacity = '0';
        container.style.transform = 'translateY(-10px)';
        setTimeout(() => {
            container.style.transition = 'all 0.3s ease';
            container.style.opacity = '1';
            container.style.transform = 'translateY(0)';
        }, 10);
    }
    
    hideFieldsFromIndex(fieldNames, startIndex) {
        for (let i = startIndex; i < fieldNames.length; i++) {
            const field = document.querySelector(`input[name="${fieldNames[i]}"]`);
            if (field) {
                const container = field.closest('.form-field');
                if (container) {
                    container.style.display = 'none';
                    // Don't clear field values - preserve user input
                }
            }
        }
    }
    
    /**
     * Setup character limits and counters
     */
    setupCharacterLimits() {
        // Three emotion points fields (255 chars each)
        ['success_1', 'success_2', 'success_3', 
         'gratitude_1', 'gratitude_2', 'gratitude_3',
         'anxiety_1', 'anxiety_2', 'anxiety_3'].forEach(fieldName => {
            this.setupCharacterCounter(fieldName, this.LIMITS.emotion_fields);
        });
        
        // Daily journal field (8,000 chars)
        this.setupCharacterCounter('journal', this.LIMITS.journal);
        
        // Entry title field (100 chars)
        this.setupCharacterCounter('title', this.LIMITS.title);
    }
    
    setupCharacterCounter(fieldName, maxLength) {
        const field = document.querySelector(`[name="${fieldName}"]`);
        if (!field) return;
        
        const container = field.closest('.form-field') || field.parentElement;
        
        // Create counter element
        const counter = document.createElement('div');
        counter.className = 'character-counter';
        counter.style.display = 'none'; // Initially hidden
        container.appendChild(counter);
        
        // Setup input listener
        field.addEventListener('input', (e) => {
            this.debounce(`${fieldName}_counter`, () => {
                this.updateCharacterCounter(e.target, counter, maxLength);
            });
        });
        
        // Prevent typing beyond limit
        field.addEventListener('keydown', (e) => {
            const currentLength = e.target.value.length;
            
            // Allow: backspace, delete, tab, escape, enter, arrow keys
            if ([8, 9, 27, 13, 37, 38, 39, 40, 46].includes(e.keyCode) ||
                // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+Z
                (e.ctrlKey === true && [65, 67, 86, 88, 90].includes(e.keyCode))) {
                return;
            }
            
            // Prevent typing if at limit
            if (currentLength >= maxLength) {
                e.preventDefault();
            }
        });
    }
    
    updateCharacterCounter(field, counter, maxLength) {
        const currentLength = field.value.length;
        const percentage = currentLength / maxLength;
        
        // Only show counter at 85% threshold
        if (percentage < this.THRESHOLDS.show_counter) {
            counter.style.display = 'none';
            return;
        }
        
        counter.style.display = 'flex';
        
        // Determine counter style based on thresholds
        let className = 'character-counter';
        if (percentage >= this.THRESHOLDS.error) {
            className += ' counter-error';
        } else if (percentage >= this.THRESHOLDS.warning) {
            className += ' counter-warning';
        } else {
            className += ' counter-info';
        }
        
        counter.className = className;
        
        // Format numbers with commas for large counts
        const formattedCurrent = this.formatNumber(currentLength);
        const formattedMax = this.formatNumber(maxLength);
        const remaining = maxLength - currentLength;
        const formattedRemaining = this.formatNumber(remaining);
        
        // Build counter content
        let content = `<span class="count">${formattedCurrent}</span>`;
        content += `<span class="separator">/</span>`;
        content += `<span class="limit">${formattedMax}</span>`;
        
        // Show remaining count at warning threshold
        if (percentage >= this.THRESHOLDS.warning) {
            content += ` <span class="remaining">(${formattedRemaining} remaining)</span>`;
        }
        
        counter.innerHTML = content;
        
        // Update field styling based on limit proximity
        this.updateFieldStyling(field, percentage);
    }
    
    updateFieldStyling(field, percentage) {
        // Remove existing limit classes
        field.classList.remove('approaching-limit', 'near-limit', 'at-limit');
        
        // Add appropriate class based on percentage
        if (percentage >= this.THRESHOLDS.error) {
            field.classList.add('at-limit');
        } else if (percentage >= this.THRESHOLDS.warning) {
            field.classList.add('near-limit');
        } else if (percentage >= this.THRESHOLDS.show_counter) {
            field.classList.add('approaching-limit');
        }
    }
    
    formatNumber(num) {
        return num.toLocaleString();
    }
    
    debounce(key, func) {
        if (this.debounceTimers.has(key)) {
            clearTimeout(this.debounceTimers.get(key));
        }
        
        const timer = setTimeout(() => {
            func();
            this.debounceTimers.delete(key);
        }, this.DEBOUNCE_DELAY);
        
        this.debounceTimers.set(key, timer);
    }
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ProgressiveUI();
    });
} else {
    new ProgressiveUI();
}