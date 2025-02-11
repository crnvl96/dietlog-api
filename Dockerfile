# Use official Python 3.12 image
 FROM python:3.12-slim

 # Set environment variables
 ENV PYTHONDONTWRITEBYTECODE=1
 ENV PYTHONUNBUFFERED=1

 # Set working directory
 WORKDIR /app

 # Copy requirements files
 COPY pyproject.toml requirements.txt uv.lock ./

 # Install dependencies using pip
 RUN pip install --no-cache-dir -r requirements.txt

 # Copy the rest of the application code
 COPY . .

 # Expose the port FastAPI runs on
 EXPOSE 8000

 # Command to run the FastAPI server
 CMD ["fastapi", "dev", "/app/app/main.py"]
