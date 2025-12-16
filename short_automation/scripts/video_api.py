#!/usr/bin/env python3
"""
AutoTube Video Generation API Server
Simple Flask server for n8n to call for video generation
"""

from flask import Flask, request, jsonify
import os
import json
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, '/scripts')
from create_video import create_youtube_short

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "autotube-video-api"})

@app.route('/generate', methods=['POST'])
def generate_video():
    """
    Generate a YouTube Short video
    
    Expected JSON body:
    {
        "hook": "...",
        "content": "...",
        "cta": "...",
        "title": "...",
        "audioPath": "/videos/audio_xxx.wav" (optional),
        "outputPath": "/videos/short_xxx.mp4" (optional),
        "useAiImages": true (optional, default: true)
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Extract parameters
        hook = data.get('hook', 'Did you know this?')
        content = data.get('content', 'Amazing content here.')
        cta = data.get('cta', 'Follow for more!')
        title = data.get('title', 'Awesome Video')
        audio_path = data.get('audioPath', data.get('audio_path'))
        use_ai_images = data.get('useAiImages', data.get('use_ai_images', True))
        
        # Generate output path if not provided
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = data.get('outputPath', data.get('output_path', f'/videos/short_{timestamp}.mp4'))
        
        # Ensure output directory exists
        Path('/videos').mkdir(exist_ok=True)
        
        # Create the video
        result_path = create_youtube_short(
            hook=hook,
            content=content,
            cta=cta,
            title=title,
            audio_path=audio_path,
            output_path=output_path,
            use_ai_images=use_ai_images
        )
        
        # Check if video was created
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            return jsonify({
                "success": True,
                "videoPath": result_path,
                "fileSize": file_size,
                "message": f"Video created successfully: {result_path}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Video file was not created"
            }), 500
            
    except Exception as e:
        import traceback
        return jsonify({
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }), 500

@app.route('/info', methods=['GET'])
def info():
    """Get server info"""
    return jsonify({
        "service": "AutoTube Video Generation API",
        "version": "2.0.0",
        "features": ["AI Image Slideshows", "Crossfade Transitions", "Ken Burns Zoom"],
        "endpoints": {
            "/health": "Health check",
            "/generate": "POST - Generate video",
            "/info": "Server info"
        }
    })

if __name__ == '__main__':
    print("🎬 Starting AutoTube Video Generation API v2.0")
    print("   Features: AI Image Slideshows, Transitions, Zoom Effects")
    print("   Listening on http://0.0.0.0:5001")
    app.run(host='0.0.0.0', port=5001, debug=False)
