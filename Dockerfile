# Use a Python 3.11 slim image as the base
FROM python:3.11-slim

# Set environment variables for non-interactive installations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies (PostgreSQL, WeasyPrint, etc.)
RUN apt-get update \
    && apt-get install -y \
    libpq-dev \
    libcairo2 \
    libpango1.0-0 \
    libgdk-pixbuf2.0-0 \
    libjpeg-dev \
    gcc \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir -p /app/staticfiles/
RUN cp -r /app/static/* /app/staticfiles/

# Expose the port that the Django app will run on
EXPOSE 8000

# Run Gunicorn to serve the Django app (using the WSGI application)
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "property.wsgi:application"]
