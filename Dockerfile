# Base image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app/backend

# Install dependencies
COPY ./requirements.txt /app/backend/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/