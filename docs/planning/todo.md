# Tasks Today

- [x] Implement locale-based date formatting with `Intl.DateTimeFormat()`
- [x] Add custom title override capability
- [x] Test format examples: "January 15, 2025" (US), "15. Januar 2025" (DE), "15 January 2025" (UK)
- [x] Review ADR: `docs/adr/decisions/0004-entry-title-auto-generation.md`

## 📋 New Executive Decisions (added 2025-07-20)

### **Decision A: Dashboard Recent Entries Limit**
- **Limit dashboard recent entries to 3 most recent entries only**
- **Rationale**: Cleaner dashboard focus, faster loading, encourages "All Entries" page usage
- **Implementation**: Modify dashboard query to `.limit(3)` and add "View all entries" link

### **Decision B: Minimal Card Design with Single Preview**
- **Problem**: Entry cards showing 3×3×255 chars = up to 2,295 characters per card (mobile disaster)
- **Card Design**: Title + Date/Score + Single preview line (60 chars from success_1)
- **Inspiration**: Apple Notes, Google Keep, Day One - focus on recognition not full content
- **Layout**: Title header, date+score+emoji, single preview line, edit button
- **Benefits**: Highly scannable, mobile-optimized, consistent card heights, quick emotional context
- **Implementation**: Redesign entry cards with 60-char truncation, smart word boundaries

### **Decision C: Navigation Pattern Simplification**
- **Remove Edit button** from entry cards (cluttered design)
- **Entire card clickable**: Full card area links to journal detail view (not just title)
- **Edit from detail view**: Edit button available in journal detail page  
- **Pattern**: Instagram, Apple Notes, Day One - entire card interaction
- **Benefits**: Large mobile touch targets, intuitive UX, no visual hints needed, accessibility-friendly
- **Implementation**: Make entire cards clickable with hover/active states, create journal detail view

## ✅ Implementation Progress (2025-07-20)

### **Completed Tasks**
- [x] **Backend: Limited dashboard to 3 recent entries** (`app/main.py:159`)
- [x] **Created journal detail view endpoint** (`/entries/{entry_id}/view` at `app/main.py:653`)
- [x] **Built entry_detail.html template** - Complete read-only view with edit button
- [x] **Redesigned dashboard entry cards** (`templates/dashboard.html:181-215`)
  - Minimal layout: Title + Date/Score + 60-char preview
  - Entire card clickable linking to detail view
  - Hover animations with shadow and translation
  - Removed edit buttons
- [x] **Redesigned entries page cards** (`templates/entries.html:133-154`)
  - Applied same minimal card design to All Entries page
  - Made entire cards clickable
  - Removed edit buttons from all entry cards
- [x] **Added "View all →" link** to dashboard Recent Entries section

### **Navigation Flow Implemented**
```
Dashboard/All Entries → Entry Card (click) → Detail View → Edit Button → Edit Form
```

### **Technical Implementation Details**
- **Card Design**: `bg-gradient-to-r from-blue-50 to-indigo-50 border-l-4 border-blue-400`
- **Preview Logic**: `{{ entry.success_1[:60] }}{% if entry.success_1|length > 60 %}...{% endif %}`
- **Hover States**: `hover:shadow-md hover:-translate-y-0.5 transition-all duration-200`
- **Touch Targets**: Entire card area with `cursor-pointer` and `block` link styling

## 🔧 Current Session Work (In Progress - 21:00)

### **Timestamp Display & Form Validation Fixes**
- [x] **Fixed timestamp display issue**: Added `was_edited` property to Entry model (`app/models.py:61-64`)
  - Issue: Property was only on `EntryRead` model, not main `Entry` table model
  - Solution: Added `@property def was_edited(self) -> bool` to Entry class
- [x] **Added timestamps to all card templates**: 
  - Dashboard cards (`templates/dashboard.html:199-208`)
  - Entries page cards (`templates/entries.html:151-160`)
  - Shows "Created: MM/DD/YYYY HH:MM AM/PM" and "Edited: MM/DD/YYYY HH:MM AM/PM" if modified
- [x] **Fixed empty field saving issue**: Updated form handling (`app/main.py:583-631`)
  - Issue: `Form(None)` parameters meant empty fields weren't processed
  - Solution: Changed to `Form("")` and updated logic to process all fields
  - Now properly saves empty strings for cleared fields
- [x] **Added `format_user_timestamp` to all templates**: Dashboard, entries, detail, edit pages
- [x] **Removed `required` attributes**: From edit form to allow clearing required fields
- [x] **Created server management utility**: `scripts/windows/utilities/kill-server.bat`
  - Unified script for terminating stubborn development servers
  - Handles zombie processes and network connections

### **Uncommitted Changes Status**
```
modified:   app/main.py                    - Form handling fixes, timestamp function access
modified:   app/models.py                  - Added was_edited property to Entry model  
modified:   templates/dashboard.html       - Added timestamps to cards
modified:   templates/edit_entry.html      - Removed required attrs, added timestamps
modified:   templates/entries.html         - Added timestamps to cards
modified:   templates/entry_detail.html    - Fixed timestamp parameter order
new file:   scripts/windows/utilities/kill-server.bat - Server management utility
```

### **Next Session Preparation**
- All timestamp and form validation issues resolved
- Card templates now consistent across dashboard and entries pages  
- Empty field clearing now works properly for all field types
- Ready for further feature development