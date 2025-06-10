# SuccessDiary – Success Metrics & Development Timeline

## 1. Release Target

* **Version:** v1.0
* **Release window:** 17 Aug 2025 (10 weeks from project start on 9 Jun 2025)

---

## 2. Key Performance Indicators (KPI)

| # | Metric          | Definition                                                                          | Success Threshold                           | Measurement Method                                                          |
| - | --------------- | ----------------------------------------------------------------------------------- | ------------------------------------------- | --------------------------------------------------------------------------- |
| 1 | Active Users    | Number of distinct accounts that create ≥1 entry                                    | **> 10 users** by 4 weeks post‑launch       | Supabase SQL: `COUNT(DISTINCT user_id)` where `entries.count > 0`           |
| 2 | User Stickiness | Average number of days each active user submits an entry within their first 45 days | **> 30 days**                               | Daily cron job aggregates `entries` per user, exports to Redash for average |
| 3 | Stability       | Production error rate (uncaught exceptions logged per 1 000 requests)               | **< 1 %**                                   | Vercel + Sentry monitoring                                                  |
| 4 | Self‑adoption   | Consecutive days the founder (you) uses the app                                     | **≥ 50 days** (covers full dog‑food period) | Internal query on `entries` table                                           |

*Note – KPI 1 & 2 are “ship‑decision” metrics. KPI 3 & 4 are quality gates.*

---

## 3. Post‑launch Checklist

1. Monitor KPI dashboards daily for first 2 weeks.
2. Collect qualitative feedback from initial users.
3. Decide on **Should** feature prioritisation for v1.1 based on usage patterns.

---

*Last updated: 10 Jun 2025*
