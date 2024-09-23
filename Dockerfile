# use the official Python image as the base image
FROM python:3.11-slim
# set the working directory in the container
WORKDIR /app
# copy the dependencies file to the working directory
COPY . /app
# install dependencies
RUN pip install poetry
# install dependencies
RUN poetry install --no-interaction --no-root
# get to the directory of the application
WORKDIR /app/app
# expose the port
EXPOSE 8000
# define the command to run on container start with poetry
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]