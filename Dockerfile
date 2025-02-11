# Use official Python 3.12 image
FROM python:3.12-slim

COPY ./app /code/app

# Set working directory
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install dependencies using pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["fastapi", "run", "app/main.py", "--port", "8000"]
