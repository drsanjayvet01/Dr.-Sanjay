# Livestock Registry Application - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│              User Interface (Streamlit)             │
│  ┌──────────┬──────────┬──────────┬──────────────┐  │
│  │Dashboard │Add Entry │Search    │ Analytics    │  │
│  │          │& Edit    │Management│& Settings    │  │
│  └──────────┴──────────┴──────────┴──────────────┘  │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│          Data Processing & Validation               │
│  ┌──────────────────────────────────────────────┐  │
│  │  Data Loader  │  Validation  │  Backup Mgmt  │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│          Storage & Persistence                      │
│  ┌──────────────────────────────────────────────┐  │
│  │  CSV Database  │  Backups Directory           │  │
│  │  (Primary)     │  (Timestamped)              │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## Component Overview

### 1. Frontend Layer (Streamlit)
- **Pages/Tabs**:
  - Dashboard (Analytics & Reports)
  - Add Entry (Data Input Form)
  - Search & Edit (Record Management)
  - Analytics (Advanced Visualizations)
  - Management (Database & Backups)
  - Settings (Configuration)

### 2. Business Logic Layer
- **Data Loading**: `load_data()` - Loads and validates CSV
- **Data Validation**: Checks for mandatory fields, duplicates
- **Backup Management**: Auto-backup creation and restoration
- **Search & Filter**: Multi-criteria search functionality

### 3. Data Layer
- **CSV Database**: `consolidated_livestock_data.csv`
  - Primary data storage
  - Row-based structure
  - Easy to understand and backup
- **Backup System**: `backups/` directory
  - Timestamped backups
  - Quick restore capability

## Data Model

### Livestock Record Structure
```python
{
    'Tag ID': str,                    # Unique identifier
    'Tagging Date': date,             # Registration date
    'Species': str,                   # Cattle, Buffalo, Goat, Sheep, Other
    'Breed': str,                     # Animal breed
    'Animal Sex': str,                # Female/Male
    'Animal Status': str,             # Active, Inactive, Died
    'Pregnancy Status': str,          # Y, N, NA
    'Milking Status': str,            # In Milk, Dry, NA
    'Owner Name': str,                # Owner's full name
    'Aadhaar No.': str,              # 12-digit Aadhaar number
    'Owner Village': str,             # Village name
    'Owner Mobile No': str,           # Contact number
    'Health Status': str,             # Healthy, Sick, Under Treatment
    'Vaccination Date': date,         # Last vaccination
    'Last Check Date': date,          # Last health checkup
    'Other Details': str              # Additional notes
}
```

## Data Flow

### Add New Record
```
User Input → Validation → Create Backup → Append to CSV → Update UI
```

### Edit Record
```
Search Record → User Edits → Create Backup → Update CSV → Refresh UI
```

### Delete Record
```
Search Record → Preview → Confirm → Create Backup → Remove Row → Update CSV
```

### Backup & Restore
```
Create Backup → Save as CSV with Timestamp
Restore Backup → Read CSV File → Write to Main Database
```

## File Structure

```
Dr.-Sanjay/
├── app.py                           # Original application
├── app_enhanced.py                  # Enhanced version (v2.0)
├── requirements.txt                 # Original dependencies
├── requirements_enhanced.txt         # Enhanced dependencies
├── sample_livestock_data.csv         # Sample data
├── consolidated_livestock_data.csv  # Main database (runtime)
├── backups/                         # Backup files directory
│   ├── backup_20240101_120000.csv
│   ├── backup_20240101_130000.csv
│   └── ...
├── deployment/
│   ├── docker/
│   │   ├── Dockerfile
│   │   └── docker-compose.yml
│   └── heroku/
│       └── Procfile
├── README.md
├── FEATURES.md
├── ARCHITECTURE.md
└── DEPLOYMENT_GUIDE.md
```

## Key Technologies

### Framework
- **Streamlit**: Web framework for rapid development

### Data Processing
- **Pandas**: Data manipulation and CSV operations
- **Python datetime**: Date handling

### Visualization
- **Plotly**: Interactive charts and graphs

### Deployment
- **Docker**: Containerization
- **Heroku**: Cloud deployment

## Security Considerations

### Data Protection
- CSV data stored locally
- Automatic backups for recovery
- Confirmation dialogs for deletions
- Input validation to prevent errors

### Future Enhancements
- User authentication
- Role-based access control
- Data encryption
- Audit logging
- API authentication tokens

## Scalability

### Current Limitations
- CSV storage (works for ~10,000+ records)
- Single-file database (no concurrent access control)
- All data in memory during operations

### Migration Path
1. **Phase 1**: CSV with backup system (Current)
2. **Phase 2**: SQLite for better concurrency
3. **Phase 3**: PostgreSQL/MySQL for production
4. **Phase 4**: Distributed database for scaling

## Performance Optimization

### Current Optimizations
- Efficient pandas operations
- Indexed searches
- Lazy loading of visualizations

### Future Improvements
- Caching for analytics
- Pagination for large datasets
- Database indexing
- Query optimization
- Lazy loading of tables

## Deployment Architecture

### Local Deployment
- Single machine
- Development environment
- Direct file system access

### Docker Deployment
- Containerized application
- Volume-mounted database
- Easy scaling

### Cloud Deployment
- Heroku, AWS, GCP, Azure
- Persistent storage solutions
- Auto-scaling capabilities
- CDN support

## Monitoring & Logging

### Current State
- Streamlit logging
- File system monitoring via timestamps

### Future Enhancements
- Application logging
- Error tracking (Sentry)
- Performance monitoring
- User activity logs
- Database query logs
