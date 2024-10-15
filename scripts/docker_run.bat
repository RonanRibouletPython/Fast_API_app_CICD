set BACKEND_URL=http://localhost:8000/docs
set LOGIN_URL=http://localhost:8000/static/login.html

docker compose down
docker compose up --build -d
timeout 5
start "" %LOGIN_URL%