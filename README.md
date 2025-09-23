# Training Feedback Survey App

A Streamlit app for collecting and analyzing training feedback across DMV courses with standardized skill questions (including **“All of the above → ranking”**), CSV/Excel persistence, and a results dashboard.

---

## Features
- AI Avatar Intro (HeyGen video)
- Demographics + training sections
- Standardized skill questions with **“All of the above → ranking”**
- Rating sliders (5 = best, 1 = worst)
- Onboarding & Research/AI feedback questions
- Optional preview before submit and submission animation
- **CSV and Excel** persistence on submit
- Results dashboard (filters, bar charts, table view, CSV export)
- Email automation hooks
- QR code integration

---

## Project Structure

├─ intro.py # Intro video + instructions
├─ Home.py # Main survey app (CSV/Excel persistence)
├─ Results.py # Results dashboard (reads survey_data.csv)
├─ utils.py # Excel export + email helpers
├─ requirements.txt # Python dependencies
├─ README.md # This file
└─ assets/ # (optional) videos, logos, QR images

---

## Requirements
- Python 3.9+ recommended
- Packages (in `requirements.txt`):
  - `streamlit`
  - `pandas`
  - `matplotlib`
  - `openpyxl`
  - `altair`

## Run Locally

# 1) Create & activate a virtual environment (recommended)
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the app
streamlit run Home.py
# (optional) in a second terminal:
# streamlit run Results.py
# Once you submit a response, a survey_data.csv file will be created/updated. The Excel file survey_results.xlsx will also append a new row per submission.
# Data Persistence

# CSV: Appends each submission to survey_data.csv (created automatically).
# Excel: Appends each submission to survey_results.xlsx (sheet: responses), via utils.# export_to_excel(...).
# Both are triggered on Submit in Home.py.