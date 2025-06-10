# MVP Scope – SuccessDiary

**SuccessDiary** is designed to support individuals in documenting their growth in a structured, data-driven way. Through personalized daily reflection and meaningful feedback from past achievements, the system encourages habit continuity and long-term behavioral change. The following outlines the MVP scope, categorized by the MoSCoW prioritization model.

---

## Must (Essential for Initial Launch)

| Feature                                | Description                                                                                                                                                |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **User Registration / Login / Logout** | Basic authentication system supporting email/password and OAuth (e.g., GitHub or Google). All user data is securely isolated.                              |
| **Daily Entry**                        | Users complete a structured entry each day including:<br>- 3 success highlights<br>- 3 gratitude points<br>- 3 sources of anxiety<br>- A self-rating (1–5) |
| **Edit Historical Entries**            | Users can view and revise entries from any date, enabling reflection and continuity.                                                                       |
| **Data Import / Export**               | Full export of user data (JSON/CSV), and support for importing past backups to ensure data ownership.                                                      |
| **Daily Highlight Prompt**             | On login, the system displays a motivational entry from the user's past to reinforce self-belief and resilience.                                           |
| **Foundational UI Framework**          | Responsive layout with clean navigation, optimized for both desktop and mobile devices. Optional support for light/dark themes.                            |

---

## Should (Important for Enhanced Experience)

| Feature                           | Description                                                                                                                                                           |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Onboarding Flow**               | Guides new users through initial setup: defining goals, selecting fields, and completing their first entry.                                                           |
| **Data Visualization**            | Provides line, bar, and pie charts to help users visualize trends in mood, routines, productivity, and more.                                                          |
| **Custom Field Management**       | Users can add, modify, or remove personalized fields (e.g., weight, meals, focus time), with support for various input types (text, number, boolean, currency, etc.). |
| **Tagging System**                | Users can tag entries (e.g., “low energy”, “productive”, “exercise”) for easier filtering and pattern recognition.                                                    |
| **Weekly / Monthly Summary View** | Aggregated views to help users reflect on progress and trends across defined periods. Useful for habit review and emotional insight.                                  |

---

## Could (Optional but Valuable Add-ons)

| Feature                                                | Description                                                                                                                      |
| ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **AI-Powered Insights**                                | Uses models such as OpenAI to summarize weekly or monthly records, offering gentle suggestions and personal reflections.         |
| **Entry Templates / Guided Prompts**                   | Provides users with structured reflection prompts (e.g., “What went well today?”) to reduce friction and improve expressiveness. |
| **Streak Counter**                                     | Displays consecutive days of journaling or habit completion to motivate consistency through gamified progress tracking.          |
| **PWA Support / Desktop Installation / Notifications** | Enables Progressive Web App installation and optional push notifications to remind users to check in daily.                      |
| **Multi-Device Sync**                                  | Syncs data across devices using cloud storage. Real-time native sync may be explored in later stages.                            |

---
