SuccessDiary - Core Functionality Overview

## Product Description
SuccessDiary is a lightweight daily logging application designed for personal growth tracking through structured emotional reflection. The core focus is building daily habits of positive reflection and emotional awareness.

## Development Roadmap

This document organizes features by development phases to ensure focused delivery of core value before expanding functionality.

---

# 🚀 MVP (Version 1.0) - Essential Features

**Goal**: Prove core concept of daily emotional reflection and establish user habits.

## 1. Daily Journal Entry System

### 1.1 Entry Rules
- Each calendar day allows exactly ONE journal entry (based on user's time zone)
- Users can edit existing entries, but saving overwrites the previous version
- System automatically records submission timestamp
- Deletion of journal entries are hard-deletes and should warn user and ask for confirmation
- Date-based system: entries are organized by calendar date

### 1.2 Entry Title
- Users can provide a custom title for each day's entry
- Title length must be limited (under 30 characters)
- If no title is provided, system generates default: "January 15, 2025" (formatted as current date)

### 1.3 Three Emotion Points (Core Feature)
**This is the key differentiator and main value proposition**

- **Highlights**: Record 1-3 brief sentences about daily achievements (minimum 1 required)
- **Gratitude**: Record 1-3 brief sentences about things to be grateful for (minimum 1 required)
- **Anxiety**: Record 0-3 brief sentences about worries or concerns (optional, can be empty)
- Maximum 3 items per category, no more allowed
- UI behavior: Show only one input line initially, display next line only after current line has content (minimize scrolling)

### 1.4 Daily Free-form Journal
- One text field for free writing about the day
- Completely optional - users can leave blank with no minimum character requirement
- Suggested maximum around 4000 characters

## 2. Overall Daily Rating
- Located at the very end of each journal entry
- Users rate their overall day: Integer scale 1-5 or "-" (user must provide input in order to save the entry)
- This field is ALWAYS enabled (cannot be disabled)
- Will be used for future trend charts/visualizations

## 3. Basic History & Viewing
- List shows: Entry date, title, and overall rating
- Click entry to be redirected to the entry page to view full content
- All historical entries remain editable; when saved, today's entry will also appear in historical entries and remain editable
- Chronological organization by date

## 4. Essential User Experience
### 4.1 Saving & Feedback
- Auto-save drafts to prevent data loss
- Display gentle confirmation: "Today's journal has been saved" after saving

### 4.2 Form Validation
- Basic form validation for required fields
- Display friendly error messages
- Frontend validation before backend submission

### 4.3 Dynamic UI
- Show only one emotion point input line initially
- Display next line only after current line has content (minimize scrolling)

---

# 📈 Version 2.0 - Health & Wellness Expansion

**Goal**: Add optional health tracking for users who want more comprehensive logging.

## 1. Health Tracking Module
### 1.1 Module Settings
- Entire health section can be enabled/disabled in user settings
- When disabled, forms hide immediately from current day's entry
- Historical data remains preserved and appears in exports
- Sub-modules can be individually toggled on/off

### 1.2 Diet Tracking
Offers two modes (Light Mode is default):

**Light Mode (Default):**
- Overall eating satisfaction: 1-5 scale (1 = very poor, 5 = excellent)
- Optional notes: Text field for additional details about eating patterns

**Standard Mode (Advanced):**
- Calories: Integer input, unit: kcal
- Protein: One decimal place, unit: g
- Carbohydrates: One decimal place, unit: g
- Fat: One decimal place, unit: g
- Users can switch between modes at any time in settings

### 1.3 Exercise Tracking
- Initial question: "Did you work out?" (Yes/No toggle)
- If "No" selected: 
  - Show Physical Activity Level: 1-5 scale (1 = sedentary, 5 = very active)
  - Skip structured workout fields
- If "Yes" selected, show:
  - Exercise Type: Dropdown with presets ("Cardio"/"Strength Training") plus custom text input option
  - Duration: Integer minutes
  - Subjective Feeling: 1-5 scale (1 = terrible, 5 = excellent)

### 1.4 Sleep Tracking
- Sleep Duration: One decimal place, unit: hours
- Sleep Quality: 1-5 scale (user self-assessment)
- Notes: Optional text field

## 2. Productivity Module
- Focus Time: Integer minutes - total deep work time for the day
- Focus Quality: 1-5 scale - quality assessment of focus sessions

## 3. Enhanced UX Features
### 3.1 Form Display
- Page loads with sections collapsed by default
- Only enabled modules auto-expand
- All other sections remain collapsed to reduce scrolling

### 3.2 Quick Fill Features
- "Copy from Yesterday" function: Quickly copies previous day's quantitative data
- Common values can be set as defaults

### 3.3 Advanced Validation
- All numeric fields show acceptable ranges
- Out-of-range or incorrect format triggers red border highlight
- Range validation for health metrics

---

# 🔧 Version 3.0+ - Advanced Customization

**Goal**: Power user features and extensive customization options.

## 1. Custom Fields System (Settings Page)
Note: All custom field management happens in a separate settings page, not in the daily entry interface.

### 1.1 Groups (Major Categories)
- Users can create new groups
- Groups can be renamed or deleted
- Deleting a group hides all its sub-items from daily forms

### 1.2 Sub-items (Fields within Groups)
Field types available:
- Numeric (can set unit and min/max limits)
- Short text
- 1-5 star rating
- Fields ordered by creation time
- Order can be adjusted by drag-and-drop in settings

### 1.3 Data Persistence
- Adding/removing fields takes effect immediately
- Historical data never lost when fields are removed
- Removed fields still visible in historical records unless manually deleted there

## 2. Advanced Analytics
- Trend charts and visualizations
- Pattern recognition
- Export functionality

## 3. Integration Features
- API access
- Third-party app integrations
- Backup and sync options

---

# Summary

**MVP Focus**: Core emotional reflection through structured daily journaling. Prove the concept and build user habits.

**V2 Focus**: Optional health and productivity tracking for users wanting comprehensive logging.

**V3+ Focus**: Power user features, customization, and advanced analytics.

This phased approach ensures we deliver core value first, then expand based on user feedback and adoption.