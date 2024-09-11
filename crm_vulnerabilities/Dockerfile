# Base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of the project
COPY . /app/

# Expose the port Django will run on
EXPOSE 8000

# Default command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
