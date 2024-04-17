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

# 本番環境用
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info", "/app/backend/manage.py", "runserver", "0.0.0.0:8000"]