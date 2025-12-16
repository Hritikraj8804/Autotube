@echo off
echo 🔧 Testing All Containers...
cd /d "C:\Users\hriti\project\n8n\short_automation"

echo.
echo 📊 Running Containers:
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo.
echo 🔍 Testing Services:
echo.
echo 1. n8n: http://localhost:5678 (configure in .env)
echo 2. Ollama: http://localhost:11434
echo 3. TTS: http://localhost:5500
echo 4. File Browser: http://localhost:8080 (admin/admin)
echo 5. PostgreSQL: docker exec youtube-db psql -U n8n -c "select 1"
echo 6. Redis: docker exec youtube-cache redis-cli ping
echo 7. Python: docker exec youtube-python python --version

echo.
pause