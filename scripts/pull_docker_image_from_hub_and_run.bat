:: set the variables
set IMAGE_NAME=my-fastapi-app
set TAG=latest
set USERNAME=ronanribouletpython
set APP_URL=http://localhost:8000/docs

:: pull the docker image from the docker hub
docker pull %USERNAME%/%IMAGE_NAME%:%TAG%

:: run the pulled docker image
docker run -d -p 8000:8000 %IMAGE_NAME%:%TAG%

:: wait for 5 seconds
timeout 5

:: open the browser
start "" %APP_URL%
