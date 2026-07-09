# Livestock Registry Application - Deployment Guide

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/drsanjayvet01/Dr.-Sanjay.git
   cd Dr.-Sanjay
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements_enhanced.txt
   ```

4. **Prepare data**
   - Place your `consolidated_livestock_data.csv` in the application directory
   - Or use the provided `sample_livestock_data.csv`

5. **Run the application**
   ```bash
   streamlit run app_enhanced.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:8501`

---

## Docker Deployment

### Prerequisites
- Docker
- Docker Compose

### Deployment Steps

1. **Build and run with Docker Compose**
   ```bash
   cd deployment/docker
   docker-compose up -d
   ```

2. **Access the application**
   - Open your browser and go to `http://localhost:8501`

3. **Stop the container**
   ```bash
   docker-compose down
   ```

### Manual Docker Commands

**Build image:**
```bash
docker build -f deployment/docker/Dockerfile -t livestock-registry:latest .
```

**Run container:**
```bash
docker run -p 8501:8501 -v $(pwd)/data:/app -v $(pwd)/backups:/app/backups livestock-registry:latest
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Deployment Steps

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Create a new Heroku app**
   ```bash
   heroku create your-app-name
   ```

3. **Add Buildpacks**
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

5. **View logs**
   ```bash
   heroku logs --tail
   ```

6. **Access the application**
   - Open `https://your-app-name.herokuapp.com`

---

## Cloud Deployment (AWS, Google Cloud, Azure)

### AWS Elastic Beanstalk

1. **Install AWS CLI and Elastic Beanstalk CLI**
2. **Initialize Elastic Beanstalk**
   ```bash
   eb init -p python-3.9 livestock-registry
   ```
3. **Create environment and deploy**
   ```bash
   eb create livestock-env
   eb deploy
   ```

### Google Cloud Run

1. **Create `cloudbuild.yaml`**
2. **Deploy**
   ```bash
   gcloud run deploy livestock-registry --source . --platform managed --region us-central1
   ```

---

## Production Considerations

### Security
- Use environment variables for sensitive data
- Implement authentication (optional)
- Use HTTPS in production
- Regular backups of the database

### Performance
- Use a proper database instead of CSV for large datasets
- Implement caching for analytics
- Optimize queries and visualizations

### Database Migration
- Consider migrating from CSV to PostgreSQL/MySQL for production
- Use SQLAlchemy for database abstraction
- Implement connection pooling

### Monitoring
- Set up logging and monitoring
- Use error tracking services (Sentry)
- Monitor application performance

---

## Troubleshooting

### Port Already in Use
```bash
# On Linux/Mac
lsof -i :8501
kill -9 <PID>

# On Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Missing Database File
- Ensure `consolidated_livestock_data.csv` is in the app directory
- Use `sample_livestock_data.csv` as a template

### Streamlit Configuration
Create `.streamlit/config.toml` for custom settings:
```toml
[server]
port = 8501
maxUploadSize = 200

[logger]
level = "info"
```

---

## Support
For issues or questions, please open an issue on GitHub.
