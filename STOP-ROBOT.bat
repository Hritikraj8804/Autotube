@echo off
echo 🛑 Stopping YouTube Automation Factory...
cd /d "C:\Users\hriti\project\n8n\short_automation"
docker-compose down
echo.
echo ✅ All containers stopped and removed.
echo 💾 Your data is saved in ./data/ folders
echo.
pause
