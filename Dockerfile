# Use an official Python image with system packages
FROM python:3.9-slim

# Install system dependencies (libGL, ffmpeg, etc.)
RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install (Task 1 by default)
COPY task1/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code
COPY . .

# Expose Streamlit port
EXPOSE 8080

# Set Streamlit config (optional: disables browser auto-opening)
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV STREAMLIT_SERVER_HEADLESS=true

# Run Streamlit app for Task 1 by default
CMD ["streamlit", "run", "task1/streamlit_app.py", "--server.port=8080", "--server.address=0.0.0.0"]
