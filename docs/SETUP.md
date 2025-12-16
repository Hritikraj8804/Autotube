# Detailed Setup Guide

This guide provides step-by-step instructions for setting up AutoTube on different operating systems.

## Table of Contents

- [Windows Setup](#windows-setup)
- [Linux Setup](#linux-setup)
- [macOS Setup](#macos-setup)
- [Configuration Guide](#configuration-guide)
- [First Run](#first-run)
- [Troubleshooting Setup](#troubleshooting-setup)

## Prerequisites for All Platforms

### Required Software

1. **Docker**
   - Windows: Docker Desktop for Windows
   - Linux: Docker Engine + Docker Compose
   - macOS: Docker Desktop for Mac

2. **Git** (for cloning the repository)

3. **System Requirements**
   - **RAM:** 4GB minimum, 8GB recommended
   - **Disk:** 10GB free space minimum (for Docker images and videos)
   - **CPU:** 2+ cores recommended
   - **Internet:** Required for initial setup and AI services

---

## Windows Setup

### 1. Install Docker Desktop

1. Download [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
2. Run the installer
3. Enable WSL 2 backend (recommended)
4. Restart your computer
5. Start Docker Desktop
6. Verify installation:
   ```powershell
   docker --version
   docker-compose --version
   ```

### 2. Install Git (if not already installed)

1. Download [Git for Windows](https://git-scm.com/download/win)
2. Run installer with default options
3. Verify:
   ```powershell
   git --version
   ```

### 3. Clone the Repository

```powershell
# Open PowerShell or Command Prompt
cd C:\Users\YourUsername\Documents
git clone https://github.com/Hritikraj8804/Autotube.git
cd Autotube
```

### 4. Configure Environment

```powershell
cd short_automation
copy .env.example .env
notepad .env
```

Edit `.env` with your settings (see [Configuration Guide](#configuration-guide))

### 5. Start AutoTube

**Option A: Using Batch Script (Recommended)**
```powershell
# Double-click START-ROBOT.bat
# OR run from command line:
.\START-ROBOT.bat
```

**Option B: Using Docker Compose**
```powershell
cd short_automation
docker-compose up -d
```

### 6. Verify Services

```powershell
docker ps
```

You should see 7 containers running.

### 7. Access Services

- **n8n**: http://localhost:5678
- **FileBrowser**: http://localhost:8080

---

## Linux Setup

### 1. Install Docker Engine

**Ubuntu/Debian:**
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install ca-certificates curl gnupg

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Verify installation
docker --version
docker compose version
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo systemctl start docker
sudo systemctl enable docker
```

### 2. Add User to Docker Group (Optional)

```bash
sudo usermod -aG docker $USER
# Log out and back in for this to take effect
```

### 3. Clone Repository

```bash
cd ~
git clone https://github.com/Hritikraj8804/Autotube.git
cd Autotube/short_automation
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env  # or use vim, gedit, etc.
```

### 5. Start Services

```bash
docker compose up -d

# View logs
docker compose logs -f
```

### 6. Set Up Automatic Startup (Optional)

Create a systemd service:

```bash
sudo nano /etc/systemd/system/autotube.service
```

Add:
```ini
[Unit]
Description=AutoTube Docker Compose
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/yourusername/Autotube/short_automation
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable autotube.service
sudo systemctl start autotube.service
```

---

## macOS Setup

### 1. Install Docker Desktop

1. Download [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
2. Drag Docker.app to Applications
3. Launch Docker Desktop
4. Grant necessary permissions
5. Verify:
   ```bash
   docker --version
   docker compose version
   ```

### 2. Install Git (if needed)

```bash
# Using Homebrew
brew install git

# OR install Xcode Command Line Tools
xcode-select --install
```

### 3. Clone Repository

```bash
cd ~/Documents
git clone https://github.com/Hritikraj8804/Autotube.git
cd Autotube/short_automation
```

### 4. Configure and Start

```bash
cp .env.example .env
nano .env  # Edit configuration

# Start services
docker compose up -d
```

---

## Configuration Guide

### Required Environment Variables

Edit `.env` file in the `short_automation` directory:

```env
# ===================================
# n8n Authentication
# ===================================
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=your_email@example.com
N8N_BASIC_AUTH_PASSWORD=YourSecurePassword123!

# ===================================
# Encryption Key
# ===================================
# Generate with: openssl rand -hex 32
N8N_ENCRYPTION_KEY=your-random-32-character-encryption-key-here

# ===================================
# PostgreSQL Database
# ===================================
POSTGRES_USER=n8n
POSTGRES_PASSWORD=YourSecureDatabasePassword123!
POSTGRES_DB=n8n
```

### Generating Secure Encryption Key

**Windows (PowerShell):**
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
```

**Linux/macOS:**
```bash
openssl rand -hex 32
```

### Optional: HuggingFace Token (Better AI Images)

1. Create free account at [HuggingFace](https://huggingface.co/)
2. Go to Settings → Access Tokens
3. Create new token
4. Add to `.env`:
   ```env
   HUGGINGFACE_TOKEN=hf_your_token_here
   ```

---

## First Run

### 1. Download AI Model

```bash
# Windows PowerShell / Linux / macOS
docker exec youtube-ai ollama pull llama3.1:8b
```

This downloads the LLaMA 3.1 8B model (~4.7GB). First time only.

### 2. Import n8n Workflow

1. Open http://localhost:5678
2. Log in with credentials from `.env`
3. Click **Workflows** → **Import from File**
4. Browse to `short_automation/workflows/autotube-complete.json`
5. Click **Import**
6. **Activate** the workflow (toggle switch at top)

### 3. Configure Groq API (for AI and TTS)

AutoTube uses Groq for fast AI script generation and TTS:

1. Get free API key from [Groq Console](https://console.groq.com/keys)
2. In n8n, go to **Credentials** → **Add Credential**
3. Select **HTTP Bearer Authentication**
4. Name: `Groq API`
5. Token: Paste your Groq API key
6. Save

### 4. Test Your First Video

1. Open the **AutoTube - Complete Pipeline** workflow
2. Click the **Manual Trigger** node
3. Edit the **Set Topic** node with your video idea:
   ```json
   {
     "topic": "5 Amazing AI Tools in 2025"
   }
   ```
4. Click **Test Workflow** (play button at bottom right)
5. Watch the workflow execute!
6. Find your video in `short_automation/videos/`

---

## Troubleshooting Setup

### Docker Won't Start

**Windows:**
- Enable Virtualization in BIOS
- Enable WSL 2: `wsl --install`
- Check Windows Features: Hyper-V, Containers

**Linux:**
- Check Docker service: `sudo systemctl status docker`
- Start if needed: `sudo systemctl start docker`

**macOS:**
- Grant all permissions in System Preferences
- Increase Docker Desktop memory (Preferences → Resources)

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :5678
# Kill process using the port

# Linux/macOS
lsof -i :5678
# Kill with: kill -9 <PID>
```

Or change ports in `docker-compose.yml`:
```yaml
ports:
  - "5679:5678"  # Use 5679 instead of 5678
```

### Containers Keep Restarting

```bash
# Check logs
docker compose logs -f

# Restart all services
docker compose down
docker compose up -d
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a

# Remove old videos
cd short_automation/videos
rm *.mp4  # Windows: del *.mp4
```

### Connection Refused

Wait 30 seconds after startup for all services to initialize:

```bash
# Check if containers are healthy
docker ps

# Check specific service logs
docker compose logs n8n
docker compose logs python
```

### n8n Login Fails

Verify `.env` credentials:
```bash
# Windows
type short_automation\.env

# Linux/macOS
cat short_automation/.env
```

### Python API Not Responding

```bash
# Restart Python container
docker restart youtube-python

# Check if API is running
curl http://localhost:5001/health
```

### AI Model Not Found

```bash
# List installed models
docker exec youtube-ai ollama list

# Pull LLaMA model
docker exec youtube-ai ollama pull llama3.1:8b
```

---

## Next Steps

After successful setup:

1. **Read the [n8n Workflow Guide](N8N_WORKFLOW.md)** to understand the automation
2. **Explore [Python API Documentation](PYTHON_API.md)** for customization
3. **Check [Architecture Overview](ARCHITECTURE.md)** to understand the system
4. **Review [Troubleshooting Guide](TROUBLESHOOTING.md)** for common issues

## Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions and share ideas
- **Documentation**: Check other docs in this folder

---

**Happy Automating! 🚀**
