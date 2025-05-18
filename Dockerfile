# Use official Python image as base
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (commonly used for FastAPI/Uvicorn)
EXPOSE 8000

# Command to run the FastAPI app with Uvicorn
CMD ["uvicorn", "agente_turistik:app", "--host", "0.0.0.0", "--port", "8000"]
