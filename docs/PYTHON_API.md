# Python API Documentation

Complete reference for the AutoTube Python video generation API and supporting modules.

## Table of Contents

- [API Server](#api-server)
- [AI Image Generator](#ai-image-generator)
- [Video Creator](#video-creator)
- [API Examples](#api-examples)
- [Customization](#customization)

---

## API Server

### Overview

**File:** `scripts/video_api.py`  
**Framework:** Flask  
**Port:** 5001  
**Base URL:** `http://python:5001` (internal) or `http://localhost:5001` (from host)

### Endpoints

#### GET /health

Health check endpoint.

**Request:**
```bash
curl http://localhost:5001/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "autotube-video-api"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

#### GET /info

Get API information and capabilities.

**Request:**
```bash
curl http://localhost:5001/info
```

**Response:**
```json
{
  "service": "AutoTube Video Generation API",
  "version": "2.0.0",
  "features": [
    "AI Image Slideshows",
    "Crossfade Transitions",
    "Ken Burns Zoom"
  ],
  "endpoints": {
    "/health": "Health check",
    "/generate": "POST - Generate video",
    "/info": "Server info"
  }
}
```

---

#### POST /generate

Generate a YouTube Short video with AI images and effects.

**Request:**
```bash
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "hook": "Did you know this amazing fact?",
    "content": "Point 1: First key insight\nPoint 2: Second valuable tip\nPoint 3: Mind-blowing conclusion",
    "cta": "Follow for more tech tips! #ai #shorts #trending",
    "title": "Amazing AI Discovery",
    "audioPath": "/videos/audio_20231216_143052.wav",
    "outputPath": "/videos/short_20231216_143052.mp4",
    "useAiImages": true
  }'
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `hook` | string | Yes | Opening line (displayed first) |
| `content` | string | Yes | Main content (newline-separated points) |
| `cta` | string | Yes | Call to action (displayed last) |
| `title` | string | Yes | Video title (for metadata) |
| `audioPath` | string | No | Path to audio file (optional) |
| `outputPath` | string | No | Output video path (auto-generated if omitted) |
| `useAiImages` | boolean | No | Generate AI images (default: true) |

**Success Response (200 OK):**
```json
{
  "success": true,
  "videoPath": "/videos/short_20231216_143052.mp4",
  "fileSize": 2457600,
  "message": "Video created successfully: /videos/short_20231216_143052.mp4"
}
```

**Error Response (500):**
```json
{
  "success": false,
  "error": "Error message describing what went wrong",
  "traceback": "Full Python traceback for debugging"
}
```

**Error Response (400 - Bad Request):**
```json
{
  "error": "No JSON data provided"
}
```

---

## AI Image Generator

### Overview

**File:** `scripts/ai_generator.py`  
**Purpose:** Generate AI images for video slideshows

### Functions

#### generate_image_pollinations()

Generate image using Pollinations.ai (free, unlimited).

```python
def generate_image_pollinations(
    prompt: str, 
    output_path: str = None, 
    index: int = 0
) -> str:
    """
    Generate image using Pollinations.ai.
    
    Args:
        prompt: Text description for image
        output_path: Optional path to save image (auto-generated if None)
        index: Image index for default naming
        
    Returns:
        Path to generated image file, or None if failed
        
    Example:
        path = generate_image_pollinations(
            "futuristic AI dashboard, vibrant colors, professional",
            index=0
        )
    """
```

**Features:**
- Free and unlimited
- No API key required
- Fast generation (~2-5 seconds)
- 1080x1920 vertical images
- Flux model
- No watermark

**Endpoint Used:**
```
https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&model=flux&nologo=true
```

---

#### generate_image_zimage()

Generate image using Z-Image via HuggingFace (higher quality, requires token).

```python
def generate_image_zimage(
    prompt: str, 
    output_path: str = None, 
    index: int = 0,
    hf_token: str = None
) -> str:
    """
    Generate image using Z-Image via HuggingFace.
    
    Args:
        prompt: Text description for image
        output_path: Optional output path
        index: Image index
        hf_token: HuggingFace API token (reads from env if None)
        
    Returns:
        Path to generated image, or None if failed
        
    Example:
        path = generate_image_zimage(
            "professional tech workspace, cinematic lighting",
            hf_token="hf_your_token"
        )
    """
```

**Features:**
- Higher quality images
- Requires free HuggingFace account
- May have rate limits
- Handles model loading delays

**Endpoint:**
```
POST https://api-inference.huggingface.co/models/Tongyi-Kongjian/Z-Image
Authorization: Bearer {token}
```

---

#### generate_slideshow_images()

Generate multiple images for video slideshow.

```python
def generate_slideshow_images(
    prompts: list, 
    topic: str, 
    use_zimage: bool = False
) -> list:
    """
    Generate multiple AI images for slideshow video.
    
    Args:
        prompts: List of text prompts for each scene
        topic: Overall video topic (added to prompts)
        use_zimage: Use Z-Image instead of Pollinations
        
    Returns:
        List of image file paths
        
    Example:
        prompts = [
            "futuristic AI interface",
            "ChatGPT productivity workspace",
            "AI art generation showcase"
        ]
        images = generate_slideshow_images(
            prompts, 
            "Top AI Tools 2025",
            use_zimage=False
        )
        # Returns: ['/videos/scene_0_xxx.jpg', '/videos/scene_1_xxx.jpg', ...]
    """
```

**Behavior:**
- Enhances each prompt with topic and style keywords
- Adds: "professional, cinematic, vibrant colors, vertical 9:16 format"
- Falls back to previous image if generation fails
- Adds 1-second delay between requests to avoid rate limiting

---

#### create_image_prompts_from_script()

Auto-generate image prompts from script sections.

```python
def create_image_prompts_from_script(
    hook: str, 
    content: str, 
    cta: str, 
    topic: str
) -> list:
    """
    Generate image prompts based on script sections.
    
    Args:
        hook: Hook text
        content: Content text (newline-separated points)
        cta: Call to action text
        topic: Video topic
        
    Returns:
        List of prompts for each scene
        
    Example:
        prompts = create_image_prompts_from_script(
            hook="Did you know AI can do this?",
            content="1. Amazing feature\n2. Cool capability\n3. Mind-blowing result",
            cta="Follow for more!",
            topic="AI Tools 2025"
        )
        # Returns: [
        #   "attention-grabbing visual for: Did you know AI...",
        #   "illustrative visual for: 1. Amazing feature",
        #   "illustrative visual for: 2. Cool capability",
        #   ...
        # ]
    """
```

**Logic:**
1. Creates prompt for hook scene
2. Splits content by lines (max 3)
3. Creates prompt for each content point
4. Creates prompt for CTA scene
5. Returns 4-6 prompts total

---

## Video Creator

### Overview

**File:** `scripts/create_video.py`  
**Purpose:** Compile images, text, and audio into final video

### Constants

```python
WIDTH = 1080          # Video width (px)
HEIGHT = 1920         # Video height (px)
FPS = 30              # Frames per second
DURATION = 30         # Total video duration (seconds)
BG_COLOR = (15, 15, 25)  # Fallback background color (RGB)
```

### Functions

#### create_text_clip()

Create styled text overlay.

```python
def create_text_clip(
    text: str,
    fontsize: int = 60,
    color: str = 'white',
    duration: float = 5,
    position: str = 'center'
) -> TextClip:
    """
    Create a styled text clip with shadow.
    
    Args:
        text: Text to display
        fontsize: Font size in pixels
        color: Text color
        duration: Display duration in seconds
        position: Position ('center', 'top', 'bottom', etc.)
        
    Returns:
        MoviePy TextClip object
        
    Example:
        txt = create_text_clip(
            "Amazing Discovery!",
            fontsize=80,
            color='yellow',
            duration=3
        )
    """
```

**Features:**
- Bold font
- Black drop shadow for readability
- Word wrapping
- Auto-centered

---

#### create_image_scene()

Create video scene from image with effects.

```python
def create_image_scene(
    image_path: str,
    text: str,
    duration: float = 6,
    zoom: bool = True
) -> CompositeVideoClip:
    """
    Create a scene from an image with text overlay and zoom effect.
    
    Args:
        image_path: Path to image file
        text: Text to overlay on image
        duration: Scene duration in seconds
        zoom: Apply Ken Burns zoom effect
        
    Returns:
        CompositeVideoClip ready for concatenation
        
    Example:
        scene = create_image_scene(
            "/videos/scene_0.jpg",
            "Did you know this?",
            duration=5,
            zoom=True
        )
    """
```

**Effects Applied:**
- Resize to 1080x1920 (maintains aspect ratio)
- Ken Burns zoom: 1.0x → 1.1x scale over duration
- Text overlay with shadow
- Fade in/out for text

---

#### create_slideshow_video()

Compile multiple images into slideshow with transitions.

```python
def create_slideshow_video(
    images: list,
    texts: list,
    audio_path: str = None,
    output_path: str = "output.mp4",
    crossfade_duration: float = 0.5
) -> str:
    """
    Create slideshow video from images with crossfade transitions.
    
    Args:
        images: List of image file paths
        texts: List of text overlays for each image
        audio_path: Optional audio file path
        output_path: Where to save final video
        crossfade_duration: Transition duration in seconds
        
    Returns:
        Path to created video file
        
    Example:
        video = create_slideshow_video(
            images=['/videos/scene_0.jpg', '/videos/scene_1.jpg'],
            texts=['Opening line', 'Main point'],
            audio_path='/videos/audio.wav',
            output_path='/videos/final.mp4'
        )
    """
```

**Process:**
1. Calculate scene duration (auto-fit to total duration)
2. Create scene for each image with zoom effect
3. Apply crossfade transitions between scenes
4. Add audio track if provided
5. Export with optimized settings

**Export Settings:**
```python
codec='libx264'      # H.264 video codec
audio_codec='aac'    # AAC audio codec
fps=30               # 30 frames per second
preset='medium'      # Encoding speed/quality balance
threads=4            # Parallel encoding
```

---

#### create_youtube_short()

Main function to create complete YouTube Short.

```python
def create_youtube_short(
    hook: str,
    content: str,
    cta: str,
    title: str,
    audio_path: str = None,
    output_path: str = "output.mp4",
    use_ai_images: bool = True
) -> str:
    """
    Create YouTube Short with AI image slideshow.
    
    Args:
        hook: Hook text (0-6s)
        content: Content text, newline-separated points (6-24s)
        cta: Call to action text (24-30s)
       title: Video title
        audio_path: Optional audio file
        output_path: Output video path
        use_ai_images: Generate AI images vs placeholders
        
    Returns:
        Path to created video
        
    Example:
        video = create_youtube_short(
            hook="Did you know AI can...",
            content="1. Feature A\n2. Feature B\n3. Feature C",
            cta="Follow for more! #ai #shorts",
            title="Amazing AI Discovery",
            audio_path="/videos/audio.wav",
            use_ai_images=True
        )
    """
```

**Process:**
1. Create image prompts from script
2. Generate AI images (if enabled)
3. Create text overlays for each section
4. Compile slideshow with transitions
5. Add audio track
6. Export final video

**Scene Structure:**
```
Scene 1 (6s):  Hook + AI image
Scene 2 (6s):  Content Point 1 + AI image  
Scene 3 (6s):  Content Point 2 + AI image
Scene 4 (6s):  Content Point 3 + AI image
Scene 5 (6s):  CTA + AI image
```

---

## API Examples

### Basic Video Generation

```python
import requests

response = requests.post('http://localhost:5001/generate', json={
    "hook": "Want to boost your productivity?",
    "content": "1. Use AI assistants\n2. Automate repetitive tasks\n3. Learn keyboard shortcuts",
    "cta": "Follow for more productivity tips! #productivity #shorts",
    "title": "3 Productivity Hacks You Need",
    "useAiImages": True
})

result = response.json()
if result['success']:
    print(f"Video created: {result['videoPath']}")
    print(f"Size: {result['fileSize']} bytes")
else:
    print(f"Error: {result['error']}")
```

### With Custom Audio

```python
response = requests.post('http://localhost:5001/generate', json={
    "hook": "Check this out!",
    "content": "Amazing content here",
    "cta": "Subscribe now!",
    "title": "Cool Video",
    "audioPath": "/videos/my_custom_audio.wav",
    "outputPath": "/videos/my_custom_video.mp4"
})
```

### Without AI Images (Faster)

```python
response = requests.post('http://localhost:5001/generate', json={
    "hook": "Quick test",
    "content": "Test content",
    "cta": "End",
    "title": "Test Video",
    "useAiImages": False  # Uses solid color backgrounds
})
```

---

## Customization

### Change Video Specifications

Edit `create_video.py`:

```python
# Make horizontal videos
WIDTH = 1920
HEIGHT = 1080

# Change duration
DURATION = 60  # 60-second videos

# Change FPS
FPS = 60  # Smoother motion
```

### Add Background Music

Modify `create_slideshow_video()`:

```python
# After creating video
if audio_path:
    audio = AudioFileClip(audio_path)
    if music_path:
        music = AudioFileClip(music_path).volumex(0.2)  # 20% volume
        audio = CompositeAudioClip([audio, music])
    final_video = final_video.set_audio(audio)
```

### Custom Text Styles

Modify `create_text_clip()`:

```python
# Different font
font='Impact'

# Stroke outline instead of shadow
stroke_color='black'
stroke_width=2

# Gradient color (requires ImageClip manipulation)
```

### Add Filters/Effects

```python
from moviepy.video.fx import all as vfx

# Apply to scene
scene = scene.fx(vfx.colorx, 1.2)  # Increase brightness
scene = scene.fx(vfx.lum_contrast, lum=0, contrast=0.1)  # Add contrast
```

### Change Image Provider

Edit `ai_generator.py`:

```python
# Use a different API
CUSTOM_API_URL = "https://your-image-api.com/generate"

def generate_image_custom(prompt):
    response = requests.post(CUSTOM_API_URL, json={"prompt": prompt})
    # Handle response...
```

### Optimize Encoding

Edit export settings in `create_slideshow_video()`:

```python
# Faster encoding (larger files)
preset='ultrafast'

# Better quality (slower encoding)
preset='slow'
bitrate='8000k'

# Smaller files
preset='slow'
bitrate='2000k'
```

---

## Dependencies

### Required Python Packages

```
flask==3.0.0
moviepy==1.0.3
Pillow==10.1.0
requests==2.31.0
numpy==1.24.3
```

### Install in Container

```bash
docker exec youtube-python pip install -r /scripts/requirements.txt
```

---

## Testing

### Test Image Generation

```bash
docker exec youtube-python python /scripts/ai_generator.py
```

### Test Video Creation

```bash
docker exec youtube-python python /scripts/create_video.py
```

### Test API Server

```bash
# Start server (if not running)
docker exec youtube-python python /scripts/video_api.py

# In another terminal, test endpoint
curl http://localhost:5001/health
```

---

## Performance Tips

1. **Parallel Image Generation**: Generate all images simultaneously
2. **Cache Images**: Save generated images for reuse
3. **Optimize Resolution**: Lower resolution for faster processing
4. **Use SSD**: Store videos on SSD for faster I/O
5. **GPU Encoding**: Use GPU-accelerated encoding if available
6. **Limit Scene Count**: Fewer scenes = faster generation

---

## Next Steps

- **Customize** video effects and styles
- **Integrate** with new AI image providers
- **Add features** like music, filters, thumbnails
- **Optimize** for your specific use case

For more information:
- [n8n Workflow Guide](N8N_WORKFLOW.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
