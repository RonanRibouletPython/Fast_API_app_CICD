# Use a slimmer base image if possible (e.g., python:3.11-slim-bullseye)
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy only the necessary files for dependencies (smaller image size)
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip poetry
RUN poetry install --no-interaction --no-root 

# Copy the rest of the application code
COPY . .

# Expose the port your FastAPI app listens on
EXPOSE 8000

WORKDIR /app

CMD ["poetry", "run", "uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "8000"]