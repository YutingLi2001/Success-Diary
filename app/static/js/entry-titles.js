/**
 * Entry Title Auto-Generation with User Locale
 * Implements ADR-0004: Entry Title Auto-Generation with User Locale
 */

/**
 * Format entry title based on user's browser locale
 * @param {Date} date - The date to format
 * @param {string} locale - Optional locale override (defaults to navigator.language)
 * @returns {string} Formatted date title
 */
const formatEntryTitle = (date, locale = navigator.language) => {
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'long', 
    day: 'numeric'
  }).format(date);
};

/**
 * Safe entry title formatting with fallback
 * @param {Date} date - The date to format
 * @returns {string} Formatted date title with fallback to US English
 */
const safeFormatEntryTitle = (date) => {
  try {
    return formatEntryTitle(date);
  } catch (error) {
    console.warn('Locale detection failed, falling back to US format:', error);
    // Fallback to US format
    return formatEntryTitle(date, 'en-US');
  }
};

/**
 * Generate auto title for entry date
 * @param {Date|string} entryDate - Entry date (Date object or ISO string)
 * @returns {string} Auto-generated title
 */
const generateAutoTitle = (entryDate) => {
  const date = entryDate instanceof Date ? entryDate : new Date(entryDate);
  return safeFormatEntryTitle(date);
};

/**
 * Initialize title field with auto-generation
 * Sets up title field behavior on page load
 */
const initializeTitleField = () => {
  const titleInput = document.getElementById('title');
  if (titleInput && !titleInput.value.trim()) {
    // Auto-generate title for today's date
    const today = new Date();
    titleInput.value = generateAutoTitle(today);
    titleInput.placeholder = 'Enter custom title or keep auto-generated';
  }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', initializeTitleField);

// Export functions for testing and external use
window.EntryTitles = {
  formatEntryTitle,
  safeFormatEntryTitle,
  generateAutoTitle,
  initializeTitleField
};