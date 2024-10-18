# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8006 available to the world outside this container
EXPOSE 8006

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run uvicorn server
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8006"]
