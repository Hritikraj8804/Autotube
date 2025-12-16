# 🤖 AutoTube - Automated YouTube Shorts Factory

> **Fully automated YouTube Shorts creation system using n8n, AI image generation, and video processing**

AutoTube is a complete automation pipeline for generating, creating, and publishing YouTube Shorts using AI. It combines n8n workflow automation, AI-powered script generation, dynamic image slideshows, text-to-speech, and video editing into one powerful system.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![n8n](https://img.shields.io/badge/n8n-Workflow-orange.svg)](https://n8n.io/)

## ✨ Features

- 🎬 **End-to-End Automation**: From topic to published video, fully automated
- 🧠 **AI Script Generation**: Uses Ollama/LLaMA for engaging script writing
- 🎨 **AI Image Slideshows**: Generates multiple AI images per video using Pollinations.ai or Z-Image
- 🎞️ **Professional Video Creation**: Ken Burns zoom effects, crossfade transitions, text overlays
- 🔊 **Text-to-Speech**: OpenTTS for natural voiceovers
- 📤 **YouTube Upload**: Direct upload to YouTube with metadata
- 🐳 **Docker-Based**: All services containerized for easy deployment
- 🔄 **n8n Workflow**: Visual automation with error handling and monitoring

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AutoTube System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐    │
│  │   n8n    │──▶│ Ollama   │──▶│  Python  │──▶│ YouTube   │   │
│  │ Workflow │    │   AI    │    │ Video API│    │   API    │    │
│  └──────────┘    └─────────┘    └──────────┘    └──────────┘    │
│       │               │                │              │         │
│       │               │                │              │         │
│       ▼               ▼                ▼              ▼         │
│  ┌──────────┐    ┌─────────┐    ┌──────────┐    ┌──────────┐    │
│  │PostgreSQL│    │ OpenTTS │    │   AI     │    │  Redis   │    │
│  │    DB    │    │  Voice  │    │  Images  │    │  Cache   │    │
│  └──────────┘    └─────────┘    └──────────┘    └──────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### System Components

| Component | Purpose | Port |
|-----------|---------|------|
| **n8n** | Workflow automation orchestrator | 5678 |
| **Ollama** | Local AI for script generation (LLaMA 3.1) | 11434 |
| **OpenTTS** | Text-to-speech conversion | 5500 |
| **Python API** | Video creation & AI image generation | 5001 |
| **PostgreSQL** | n8n database | 5432 |
| **Redis** | Caching layer | 6379 |
| **FileBrowser** | File management UI | 8080 |

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (Windows/Mac) or Docker Engine (Linux)
- **Docker Compose** v2.0+
- **Git**
- **4GB RAM minimum** (8GB recommended)
- **10GB free disk space**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Hritikraj8804/Autotube.git
   cd Autotube
   ```

2. **Configure environment variables**
   ```bash
   cd short_automation
   cp .env.example .env
   ```
   
   Edit `.env` and set:
   ```env
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=your_email@example.com
   N8N_BASIC_AUTH_PASSWORD=your_secure_password
   N8N_ENCRYPTION_KEY=generate-a-random-key-here
   POSTGRES_PASSWORD=your_secure_db_password
   ```

3. **Start the system**
   
   **Windows:**
   ```bash
   START-ROBOT.bat
   ```
   
   **Linux/Mac:**
   ```bash
   cd short_automation
   docker-compose up -d
   ```

4. **Access services**
   - n8n Dashboard: http://localhost:5678
   - File Browser: http://localhost:8080
   - AI Server: http://localhost:11434

5. **Import the workflow**
   - Open n8n at http://localhost:5678
   - Click **Workflows** → **Import from File**
   - Select `short_automation/workflows/autotube-complete.json`
   - Activate the workflow

6. **Download AI model**
   ```bash
   docker exec youtube-ai ollama pull llama3.1:8b
   ```

## 📖 Usage

### Creating Your First Video

1. **Open n8n** at http://localhost:5678
2. **Find the AutoTube workflow** and open it
3. **Configure the Manual Trigger node** with your video topic:
   ```json
   {
     "topic": "Top 5 AI Tools in 2025"
   }
   ```
4. **Click "Test Workflow"** and watch the magic happen!

### How It Works

1. **Script Generation**: AI generates a 30-second script with hook, content, and CTA
2. **Image Creation**: Multiple AI images are generated based on script sections
3. **Voice Generation**: Text-to-speech creates professional voiceover
4. **Video Compilation**: Images are assembled with transitions, zoom effects, and text overlays
5. **YouTube Upload**: Video is uploaded with title, description, and tags

### Video Specifications

- **Format**: Vertical 9:16 (1080x1920)
- **Duration**: ~30 seconds (YouTube Shorts)
- **FPS**: 30
- **Effects**: Ken Burns zoom, crossfade transitions
- **Audio**: OpenTTS voice synthesis

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `short_automation` directory:

```env
# n8n Authentication
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=your_email@example.com
N8N_BASIC_AUTH_PASSWORD=your_secure_password

# Encryption
N8N_ENCRYPTION_KEY=your-random-32-char-key

# Database
POSTGRES_USER=n8n
POSTGRES_PASSWORD=your_secure_db_password
POSTGRES_DB=n8n

# Optional: HuggingFace token for Z-Image (better quality)
HUGGINGFACE_TOKEN=your_hf_token_here
```

### YouTube API Setup

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable **YouTube Data API v3**
3. Create OAuth 2.0 credentials
4. Download credentials as `client_secret_*.json`
5. Place in `short_automation/` directory (already gitignored)

### AI Image Generation

AutoTube supports two AI image providers:

**Pollinations.ai** (Default - Free, Unlimited)
- No API key required
- Good quality
- Fast generation
- Already configured

**Z-Image via HuggingFace** (Better Quality)
- Requires free HuggingFace account
- Set `HUGGINGFACE_TOKEN` in `.env`
- Edit workflow to enable Z-Image

## 🛠️ Development

### Project Structure

```
Autotube/
├── short_automation/
│   ├── docker-compose.yml      # Service definitions
│   ├── .env.example            # Environment template
│   ├── workflows/              # n8n workflow files
│   │   └── autotube-complete.json
│   ├── scripts/                # Python automation
│   │   ├── ai_generator.py     # AI image generation
│   │   ├── create_video.py     # Video creation
│   │   └── video_api.py        # Flask API server
│   ├── videos/                 # Generated content (gitignored)
│   └── data/                   # Persistent data (gitignored)
├── START-ROBOT.bat             # Windows start script
├── STOP-ROBOT.bat              # Windows stop script
├── TEST-ALL.bat                # Service testing script
├── docs/                       # Documentation
└── README.md                   # This file
```

### Python API Endpoints

The Python video API runs on `http://localhost:5001`:

- `GET /health` - Health check
- `POST /generate` - Generate video
- `GET /info` - API information

**Example Request:**
```bash
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "hook": "Did you know?",
    "content": "Amazing facts here",
    "cta": "Follow for more!",
    "title": "Cool Video",
    "useAiImages": true
  }'
```

### Local Development

1. **Install Python dependencies**
   ```bash
   docker exec youtube-python pip install -r /scripts/requirements.txt
   ```

2. **Test video generation**
   ```bash
   docker exec youtube-python python /scripts/create_video.py
   ```

3. **View logs**
   ```bash
   docker-compose logs -f
   ```

## 🐛 Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# Restart all services
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs
```

### n8n won't connect
- Verify port 5678 is not in use
- Check `.env` file is configured correctly
- Wait 30 seconds after startup for initialization

### AI model not found
```bash
docker exec youtube-ai ollama pull llama3.1:8b
```

### Video generation fails
- Check Python container is running: `docker ps`
- Verify videos directory is writable
- Check logs: `docker logs youtube-python`

### More troubleshooting
See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for detailed solutions.

## 📚 Documentation

- [Architecture Overview](docs/ARCHITECTURE.md)
- [Detailed Setup Guide](docs/SETUP.md)
- [n8n Workflow Guide](docs/N8N_WORKFLOW.md)
- [Python API Documentation](docs/PYTHON_API.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **n8n** - Workflow automation platform
- **Ollama** - Local AI inference
- **Pollinations.ai** - Free AI image generation
- **OpenTTS** - Text-to-speech engine
- **MoviePy** - Video editing library
- **YouTube API** - Video publishing

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Hritikraj8804/Autotube/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Hritikraj8804/Autotube/discussions)

## 🗺️ Roadmap

- [ ] Support for multiple AI models (GPT-4, Claude, Gemini)
- [ ] Advanced video editing (effects, filters)
- [ ] Thumbnail generation
- [ ] Multi-language support
- [ ] Scheduled posting
- [ ] Analytics dashboard
- [ ] Music integration
- [ ] Custom brand templates

---

**Made with ❤️ by the AutoTube team**

*Star ⭐ this repo if you find it useful!*
