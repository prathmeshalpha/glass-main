# Use a Python 3.11 slim image as the base
FROM python:3.11-slim

# Set environment variables for non-interactive installations
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install the Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Create the staticfiles directory (if it doesn't exist)
RUN mkdir -p /app/staticfiles/

# Copy static files from /app/static to /app/staticfiles
RUN cp -r /app/static/* /app/staticfiles/

# Expose the port that the Django app will run on
EXPOSE 8000

# Set the default command (to be overridden by docker-compose.yml)
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "property.wsgi:application"]
