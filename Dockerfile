# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Set the port for Google Cloud Run
ENV PORT=8080

# Start the app with gunicorn
CMD ["gunicorn", "--bind", ":8080", "app:app"]
