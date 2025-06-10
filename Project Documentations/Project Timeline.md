# Development Timeline (10 Weeks)

| Week | Dates (2025)    | Primary Objective  | Key Deliverables                                                                                   |
| ---- | --------------- | ------------------ | -------------------------------------------------------------------------------------------------- |
|  1   | Jun 9 – Jun 15  | Foundation         | Project scaffold (Next.js, Tailwind); docs committed; CI lint/format setup; Clerk auth live in dev |
|  2   | Jun 16 – Jun 22 | Data Model & DB    | Prisma schema (`User`, `Entry`); local migrations; connect to Supabase PG; seed script             |
|  3   | Jun 23 – Jun 29 | Daily Entry MVP    | `entry.create` tRPC route; Zod validation; Journal form UI                                         |
|  4   | Jun 30 – Jul 6  | History & Edit     | `entry.list`, `entry.update`; Calendar/date navigation; basic responsive polish                    |
|  5   | Jul 7 – Jul 13  | Highlight Modal    | Algorithm to pick past positive entry; modal component; unit tests                                 |
|  6   | Jul 14 – Jul 20 | Import / Export    | JSON export + import; CSV export helper; file‑size guard                                           |
|  7   | Jul 21 – Jul 27 | UI Hardening       | Dark/light theme toggle; mobile viewport QA; accessibility pass                                    |
|  8   | Jul 28 – Aug 3  | Pre‑launch QA      | End‑to‑end tests (Playwright); error logging with Sentry; staging env on Vercel                    |
|  9   | Aug 4 – Aug 10  | Dog‑food & Bug‑fix | Founder daily use; fix blockers; prepare launch docs, screenshots                                  |
|  10  | Aug 11 – Aug 17 | **v1.0 Launch**    | Deploy production DB; public README & marketing post; open source repo; tag v1.0                   |

---