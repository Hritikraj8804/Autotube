# n8n Workflow Guide

Complete guide to understanding and customizing the AutoTube n8n workflow.

## Table of Contents

- [Workflow Overview](#workflow-overview)
- [Node-by-Node Breakdown](#node-by-node-breakdown)
- [Data Flow](#data-flow)
- [Customization Guide](#customization-guide)
- [Error Handling](#error-handling)
- [Advanced Usage](#advanced-usage)

## Workflow Overview

The AutoTube workflow automates the entire YouTube Shorts creation process from a simple topic input to a fully rendered video.

### Workflow Steps

```
Manual Trigger → Set Topic → AI Script → Parse Script → TTS → Save Audio → Video Generation → Final Output
```

### Execution Time

- **Average**: 2-5 minutes per video
- Script generation: 5-10s
- TTS: 10-20s
- Video creation: 1-3 minutes (depending on images)

### Required Credentials

1. **Groq API** (HTTP Bearer Auth)
   - Get free key: https://console.groq.com/keys
   - Used for both AI script generation and TTS

---

## Node-by-Node Breakdown

### 1. Manual Trigger

**Type:** `n8n-nodes-base.manualTrigger`  
**Purpose:** Start the workflow manually

**Configuration:**
- No special configuration needed
- Simply click "Test Workflow" to execute

**Alternative Triggers:**
```javascript
// Schedule trigger - Run daily at 9 AM
Cron: 0 9 * * *

// Webhook trigger - HTTP endpoint
Method: POST
Path: /autotube-create
```

---

### 2. Set Topic

**Type:** `n8n-nodes-base.set`  
**Purpose:** Define the video topic

**Configuration:**
```json
{
  "values": {
    "string": [
      {
        "name": "topic",
        "value": "5 AI tools that will change your life in 2025"
      }
    ]
  }
}
```

**Customization:**
```javascript
// You can add more fields
{
  "topic": "Your video topic",
  "style": "educational",  // educational, entertaining, motivational
  "duration": 30,          // seconds
  "targetAudience": "tech enthusiasts"
}
```

**Output:**
```json
{
  "topic": "5 AI tools that will change your life in 2025"
}
```

---

### 3. AI Script Writer

**Type:** `n8n-nodes-base.httpRequest`  
**Purpose:** Generate engaging video script using Groq AI (LLaMA 3.1)

**Configuration:**
- **Method:** POST
- **URL:** `https://api.groq.com/openai/v1/chat/completions`
- **Authentication:** HTTP Bearer (Groq API credential)

**Request Body:**
```json
{
  "model": "llama-3.1-8b-instant",
  "messages": [
    {
      "role": "system",
      "content": "You are a viral YouTube Shorts script writer..."
    },
    {
      "role": "user",
      "content": "Create an engaging 30-second script about: {{ $json.topic }}"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 1024
}
```

**Prompt Engineering:**

The prompt instructs AI to format response as:
```
HOOK (0-3 seconds):
[Attention-grabbing opening]

CONTENT (3-25 seconds):
[3-4 key points]

CTA (25-30 seconds):
[Call to action + hashtags]

TITLE:
[Catchy YouTube title under 60 characters]

DESCRIPTION:
[Short description with hashtags]
```

**Customization Tips:**

Change `temperature` for creativity:
- `0.3` - More consistent, factual
- `0.7` - Balanced (default)
- `0.9` - More creative, varied

Modify system prompt:
```javascript
"You are a viral YouTube Shorts script writer specializing in [YOUR NICHE]. Focus on [STYLE]."
```

**Output Example:**
```json
{
  "choices": [{
    "message": {
      "content": "HOOK (0-3 seconds):\nDid you know AI can now create entire videos?\n\nCONTENT (3-25 seconds):\n..."
    }
  }]
}
```

---

### 4. Parse Script

**Type:** `n8n-nodes-base.code`  
**Purpose:** Extract structured data from AI response

**JavaScript Code:**
```javascript
const choices = $input.first().json.choices;
const response = choices && choices[0] && choices[0].message 
  ? choices[0].message.content : '';

// Extract sections using regex
const hookMatch = response.match(/HOOK[^:]*:\s*([\s\S]*?)(?=CONTENT|$)/i);
const contentMatch = response.match(/CONTENT[^:]*:\s*([\s\S]*?)(?=CTA|$)/i);
const ctaMatch = response.match(/CTA[^:]*:\s*([\s\S]*?)(?=TITLE|$)/i);
const titleMatch = response.match(/TITLE[^:]*:\s*([\s\S]*?)(?=DESCRIPTION|$)/i);
const descMatch = response.match(/DESCRIPTION[^:]*:\s*([\s\S]*?)$/i);

// Clean text helper
const cleanText = (text) => text 
  ? text.trim().replace(/\[.*?\]/g, '').trim() 
  : '';

// Extract and clean
const hook = hookMatch ? cleanText(hookMatch[1]) : 'Did you know this?';
const content = contentMatch ? cleanText(contentMatch[1]) : 'Amazing content here.';
const cta = ctaMatch ? cleanText(ctaMatch[1]) : 'Follow for more!';
let title = titleMatch ? cleanText(titleMatch[1]) : $('Set Topic').first().json.topic;
let description = descMatch ? cleanText(descMatch[1]) : `${title} #shorts`;

// Ensure #shorts tag
if (!title.includes('#shorts')) {
  title = title.substring(0, 90) + ' #shorts';
}

return [{
  json: {
    topic: $('Set Topic').first().json.topic,
    hook: hook,
    content: content,
    cta: cta,
    title: title.substring(0, 100),
    description: description.substring(0, 500),
    fullScript: `${hook}\n\n${content}\n\n${cta}`,
    tags: ['shorts', 'viral', 'trending', 'ai']
  }
}];
```

**Output:**
```json
{
  "topic": "5 AI tools...",
  "hook": "Did you know...",
  "content": "Point 1\nPoint 2\nPoint 3",
  "cta": "Follow for more tips!",
  "title": "5 AI Tools That Will Blow Your Mind #shorts",
  "description": "Check out these amazing AI tools... #ai #shorts #tech",
  "fullScript": "Did you know...\n\nPoint 1...",
  "tags": ["shorts", "viral", "trending", "ai"]
}
```

---

### 5. Text to Speech

**Type:** `n8n-nodes-base.httpRequest`  
**Purpose:** Convert script to audio using Groq's PlayAI TTS

**Configuration:**
- **Method:** POST
- **URL:** `https://api.groq.com/openai/v1/audio/speech`
- **Response Format:** File

**Request Body:**
```json
{
  "model": "playai-tts",
  "input": "{{ JSON.stringify($json.fullScript) }}",
  "voice": "Fritz-PlayAI",
  "response_format": "wav"
}
```

**Available Voices:**
- `Fritz-PlayAI` - Male, energetic (default)
- `Bella-PlayAI` - Female, friendly
- `Andrew-PlayAI` - Male, professional
- `Sarah-PlayAI` - Female, warm

**Customization:**

Change voice:
```json
{
  "voice": "Bella-PlayAI"
}
```

**Output:**
Binary audio file (WAV format)

---

### 6. Save Audio File

**Type:** `n8n-nodes-base.readWriteFile`  
**Purpose:** Save audio to disk for video creation

**Configuration:**
```json
{
  "operation": "write",
  "fileName": "/videos/audio_{{ $now.format('yyyyMMdd_HHmmss') }}.wav",
  "dataPropertyName": "data"
}
```

**File Naming:**
```
audio_%Y%m%d_%H%M%S.wav
Example: audio_20231216_143052.wav
```

**Output:**
```json
{
  "fileName": "/videos/audio_20231216_143052.wav"
}
```

---

### 7. Generate Video

**Type:** `n8n-nodes-base.httpRequest`  
**Purpose:** Call Python API to create video with AI images

**Configuration:**
- **Method:** POST
- **URL:** `http://python:5001/generate`
- **Timeout:** 300000ms (5 minutes)

**Request Body:**
```json
{
  "hook": "{{ JSON.stringify($('Parse Script').first().json.hook) }}",
  "content": "{{ JSON.stringify($('Parse Script').first().json.content) }}",
  "cta": "{{ JSON.stringify($('Parse Script').first().json.cta) }}",
  "title": "{{ JSON.stringify($('Parse Script').first().json.title) }}",
  "audioPath": "{{ JSON.stringify($('Save Audio File').first().json.fileName) }}",
  "outputPath": "/videos/short_{{ $now.format('yyyyMMdd_HHmmss') }}.mp4",
  "useAiImages": true
}
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `hook` | string | Opening line (0-6s) |
| `content` | string | Main content (6-24s) |
| `cta` | string | Call to action (24-30s) |
| `title` | string | Video title (for metadata) |
| `audioPath` | string | Path to audio file |
| `outputPath` | string | Where to save video |
| `useAiImages` | boolean | Generate AI images (true) or use placeholders (false) |

**Output:**
```json
{
  "success": true,
  "videoPath": "/videos/short_20231216_143052.mp4",
  "fileSize": 2457600,
  "message": "Video created successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Error message here",
  "traceback": "..."
}
```

---

### 8. Final Output

**Type:** `n8n-nodes-base.set`  
**Purpose:** Format final success message

**Configuration:**
```json
{
  "status": "✅ Video Created Successfully!\n\n📝 Topic: ...\n🎬 Title: ...",
  "videoFile": "{{ $json.videoPath }}",
  "videoTitle": "{{ $('Parse Script').first().json.title }}",
  "videoDescription": "{{ $('Parse Script').first().json.description }}"
}
```

**Output:**
```json
{
  "status": "✅ Video Created Successfully!...",
  "videoFile": "/videos/short_xxx.mp4",
  "videoTitle": "Amazing Title #shorts",
  "videoDescription": "Description with #hashtags"
}
```

---

## Data Flow

### Complete Data Journey

```
1. INPUT
   { topic: "5 AI Tools" }

2. AI SCRIPT GENERATION
   → API Call to Groq
   → Response: Raw script text

3. PARSING
   → Extract: hook, content, cta, title, description
   → Format: Structured JSON

4. AUDIO GENERATION
   → fullScript → Groq TTS API
   → Response: WAV audio file

5. SAVE AUDIO
   → Write to /videos/audio_xxx.wav
   → Return: file path

6. VIDEO CREATION
   → Python API receives:
     - Script components
     - Audio path
   → Generates:
     - AI images (4-6 per video)
     - Video with effects
     - Text overlays
   → Returns: video path

7. OUTPUT
   → Success message with paths
```

---

## Customization Guide

### Change Video Style

Modify the AI Script Writer system prompt:

```javascript
// Educational style
"You are an educational content creator. Focus on clear explanations and valuable insights."

// Entertainment style
"You are a viral content creator. Focus on humor, surprise, and entertainment."

// Motivational style
"You are a motivational speaker. Focus on inspiration and empowerment."
```

### Add Custom Fields

In **Set Topic** node:
```json
{
  "topic": "Your topic",
  "niche": "technology",
  "mood": "upbeat",
  "keywords": ["AI", "automation", "future"]
}
```

Then modify AI prompt to use these:
```javascript
`Create a ${$json.mood} script about ${$json.topic} in the ${$json.niche} niche, focusing on: ${$json.keywords.join(', ')}`
```

### Change Video Duration

Currently hardcoded to 30 seconds. To change, modify:

1. AI prompt: Change second allocations
2. Python `create_video.py`: Modify `DURATION` constant

### Disable AI Images

In **Generate Video** node:
```json
{
  "useAiImages": false  // Uses fallback placeholders
}
```

### Add YouTube Upload

Add after **Final Output**:

1. **Read Binary File** node
   - Path: `{{ $('Final Output').first().json.videoFile }}`

2. **YouTube Upload** node (requires YouTube credential)
   - Title: `{{ $('Final Output').first().json.videoTitle }}`
   - Description: `{{ $('Final Output').first().json.videoDescription }}`
   - File: From previous node

---

## Error Handling

### Built-in Error Handling

n8n automatically:
- Retries failed HTTP requests (3x)
- Shows error details in UI
- Stops execution on failure
- Preserves execution history

### Add Custom Error Handling

Add **Error Trigger** node:

```javascript
// In Error Trigger node
// Send notification on failure
{
  "message": `Workflow failed at ${$json.node}`,
  "error": $json.error.message,
  "executionId": $executionId
}
```

### Common Errors

**Timeout:**
```
Solutions:
- Increase timeout in node settings
- Check Python container is running
- Verify network connectivity
```

**Authentication Failed:**
```
Solutions:
- Verify Groq API key is correct
- Check credential name matches
- Regenerate API key if expired
```

**File Not Found:**
```
Solutions:
- Check volumes are mounted correctly
- Verify paths use /videos not ./videos
- Restart containers
```

---

## Advanced Usage

### Schedule Automatic Posting

Replace **Manual Trigger** with **Cron** node:

```javascript
// Daily at 9 AM
0 9 * * *

// Every 4 hours
0 */4 * * *

// Monday, Wednesday, Friday at 2 PM
0 14 * * 1,3,5
```

### Create Topic Queue

1. Add **Airtable/Google Sheets** node
2. Read topics from database
3. Loop through each topic
4. Create videos for all

### A/B Testing

Create two branches:
- Branch A: One AI model/voice
- Branch B: Different model/voice
- Compare performance

### Add Music

Modify Python API call:
```json
{
  "audioPath": "/videos/audio_xxx.wav",
  "backgroundMusic": "/videos/music/upbeat.mp3",
  "musicVolume": 0.2
}
```

(Requires modifying `create_video.py` to support music)

---

## Best Practices

1. **Test Individually**: Test each node before running full workflow
2. **Use Variables**: Store reusable values in Set nodes
3. **Add Descriptions**: Document complex nodes
4. **Version Control**: Export and backup workflows regularly
5. **Monitor Executions**: Check execution history for failures
6. **Optimize Timeouts**: Set appropriate timeouts for each node
7. **Handle Errors**: Add error workflows for notifications

---

## Workflow Export/Import

### Export Workflow

1. Open workflow in n8n
2. Click ... (three dots) → Download
3. Save JSON file

### Import Workflow

1. Go to Workflows → Import from File
2. Select JSON file
3. Activate workflow

### Share Workflow

The workflow JSON is in:
```
short_automation/workflows/autotube-complete.json
```

---

## Next Steps

- **Customize** the workflow for your niche
- **Add nodes** for scheduling or uploading
- **Integrate** with other services
- **Monitor** execution history
- **Optimize** for performance

For more help, see:
- [Python API Documentation](PYTHON_API.md)
- [Troubleshooting Guide](TROUBLESHOOTING.md)
- [Architecture Overview](ARCHITECTURE.md)
