FROM python:3.12.3-slim

# Set the working directory
WORKDIR /code

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip and install dependencies with debug information
RUN pip3 install --no-cache-dir -r requirements.txt

# Check the pip log file for errors

# Copy the project files
COPY . .

# Copy static and template files
COPY ./static /code/static
COPY ./templates /code/templates
COPY ./tmp /code/tmp

# Command to run the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]