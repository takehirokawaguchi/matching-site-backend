# 開発環境用
# Base image
# FROM python:3.10

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app/backend

# # Install dependencies
# COPY ./requirements.txt /app/backend/
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy project
# COPY . /app/

# 本番環境用
#Base image
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
COPY . /app/backend/

# RUN chmod a+x build.sh
# ENTRYPOINT [ "bash", "./build.sh" ]
# CMD [ "gunicorn", "backend.wsgi" ]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
