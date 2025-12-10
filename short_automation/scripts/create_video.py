#!/usr/bin/env python3
"""
AutoTube - YouTube Shorts Video Creator (MoviePy 2.x compatible)
Creates vertical 9:16 videos with text overlays
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# MoviePy 2.x imports
from moviepy import TextClip, ColorClip, CompositeVideoClip, AudioFileClip

# Video specifications for YouTube Shorts
WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION = 30  # seconds
BG_COLOR = (15, 15, 25)  # Dark blue-black background


def create_text_clip(text, fontsize=60, color='white', duration=5, position='center'):
    """Create a styled text clip"""
    # Wrap long text
    max_chars = 25
    lines = []
    words = text.split()
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) <= max_chars:
            current_line = (current_line + " " + word).strip()
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    
    wrapped_text = '\n'.join(lines)
    
    try:
        txt_clip = TextClip(
            text=wrapped_text,
            font_size=fontsize,
            color=color,
            font='Arial',
            stroke_color='black',
            stroke_width=2,
            text_align='center',
            size=(WIDTH - 100, None)
        )
        return txt_clip.with_position(position).with_duration(duration)
    except Exception as e:
        print(f"Error creating text clip: {e}")
        # Simple fallback
        txt_clip = TextClip(
            text=wrapped_text,
            font_size=fontsize,
            color=color
        )
        return txt_clip.with_position(position).with_duration(duration)


def create_youtube_short(
    hook: str,
    content: str,
    cta: str,
    title: str,
    audio_path: str = None,
    output_path: str = "output.mp4",
    duration: int = DURATION
):
    """
    Create a YouTube Short video
    """
    print(f"🎬 Creating YouTube Short: {title}")
    print(f"   Duration: {duration}s, Resolution: {WIDTH}x{HEIGHT}")
    
    clips = []
    
    # 1. Background
    bg = ColorClip(size=(WIDTH, HEIGHT), color=BG_COLOR).with_duration(duration)
    clips.append(bg)
    
    # 2. Title at top
    title_clip = create_text_clip(
        title[:40],
        fontsize=45,
        color='gold',
        duration=duration,
        position=('center', 120)
    )
    clips.append(title_clip)
    
    # 3. Hook (0-5 seconds)
    hook_clip = create_text_clip(
        hook,
        fontsize=65,
        color='#00FF88',
        duration=5,
        position='center'
    ).with_start(0)
    clips.append(hook_clip)
    
    # 4. Content (5-22 seconds)
    content_parts = [p.strip() for p in content.split('\n') if p.strip()][:4]
    if content_parts:
        content_duration = 17 / len(content_parts)
        for i, part in enumerate(content_parts):
            part_clip = create_text_clip(
                part,
                fontsize=50,
                color='white',
                duration=content_duration,
                position='center'
            ).with_start(5 + (i * content_duration))
            clips.append(part_clip)
    
    # 5. CTA (22-30 seconds)
    cta_clip = create_text_clip(
        cta,
        fontsize=60,
        color='#FF6B6B',
        duration=8,
        position='center'
    ).with_start(22)
    clips.append(cta_clip)
    
    # 6. Follow watermark
    follow_clip = create_text_clip(
        "FOLLOW FOR MORE",
        fontsize=35,
        color='white',
        duration=duration,
        position=('center', HEIGHT - 200)
    )
    clips.append(follow_clip)
    
    # 7. Compose
    print("   Compositing...")
    video = CompositeVideoClip(clips, size=(WIDTH, HEIGHT))
    
    # 8. Add audio if available
    if audio_path and os.path.exists(audio_path):
        print(f"   Adding audio: {audio_path}")
        try:
            audio = AudioFileClip(audio_path)
            if audio.duration > duration:
                audio = audio.subclipped(0, duration)
            video = video.with_audio(audio)
        except Exception as e:
            print(f"   Audio error: {e}")
    
    # 9. Export
    print(f"   Rendering: {output_path}")
    video.write_videofile(
        output_path,
        fps=FPS,
        codec='libx264',
        audio_codec='aac',
        threads=4,
        preset='medium',
        logger=None
    )
    
    video.close()
    print(f"✅ Video created: {output_path}")
    return output_path


def main():
    """Main function"""
    # Test content
    test_data = {
        "hook": "Did you know AI can create videos automatically?",
        "content": "Step 1: AI writes the script\nStep 2: Text-to-speech creates voice\nStep 3: MoviePy makes the video\nStep 4: Auto-upload to YouTube!",
        "cta": "Follow for more AI tips!\n#shorts #ai #automation",
        "title": "AI Creates Videos Automatically!"
    }
    
    # Check for JSON input
    if len(sys.argv) > 1:
        try:
            test_data = json.loads(sys.argv[1])
        except:
            test_data["hook"] = sys.argv[1]
    
    # Output path
    output_dir = Path("/videos")
    output_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = str(output_dir / f"short_{timestamp}.mp4")
    
    # Audio path (optional)
    audio_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create video
    result = create_youtube_short(
        hook=test_data.get("hook", "Amazing fact!"),
        content=test_data.get("content", "Great content here."),
        cta=test_data.get("cta", "Follow for more!"),
        title=test_data.get("title", "Awesome Video"),
        audio_path=audio_path,
        output_path=output_path
    )
    
    print(f"\n📁 Output: {result}")
    return result


if __name__ == "__main__":
    main()