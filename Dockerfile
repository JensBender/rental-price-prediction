# Use the official Python image as a parent image
FROM python:3-alpine3.10

# Set the working directory within the container
WORKDIR /app

# Copy all necessary model deployment files into the container
COPY model_deployment.py model_deployment.py
COPY models/ models/
COPY static/ static/
COPY templates/ templates/
COPY deployment_requirements.txt deployment_requirements.txt

# Expose a port for the Flask app to run on
EXPOSE 8080

# Define the command to run when the container starts
CMD ["python", "model_deployment.py"]