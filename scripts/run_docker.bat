:: set the variable to store the image name and the URL of the application
set IMAGE_NAME=my-fastapi-app

:: check if the docke image exists
docker build -t %IMAGE_NAME% .

:: run the containder mapped on port 8000
echo Starting container...
docker run -d -p 8000:8000 %IMAGE_NAME% 