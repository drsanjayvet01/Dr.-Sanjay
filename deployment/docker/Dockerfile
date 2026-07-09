FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_enhanced.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_enhanced.txt

# Copy application
COPY app_enhanced.py .
COPY sample_livestock_data.csv .
COPY consolidated_livestock_data.csv . || true

# Create backup directory
RUN mkdir -p backups

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "app_enhanced.py", "--server.port=8501", "--server.address=0.0.0.0"]
