# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt, including Gunicorn
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Expose the port Gunicorn will run on
EXPOSE 8585

# Run Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8585", "main:app"]
