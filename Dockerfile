# Use the official Python image as the base image
FROM python:latest

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application to the working directory
COPY . .

# Expose the application port (if needed)
EXPOSE 8000

# Define the default command to run the applicationp
CMD ["python", "app.py"]