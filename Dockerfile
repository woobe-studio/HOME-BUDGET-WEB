# Use official Python image as base
FROM python:3.10.0

# Set working directory in container
WORKDIR /app

# Copy project files to container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add permission to wait-for-db.sh
RUN chmod +x wait-for-db.sh

# Expose port 8000 for Django
EXPOSE 8000

# Define the default command
CMD ["sh", "-c", "python manage.py migrate && ./wait-for-db.sh db python manage.py runserver 0.0.0.0:8000"]
