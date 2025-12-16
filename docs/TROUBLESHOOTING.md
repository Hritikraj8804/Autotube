# Troubleshooting Guide

Common issues and solutions for AutoTube.

## Table of Contents

- [Docker Issues](#docker-issues)
- [n8n Issues](#n8n-issues)
- [Python/Video Issues](#pythonvideo-issues)
- [AI/Script Generation Issues](#aiscript-generation-issues)
- [Network Issues](#network-issues)
- [Performance Issues](#performance-issues)

---

## Docker Issues

### Docker Won't Start

**Symptoms:**
- Docker Desktop won't launch
- "Docker daemon not running" error

**Solutions:**

**Windows:**
```powershell
# 1. Enable Virtualization in BIOS
# Restart computer → Enter BIOS → Enable VT-x/AMD-V

# 2. Enable WSL 2
wsl --install
wsl --set-default-version 2

# 3. Enable Windows Features
# Settings → Apps → Optional Features → More Windows Features
# Enable: Hyper-V, Windows Hypervisor Platform, Virtual Machine Platform

#4. Restart Docker Desktop
```

**Linux:**
```bash
# Check Docker service status
sudo systemctl status docker

# Start Docker if stopped
sudo systemctl start docker

# Enable Docker to start on boot
sudo systemctl enable docker

# Check for errors
journalctl -u docker.service -n 50
```

**macOS:**
```bash
# Grant permissions
# System Preferences → Security & Privacy → Grant Docker permissions

# Increase resources
#Docker Desktop → Preferences → Resources
# CPU: 4+ cores
# Memory: 4GB+
```

---

### Containers Won't Start

**Symptoms:**
```
docker-compose up -d
# Some containers exit immediately or restart loop
```

**Diagnosis:**
```bash
# Check container status
docker ps -a

# View logs for specific container
docker logs youtube-automation
docker logs youtube-python
docker logs youtube-ai

# Check all logs
docker-compose logs
```

**Common Causes:**

#### Port Already in Use
```bash
# Windows - Find process using port
netstat -ano | findstr :5678
taskkill /PID <process_id> /F

# Linux/macOS
lsof -i :5678
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5679:5678"  # Use different external port
```

#### Permission Issues (Linux)
```bash
# Fix volume permissions
sudo chown -R $USER:$USER ./data ./videos

# Docker without sudo
sudo usermod -aG docker $USER
# Log out and back in
```

#### Out of Memory
```bash
# Check Docker stats
docker stats

# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory (8GB recommended)

# Linux - Check system memory
free -h

# Stop unnecessary containers
docker stop $(docker ps -q)
```

---

### Docker Out of Disk Space

**Symptoms:**
- "No space left on device" error
- Containers won't start

**Solutions:**
```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a --volumes
# WARNING: This removes all unused containers, images, and volumes

# Or selectively clean
docker container prune  # Remove stopped containers
docker image prune -a   # Remove unused images
docker volume prune     # Remove unused volumes

# Check available disk space
df -h  # Linux/macOS
# Windows: File Explorer → This PC
```

---

## n8n Issues

### Can't Access n8n (http://localhost:5678)

**Symptoms:**
- "Connection refused"
- "This site can't be reached"

**Diagnosis:**
```bash
# Check if n8n container is running
docker ps | grep youtube-automation

# Check n8n logs
docker logs youtube-automation

# Test from inside container
docker exec youtube-automation curl http://localhost:5678
```

**Solutions:**

1. **Wait for startup** (takes 20-30 seconds)
   ```bash
   # Watch startup logs
   docker logs -f youtube-automation
   # Wait for: "Ready to accept connections"
   ```

2. **Check port binding**
   ```bash
   docker port youtube-automation
   # Should show: 5678/tcp -> 0.0.0.0:5678
   ```

3. **Restart container**
   ```bash
   docker restart youtube-automation
   
   # Or restart all
   docker-compose down
   docker-compose up -d
   ```

4. **Check firewall**
   ```powershell
   # Windows: Allow in firewall
   # Settings → Update & Security → Windows Security → Firewall
   # Allow Docker Desktop
   ```

---

### n8n Login Fails

**Symptoms:**
- "Invalid credentials"
- Login page keeps reloading

**Solutions:**

1. **Verify credentials in .env**
   ```bash
   # Windows
   type short_automation\.env
   
   # Linux/macOS
   cat short_automation/.env
   
   # Check these lines:
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=your_email@example.com
   N8N_BASIC_AUTH_PASSWORD=your_password
  ```

2. **Restart n8n after .env changes**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Clear browser cache**
   - Ctrl+Shift+Delete
   - Clear cookies and cached files
   - Try incognito/private mode

4. **Reset n8n**
   ```bash
   # Backup workflows first!
   docker-compose down
   rm -rf ./data/n8n/*  # WARNING: Deletes all n8n data
   docker-compose up -d
   ```

---

### Workflow Won't Import

**Symptoms:**
- "Invalid workflow format"
- Import button grayed out

**Solutions:**

1. **Check JSON format**
   ```bash
   # Validate JSON
   python -m json.tool short_automation/workflows/autotube-complete.json
   ```

2. **Try downloading again**
   - File may be corrupted
   - Use Git LFS for large files

3. **Manual import**
   - Copy JSON content
   - In n8n: New Workflow → Code → Paste

---

### Workflow Execution Fails

**Symptoms:**
- Red error nodes
- "Execution failed"

**Diagnosis:**
```bash
# Check execution details in n8n UI
# Click on failed node → View error message

# Common error types:
# - Authentication failed  → Check credentials
# - Timeout               → Increase timeout
# - Connection refused    → Check service is running
# - Invalid response      → Check API endpoint
```

**Solutions:**

1. **Test each node individually**
   - Click node → "Execute Node"
   - Find where it breaks

2. **Check credentials**
   - n8n → Credentials
   - Verify Groq API key is correct
   - Test connection

3. **Increase timeouts**
   - Open failing HTTP Request node
   - Options → Timeout → 300000 (5 minutes)

4. **Check service connectivity**
   ```bash
   # Test Python API
   docker exec youtube-automation curl http://python:5001/health
   
   # Test Ollama
   docker exec youtube-automation curl http://ollama:11434/api/tags
   ```

---

## Python/Video Issues

### Video Generation Fails

**Symptoms:**
- "Video file was not created"
- Python API returns error

**Diagnosis:**
```bash
# Check Python logs
docker logs youtube-python

# Test Python API directly
curl http://localhost:5001/health

# Check if Python container is running
docker ps | grep youtube-python
```

**Common Errors:**

#### "ModuleNotFoundError"
```bash
# Install missing packages
docker exec youtube-python pip install moviepy Pillow requests flask

# Or install from requirements.txt
docker exec youtube-python pip install -r /scripts/requirements.txt
```

#### "Permission denied" writing video
```bash
# Fix permissions (Linux)
sudo chown -R $USER:$USER ./short_automation/videos

# Windows: Run Docker Desktop as Administrator
```

#### "Out of memory" during video export
```bash
# Increase Docker memory
# Docker Desktop → Settings → Resources → Memory: 8GB

# Or reduce video quality in create_video.py
# Change: preset='ultrafast', bitrate='2000k'
```

#### "Audio file not found"
```bash
# Check audio path is correct
ls -la ./short_automation/videos/audio_*

# Verify path format uses /videos not ./videos
# Correct:   /videos/audio_xxx.wav
# Incorrect: ./videos/audio_xxx.wav
```

---

### AI Image Generation Fails

**Symptoms:**
- "Image generation failed"
- Video has missing/duplicate images

**Solutions:**

1. **Check internet connection**
   ```bash
   # Test from Python container
   docker exec youtube-python curl https://image.pollinations.ai
   ```

2. **Try different AI provider**
   - Edit workflow
   - In Generate Video node, set:
     ```json
     {"useAiImages": false}
     ```
   - Uses fallback placeholders

3. **Use Z-Image instead**
   - Get HuggingFace token
   - Add to .env: `HUGGINGFACE_TOKEN=your_token`
   - Edit ai_generator.py to use Z-Image

4. **Check rate limiting**
   - Pollinations.ai may throttle
   - Add delays in code:
     ```python
     time.sleep(2)  # Wait 2 seconds between images
     ```

---

### Video Has No Audio

**Symptoms:**
- Video plays but no sound
- Silent video

**Solutions:**

1. **Check audio file exists**
   ```bash
   ls -la ./short_automation/videos/audio_*
   ```

2. **Verify audio format**
   ```bash
   # Should be WAV format
   file ./short_automation/videos/audio_xxx.wav
   ```

3. **Test audio playback**
   ```bash
   # Play audio (Linux)
   docker exec youtube-python apt-get update && apt-get install -y ffmpeg
   docker exec youtube-python ffmpeg -i /videos/audio_xxx.wav -f null -
   # Should show audio stream info
   ```

4. **Check audio path in workflow**
   - Verify audioPath is correctly passed to video generation
   - Use full path: `/videos/audio_xxx.wav`

---

## AI/Script Generation Issues

### Groq API Errors

**Symptoms:**
- "Authentication failed"
- "Rate limit exceeded"
- "Invalid API key"

**Solutions:**

1. **Verify API key**
   ```bash
   # Test Groq API directly
   curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer gsk_your_key_here"
   ```

2. **Regenerate API key**
   - Go to https://console.groq.com/keys
   - Delete old key
   - Create new key
   - Update in n8n credentials

3. **Check rate limits**
   - Free tier: 30 requests/minute
   - Wait and retry
   - Or upgrade to paid tier

4. **Use Ollama instead**
   - Change workflow to use local Ollama
   - Endpoint: `http://ollama:11434/api/generate`
   - Model: `llama3.1:8b`

---

### Ollama Not Responding

**Symptoms:**
- Connection timeout
- Model not found

**Solutions:**

1. **Check Ollama is running**
   ```bash
   docker ps | grep youtube-ai
   docker logs youtube-ai
   ```

2. **Pull model**
   ```bash
   docker exec youtube-ai ollama list
   
   # If model missing
   docker exec youtube-ai ollama pull llama3.1:8b
   ```

3. **Test Ollama**
   ```bash
   docker exec youtube-ai ollama run llama3.1:8b "Hello"
   ```

4. **Increase timeout**
   - First run may be slow (loading model)
   - Wait 30-60 seconds

---

### Poor Quality Scripts

**Symptoms:**
- Scripts don't follow format
- Generic/boring content

**Solutions:**

1. **Improve prompt**
   - Edit AI Script Writer node
   - Be more specific:
     ```javascript
     "Create a VIRAL YouTube Shorts script about: ${topic}
     Use hooks that create curiosity.
     Make it energetic and fast-paced.
     Include numbers and specific examples."
     ```

2. **Adjust temperature**
   ```json
   {
     "temperature": 0.9  // More creative
   }
   ```

3. **Try different model**
   ```json
   {
     "model": "llama-3.1-70b-versatile"  // Larger, better model
   }
   ```

4. **Provide examples**
   - Include example scripts in system prompt

---

## Network Issues

### Containers Can't Communicate

**Symptoms:**
- "Connection refused" between services
- Python can't reach n8n, etc.

**Diagnosis:**
```bash
# Check all containers are on same network
docker network inspect automation-network

# Test connectivity
docker exec youtube-automation ping python
docker exec youtube-python ping ollama
```

**Solutions:**

1. **Recreate network**
   ```bash
   docker-compose down
   docker network prune
   docker-compose up -d
   ```

2. **Use service names, not localhost**
   - ✅ `http://python:5001`
   - ❌ `http://localhost:5001`

3. **Check docker-compose.yml**
   - Ensure all services use `automation-network`

---

### Can't Access from Host

**Symptoms:**
- Can't open http://localhost:5678 from browser

**Solutions:**

1. **Check port mapping**
   ```bash
   docker ps
   # Should show: 0.0.0.0:5678->5678/tcp
   ```

2. **Try 127.0.0.1 instead**
   - http://127.0.0.1:5678

3. **Check Windows firewall**
   - Allow Docker Desktop
   - Allow private networks

---

## Performance Issues

### Slow Video Generation

**Symptoms:**
- Takes >10 minutes to create video

**Solutions:**

1. **Use faster encoding preset**
   - Edit `create_video.py`
   - Change: `preset='ultrafast'`

2.**Reduce image generation time**
   - Use Pollinations instead of Z-Image
   - Disable AI images: `useAiImages: false`

3. **Increase Docker resources**
   - Docker Desktop → Settings → Resources
   - CPU: 4+ cores
   - Memory: 8GB

4. **Use SSD**
   - Store `./videos` on SSD not HDD

---

### High CPU/Memory Usage

**Symptoms:**
- Computer slow while generating videos
- Docker using too much resources

**Solutions:**

```bash
# Limit Docker resources
# Docker Desktop → Settings → Resources
# CPU: 50% of cores
# Memory: 6GB

# Or in docker-compose.yml
services:
  python:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
```

---

## General Debugging Tips

### Enable Debug Logging

```bash
# n8n debug logs
docker exec youtube-automation n8n --help

# Python debug logs
# Edit video_api.py
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Check All Services

```bash
# Health check script
curl http://localhost:5678              # n8n
curl http://localhost:5001/health        # Python API
curl http://localhost:11434/api/tags     # Ollama
curl http://localhost:5500/api/voices    # OpenTTS (if used)
curl http://localhost:8080               # FileBrowser
```

### View All Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker logs -f youtube-python

# Last 100 lines
docker logs --tail 100 youtube-automation
```

### Restart Everything 

```bash
# Complete restart
docker-compose down
docker system prune -f
docker-compose up -d

# Check all healthy
docker ps
```

---

## Still Having Issues?

1. **Check logs** - Most errors show in Docker logs
2. **Search issues** - GitHub Issues may have solution
3. **Ask community** - GitHub Discussions
4. **Report bug** - Create detailed GitHub Issue with:
   - Error message
   - Steps to reproduce
   - Docker logs
   - System info (OS, Docker version)

---

## Useful Commands Reference

```bash
# === Docker ===
docker-compose up -d          # Start all services
docker-compose down           # Stop all services
docker-compose logs -f        # View logs
docker ps                     # List running containers
docker restart <container>    # Restart container

# === n8n ===
# Access: http://localhost:5678
# Logs: docker logs youtube-automation

# === Python ===
docker exec youtube-python python /scripts/video_api.py
docker logs youtube-python

# === Ollama ===
docker exec youtube-ai ollama list
docker exec youtube-ai ollama pull llama3.1:8b

# === Cleanup ===
docker system prune -a
rm -rf ./short_automation/data/*
rm -rf ./short_automation/videos/*

# === Testing ===
curl http://localhost:5001/health
curl http://localhost:5678
docker exec youtube-python python /scripts/ai_generator.py
```

---

**Remember:** Most issues are solved by restarting containers or checking logs!
