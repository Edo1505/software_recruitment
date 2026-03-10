# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the index.html file to the working directory
COPY index.html .

# Expose port 8000 to allow communication
EXPOSE 8000

# Start the Python built-in HTTP server
CMD ["python3", "-m", "http.server", "8000"]