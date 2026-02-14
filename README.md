# Behavior Intelligence Dashboard

## Overview
The Behavior Intelligence Dashboard is a real-time monitoring system that detects risky behavior based on user events. High-risk activity are automatically flagged and displayed on a live dashboard for human review.

## Features
- Real-time event ingestion via FastAPI backend
- Risk detection (HIGH / LOW) based on event content
- Active alert system for high-risk behavior
- Live event feed with timestamps, actor, and type
- Interactive charts: Events over time, Risk distribution, Actor activity
- Login-protected dashboard (Admin & Analyst roles)
- Fully deployable online

## Installation (Local Setup)
1. Clone the repository:
```bash
git clone https://github.com/LINCOLN/behavior-dashboard.git