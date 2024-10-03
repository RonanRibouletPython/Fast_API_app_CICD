set APP_URL=http://localhost:8000/docs

docker compose down
docker compose up --build -d
timeout 5
start "" %APP_URL%