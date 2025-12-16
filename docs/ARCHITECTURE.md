# AutoTube Architecture

This document provides a detailed overview of the AutoTube system architecture, components, and data flow.

## System Overview

AutoTube is a microservices-based architecture designed for automated YouTube Shorts creation. It uses Docker containers to orchestrate multiple specialized services that work together to generate videos from simple text topics.

## Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────┐
│                         AutoTube System                                │
│                                                                        │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │                     n8n Workflow Engine                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │  │
│  │  │ Trigger  │→ │ AI Script│→ │   TTS    │→ │  Video   │       │  │
│  │  │          │  │ Generate │  │ Generate │  │ Compose  │       │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│         ↓              ↓              ↓              ↓                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐          │
│  │PostgreSQL│   │  Ollama  │   │ OpenTTS  │   │  Python  │          │
│  │          │   │  LLaMA   │   │   Voice  │   │ Video API│          │
│  │  Storage │   │    AI    │   │  Engine  │   │          │          │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘          │
│                        ↓                            ↓                  │
│                 ┌──────────┐              ┌──────────────┐           │
│                 │  Redis   │              │ AI Image Gen │           │
│                 │  Cache   │              │ Pollinations │           │
│                 └──────────┘              └──────────────┘           │
│                                                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    Shared Volumes                             │   │
│  │  ./videos  │  ./scripts  │  ./data  │  ./workflows           │   │
│  └──────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. n8n Workflow Engine
**Container:** `youtube-automation`  
**Port:** 5678  
**Purpose:** Orchestration and automation hub

The brain of AutoTube. n8n provides:
- Visual workflow design
- Node-based automation
- Error handling and retry logic
- Webhook support
- Credential management
- Execution history

**Key Features:**
- Triggers manual or scheduled video creation
- Coordinates all services
- Handles data transformation between nodes
- Manages API calls to external services (Groq AI)
- Persists workflow state

### 2. Ollama AI Engine
**Container:** `youtube-ai`  
**Port:** 11434  
**Purpose:** Local AI inference for script generation

Runs large language models locally:
- **Model:** LLaMA 3.1 8B (optimized for speed and quality)
- **Usage:** Generate engaging YouTube Shorts scripts
- **Benefits:** Free, private, fast, no API limits

**API Endpoint:**
```
POST http://localhost:11434/api/generate
```

### 3. OpenTTS Server
**Container:** `youtube-tts`  
**Port:** 5500  
**Purpose:** Text-to-speech voice generation

Converts script text to natural voiceovers:
- Multiple voice options
- High-quality speech synthesis
- WAV format output
- No usage limits

**Supported Voices:**
- Multiple languages
- Various accents
- Male/female options

### 4. Python Video API
**Container:** `youtube-python`  
**Port:** 5001  
**Purpose:** Video creation and AI image generation

Custom Flask API that handles:

**Modules:**
- `ai_generator.py` - AI image generation via Pollinations.ai/Z-Image
- `create_video.py` - Video compilation with MoviePy
- `video_api.py` - REST API endpoints

**Key Features:**
- Generate multiple AI images per video
- Apply Ken Burns zoom effects
- Crossfade transitions between scenes
- Text overlay rendering
- Audio synchronization
- Video encoding optimization

**Dependencies:**
- MoviePy - Video editing
- Pillow - Image processing
- Requests - API calls
- Flask - Web server

### 5. PostgreSQL Database
**Container:** `youtube-db`  
**Port:** 5432 (internal)  
**Purpose:** n8n data persistence

Stores:
- Workflow definitions
- Execution history
- Credentials (encrypted)
- User settings
- Node configurations

**Data Persistence:**
Volume mounted at `./data/postgres`

### 6. Redis Cache
**Container:** `youtube-cache`  
**Port:** 6379 (internal)  
**Purpose:** Caching and session management

Used for:
- Workflow execution queuing
- Rate limit tracking
- Temporary data storage
- Performance optimization

### 7. FileBrowser
**Container:** `youtube-files`  
**Port:** 8080  
**Purpose:** File management UI

Web-based file manager for:
- Viewing generated videos
- Downloading audio files
- Managing assets
- Uploading resources
- Browsing logs

## Data Flow

### Complete Video Creation Flow

```
1. USER TRIGGER
   ↓
2. n8n: Set Topic
   Topic: "5 AI Tools for 2025"
   ↓
3. n8n → Groq API: Generate Script
   Request: "Create engaging script about: {topic}"
   Response: {hook, content, cta, title, description}
   ↓
4. n8n: Parse Script
   Extract and structure script components
   ↓
5. n8n → Groq TTS: Generate Audio
   Input: Full script text
   Output: audio_20231216_194530.wav
   ↓
6. n8n: Save Audio File
   Path: /videos/audio_20231216_194530.wav
   ↓
7. n8n → Python API: Generate Video
   POST /generate
   {
     hook: "Did you know...",
     content: "Point 1\nPoint 2\nPoint 3",
     cta: "Follow for more!",
     audioPath: "/videos/audio_xxx.wav",
     useAiImages: true
   }
   ↓
8. Python API:
   a. Parse script sections
   b. Generate image prompts
   c. Call Pollinations.ai for each image
   d. Download and save images
   e. Create video clips with zoom effects
   f. Add text overlays
   g. Apply crossfade transitions
   h. Sync with audio
   i. Export final video
   ↓
9. Python API Response:
   {
     success: true,
     videoPath: "/videos/short_20231216_194530.mp4",
     fileSize: 2457600
   }
   ↓
10. n8n: Final Output
    Display success message with video details
```

## Network Architecture

All containers run on a custom Docker network: `automation-network`

**Internal DNS:**
- `n8n` - n8n service
- `ollama` - AI service
- `tts` - Text-to-speech
- `python` - Python API
- `postgres` - Database
- `redis` - Cache
- `filebrowser` - File manager

**External Ports:**
- 5678 → n8n web UI
- 11434 → Ollama API
- 5500 → OpenTTS API
- 8080 → FileBrowser UI

## Storage Architecture

### Volume Mounts

```yaml
volumes:
  # n8n data
  ./data/n8n:/home/node/.n8n
  
  # Ollama models
  ./data/ollama:/root/.ollama
  
  # OpenTTS data
  ./data/tts:/root/.local/share/opentts
  
  # PostgreSQL database
  ./data/postgres:/var/lib/postgresql/data
  
  # Redis data
  ./data/redis:/data
  
  # Shared volumes
  ./videos:/videos          # Generated media
  ./scripts:/scripts        # Python code
  ./templates:/templates    # Video templates
  ./assets:/assets         # Static assets
```

### File Organization

```
short_automation/
├── data/               # Persistent service data (gitignored)
│   ├── n8n/           # Workflows, credentials, database
│   ├── ollama/        # AI models (large files)
│   ├── tts/           # TTS models and cache
│   ├── postgres/      # Database files
│   └── redis/         # Cache data
├── videos/            # Generated content (gitignored)
│   ├── short_*.mp4    # Final videos
│   ├── audio_*.wav    # Voice files
│   └── scene_*.jpg    # AI images
├── scripts/           # Python source code
│   ├── ai_generator.py
│   ├── create_video.py
│   └── video_api.py
└── workflows/         # n8n workflow exports
    └── autotube-complete.json
```

## Security Architecture

### Authentication

1. **n8n**: Basic authentication via environment variables
2. **FileBrowser**: Default admin/admin (should be changed)
3. **Internal services**: No authentication (internal network only)

### Secrets Management

- **Environment Variables**: Stored in `.env` (gitignored)
- **n8n Credentials**: Encrypted in PostgreSQL
- **Google OAuth**: Separate JSON file (gitignored)

### Network Security

- Internal Docker network isolates services
- Only necessary ports exposed to host
- No external database access
- Redis not externally accessible

## API Interfaces

### Python Video API

**Base URL:** `http://python:5001` (internal) or `http://localhost:5001` (from host)

**Endpoints:**

```
GET /health
Response: {"status": "healthy", "service": "autotube-video-api"}

GET /info
Response: {
  "service": "AutoTube Video Generation API",
  "version": "2.0.0",
  "features": ["AI Image Slideshows", "Transitions", "Zoom"]
}

POST /generate
Request: {
  "hook": "Opening line",
  "content": "Main content",
  "cta": "Call to action",
  "title": "Video title",
  "audioPath": "/videos/audio_xxx.wav",
  "outputPath": "/videos/short_xxx.mp4",
  "useAiImages": true
}
Response: {
  "success": true,
  "videoPath": "/videos/short_xxx.mp4",
  "fileSize": 2457600
}
```

### AI Image Generation

**Pollinations.ai:**
```
GET https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&model=flux&nologo=true
```

**Z-Image (HuggingFace):**
```
POST https://api-inference.huggingface.co/models/Tongyi-Kongjian/Z-Image
Headers: { "Authorization": "Bearer {token}" }
Body: { "inputs": "{prompt}" }
```

## Scalability Considerations

### Current Limitations

- Single container per service
- Local file storage
- Synchronous processing
- No load balancing

### Scaling Options

1. **Horizontal Scaling:**
   - Multiple Python workers
   - n8n queue mode
   - Shared Redis cache

2. **Storage Scaling:**
   - NFS/S3 for videos
   - Separate database server
   - CDN for distribution

3. **Processing Optimization:**
   - GPU support for AI generation
   - Parallel image generation
   - Video encoding optimization
   - Caching frequently used assets

## Monitoring and Debugging

### Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f python

# n8n execution logs
# Available in n8n UI at http://localhost:5678
```

### Health Checks

```bash
# n8n
curl http://localhost:5678

# Python API
curl http://localhost:5001/health

# Ollama
curl http://localhost:11434/api/tags

# OpenTTS
curl http://localhost:5500/api/voices
```

### Resource Monitoring

```bash
# Container stats
docker stats

# Disk usage
docker system df
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Orchestration | n8n | Workflow automation |
| AI - LLM | Ollama + LLaMA 3.1 | Script generation |
| AI - Images | Pollinations.ai / Z-Image | Image generation |
| TTS | OpenTTS | Voice synthesis |
| Video | Python + MoviePy | Video editing |
| API | Flask | REST endpoints |
| Database | PostgreSQL | Data persistence |
| Cache | Redis | Performance |
| File Manager | FileBrowser | UI for files |
| Container | Docker + Compose | Deployment |

## Design Decisions

### Why Docker?
- Consistent environment across platforms
- Easy installation and updates
- Service isolation
- Resource management
- Portable deployment

### Why n8n?
- Visual workflow design
- Extensive integrations
- Self-hosted option
- Active community
- Easy customization

### Why Local AI (Ollama)?
- No API costs
- Complete privacy
- No rate limits
- Fast response times
- Offline capability

### Why Python for Video?
- Rich library ecosystem (MoviePy)
- Easy integration
- Flexible and powerful
- Great for media processing
- Wide community support

## Future Architecture Enhancements

1. **Microservice Separation:**
   - Dedicated image generation service
   - Separate audio processing service
   - Independent upload service

2. **Message Queue:**
   - RabbitMQ or Apache Kafka
   - Async job processing
   - Better scalability

3. **API Gateway:**
   - Single entry point
   - Rate limiting
   - Authentication layer

4. **Cloud Integration:**
   - S3 for storage
   - CloudFront for CDN
   - ECS/EKS for hosting

5. **Monitoring Stack:**
   - Prometheus for metrics
   - Grafana for visualization
   - ELK for log aggregation
