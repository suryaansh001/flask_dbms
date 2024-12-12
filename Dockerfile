# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /surya

# Copy the current directory contents into the container at /surya
COPY . /surya

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside the container
EXPOSE 5000

# Define environment variable to tell Flask to run in production mode
ENV FLASK_ENV=production

# Run sury.py when the container launches
CMD ["python", "surya.py"]
