# Use a slimmer base image
FROM python:3.11-slim-bullseye

# Install build essentials and PostgreSQL client development package
RUN apt-get update && apt-get install -y build-essential libpq-dev 

# Set the working directory
WORKDIR /app

# Copy only the necessary files for dependencies
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry install --no-interaction --no-root 

# Copy the rest of the application code
COPY . .

# Expose the port your FastAPI app listens on
EXPOSE 8000

# Start the application
CMD ["poetry", "run", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]