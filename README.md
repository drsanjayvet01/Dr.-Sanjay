# 🐾 Livestock Development & Registration Dashboard

A Streamlit-based web application for managing and tracking livestock records with analytics and database management capabilities.

## Features

### 📊 Tab 1: Analytics Dashboard
- View livestock statistics and visualizations
- Filter records by village and species
- Display KPI metrics (total records, unique owners, villages monitored)
- Interactive histogram showing livestock distribution
- Filterable registry ledger view

### ➕ Tab 2: Register New Entry
- Add new livestock records with comprehensive form
- Collect animal details (species, breed, sex, status, pregnancy, milking)
- Capture owner information (name, Aadhaar, village, mobile)
- Built-in validation for mandatory fields
- Duplicate prevention
- Auto-save to CSV database

### 🗑️ Tab 3: Manage & Remove Records
- Search and delete livestock records by Tag ID
- Preview before deletion
- Confirmation required before permanent removal
- Immediate database updates

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Database Format

The application uses a CSV file (`consolidated_livestock_data.csv`) with the following columns:
- Tag ID (Unique Identifier)
- Tagging Date
- Species (Cattle, Buffalo, Goat, Sheep, Other)
- Breed
- Animal Sex
- Animal Status
- Pregnancy Status
- Milking Status
- Owner Name
- Aadhaar No.
- Owner Village
- Owner Mobile No
- Other Details

## Data Safety

- Tag IDs are normalized to handle numeric strings
- Dynamic column injection for new tracking fields
- Validation prevents duplicate entries
- Confirmation dialogs for destructive operations
- All changes immediately persisted to disk

## Requirements

- Python 3.8+
- Streamlit 1.28.1+
- Pandas 2.0.3+
- Plotly 5.17.0+

## Usage

1. Place your `consolidated_livestock_data.csv` file in the application directory
2. Run the app with `streamlit run app.py`
3. Use the three tabs to view analytics, add records, or manage existing entries

## License

MIT License
