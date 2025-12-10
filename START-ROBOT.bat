@echo off
echo 🚀 Starting YouTube Automation Factory...
cd /d "C:\Users\hriti\project\n8n\short_automation"
docker-compose up -d
timeout 20
echo.
echo ✅ ALL SERVICES STARTED:
echo.
echo 🌐 n8n Dashboard:    http://localhost:5678
echo 👤 Login: redroy9525@gmail.com / 8804895628@Hr
echo.
echo 🧠 AI Server:        http://localhost:11434
echo 🔊 TTS Server:       http://localhost:5500
echo 📊 Docker Dashboard: http://localhost:9000
echo 📁 File Manager:     http://localhost:8080
echo.
echo 🔍 Check: docker ps (should show 8 containers)
echo.
pause