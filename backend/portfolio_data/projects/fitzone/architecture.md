---
title: FITZONE Architecture & Challenges
category: project
tech: Next.js, React, TypeScript, Tailwind CSS
---

# FITZONE Technical Architecture & Engineering Challenges

## System Architecture
FITZONE is built on a serverless frontend-centric architecture:
- **Frontend**: Next.js and React for dynamic, component-driven UI.
- **Styling**: Tailwind CSS for responsive grid layouts.
- **Hosting**: Vercel for fast caching and continuous integration.

## Key Challenges & Solutions
1. **Membership Lifecycle Modeling**:
   - *Challenge*: Designing a data model to handle rolling membership expirations, grace periods, and partial payments.
   - *Solution*: Developed a custom date-calculation algorithm in TypeScript that handles membership statuses dynamically (e.g. Active, Pending, Expired, Suspended) based on payment logs.
2. **Network Constraints**:
   - *Challenge*: Gym owners often have weak cellular connections inside basements or concrete buildings.
   - *Solution*: Kept assets lightweight, stripped unnecessary dependencies, and used Client-Side Storage where possible to cache static records, ensuring smooth mobile operation.
