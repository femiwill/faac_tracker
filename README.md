# Nigeria FAAC Allocation & Revenue Tracker

A web app where Nigerians can search for any state or local government and see how much federal allocation (FAAC) they received and how much internally generated revenue (IGR) they produced.

## Features

- **Search** for any of Nigeria's 36 states + FCT or 774 LGAs
- **State Detail** page with monthly FAAC allocations, IGR data, and charts
- **LGA Detail** page with allocation history
- **Compare** up to 3 states side by side with visual charts
- **Admin** panel to add new monthly allocation data
- Dark mode toggle

## Tech Stack

- Python / Flask / SQLAlchemy
- Bootstrap 5 / Chart.js
- SQLite database

## Setup

```bash
pip install -r requirements.txt
python seed_data.py   # Populate database with initial data
python app.py         # Run development server at http://localhost:5000
```

## Deployment

Configured for Railway deployment via `Procfile`.

## Data Sources

Seed data compiled from published FAAC reports, NBS (National Bureau of Statistics), BudgIT, and Ministry of Finance press releases.

---

Designed by **Place of Ideation**
