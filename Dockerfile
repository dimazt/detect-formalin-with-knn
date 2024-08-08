FROM python:3.9

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Command to run the application
CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "app:app"]
