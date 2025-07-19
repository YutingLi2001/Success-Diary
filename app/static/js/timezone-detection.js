/**
 * Timezone Detection System
 * 
 * Implements automatic browser timezone detection with priority chain:
 * Manual setting → Auto-detection → UTC fallback
 * 
 * Based on ADR-0005: User Timezone Handling Strategy
 */

class TimezoneManager {
    constructor() {
        this.detectedTimezone = null;
        this.effectiveTimezone = null;
        this.userPreference = null;
        this.autoDetectEnabled = true;
    }

    /**
     * Detect browser timezone using Intl API
     * @returns {string} Detected timezone (e.g., 'America/New_York')
     */
    detectBrowserTimezone() {
        try {
            this.detectedTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
            console.log(`Browser timezone detected: ${this.detectedTimezone}`);
            return this.detectedTimezone;
        } catch (error) {
            console.warn('Failed to detect browser timezone:', error);
            this.detectedTimezone = 'UTC';
            return 'UTC';
        }
    }

    /**
     * Get effective timezone based on priority chain
     * @param {string|null} userPreference - Manual timezone preference
     * @param {boolean} autoDetectEnabled - Whether auto-detection is enabled
     * @returns {string} Effective timezone to use
     */
    getEffectiveTimezone(userPreference = null, autoDetectEnabled = true) {
        // Priority chain: Manual → Auto-detection → UTC fallback
        if (userPreference) {
            this.effectiveTimezone = userPreference;
            console.log(`Using manual timezone preference: ${userPreference}`);
            return userPreference;
        }

        if (autoDetectEnabled && this.detectedTimezone) {
            this.effectiveTimezone = this.detectedTimezone;
            console.log(`Using auto-detected timezone: ${this.detectedTimezone}`);
            return this.detectedTimezone;
        }

        // Fallback to UTC
        this.effectiveTimezone = 'UTC';
        console.log('Using UTC fallback timezone');
        return 'UTC';
    }

    /**
     * Send timezone data to backend
     * @param {string} timezone - Effective timezone
     * @param {string} detected - Detected timezone (for caching)
     * @returns {Promise<boolean>} Success status
     */
    async saveTimezone(timezone, detected) {
        try {
            const response = await fetch('/api/user/timezone', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    timezone: timezone,
                    detected: detected,
                    timestamp: new Date().toISOString()
                })
            });

            if (response.ok) {
                console.log('Timezone saved successfully');
                return true;
            } else {
                console.warn('Failed to save timezone:', response.status);
                return false;
            }
        } catch (error) {
            console.error('Error saving timezone:', error);
            return false;
        }
    }

    /**
     * Initialize timezone detection and handling
     * Called on page load for authenticated users
     * @param {Object} userSettings - Current user timezone settings
     */
    async initialize(userSettings = {}) {
        console.log('Initializing timezone detection...');

        // Extract user settings
        this.userPreference = userSettings.user_timezone || null;
        this.autoDetectEnabled = userSettings.timezone_auto_detect !== false;

        // Always detect browser timezone for comparison/caching
        this.detectBrowserTimezone();

        // Determine effective timezone
        const effectiveTimezone = this.getEffectiveTimezone(
            this.userPreference, 
            this.autoDetectEnabled
        );

        // Save to backend if auto-detection is enabled
        if (this.autoDetectEnabled) {
            await this.saveTimezone(effectiveTimezone, this.detectedTimezone);
        }

        // Store in sessionStorage for client-side use
        sessionStorage.setItem('effectiveTimezone', effectiveTimezone);
        sessionStorage.setItem('detectedTimezone', this.detectedTimezone);

        return effectiveTimezone;
    }

    /**
     * Get current effective timezone from session or detect
     * @returns {string} Current timezone
     */
    getCurrentTimezone() {
        const stored = sessionStorage.getItem('effectiveTimezone');
        if (stored) {
            return stored;
        }

        // Fallback: detect and use immediately
        this.detectBrowserTimezone();
        return this.detectedTimezone || 'UTC';
    }

    /**
     * Update user timezone preference
     * @param {string|null} newTimezone - New manual preference (null to clear)
     * @param {boolean} enableAutoDetect - Whether to enable auto-detection
     */
    async updatePreference(newTimezone, enableAutoDetect = true) {
        this.userPreference = newTimezone;
        this.autoDetectEnabled = enableAutoDetect;

        // Recalculate effective timezone
        const effectiveTimezone = this.getEffectiveTimezone(
            this.userPreference, 
            this.autoDetectEnabled
        );

        // Save to backend
        await this.saveTimezone(effectiveTimezone, this.detectedTimezone);

        // Update session storage
        sessionStorage.setItem('effectiveTimezone', effectiveTimezone);

        console.log(`Timezone preference updated: ${newTimezone || 'auto-detect'}`);
        return effectiveTimezone;
    }
}

// Global timezone manager instance
window.timezoneManager = new TimezoneManager();

// Auto-initialize on DOM ready for authenticated users
document.addEventListener('DOMContentLoaded', () => {
    // Check if user is authenticated (look for user data)
    const userElement = document.querySelector('#user-timezone-data');
    
    if (userElement) {
        // Extract user timezone settings from data attributes
        const userSettings = {
            user_timezone: userElement.dataset.userTimezone || null,
            timezone_auto_detect: userElement.dataset.timezoneAutoDetect !== 'false',
            last_detected_timezone: userElement.dataset.lastDetectedTimezone || null
        };

        // Initialize timezone handling
        window.timezoneManager.initialize(userSettings)
            .then(timezone => {
                console.log(`Timezone system initialized with: ${timezone}`);
                
                // Dispatch custom event for other components
                document.dispatchEvent(new CustomEvent('timezoneReady', {
                    detail: { timezone }
                }));
            })
            .catch(error => {
                console.error('Timezone initialization failed:', error);
            });
    }
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TimezoneManager;
}