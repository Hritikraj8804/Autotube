#!/usr/bin/env python3
"""
AI Media Generator for AutoTube
Generates multiple images for slideshow videos using various AI APIs
"""

import os
import requests
import time
from pathlib import Path
from datetime import datetime

# Image generation endpoints
POLLINATIONS_URL = "https://image.pollinations.ai/prompt/{prompt}?width=1080&height=1920&model=flux&nologo=true"
Z_IMAGE_HF_URL = "https://api-inference.huggingface.co/models/Tongyi-Kongjian/Z-Image"

def generate_image_pollinations(prompt: str, output_path: str = None, index: int = 0) -> str:
    """Generate image using Pollinations.ai (free, unlimited)"""
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/videos/scene_{index}_{timestamp}.jpg"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Clean prompt
        clean_prompt = prompt.replace('\n', ' ').strip()
        url = POLLINATIONS_URL.format(prompt=requests.utils.quote(clean_prompt))
        
        print(f"🎨 Generating image {index + 1}: {clean_prompt[:50]}...")
        
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Image {index + 1} saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Image {index + 1} generation failed: {e}")
        return None


def generate_image_zimage(prompt: str, output_path: str = None, index: int = 0, hf_token: str = None) -> str:
    """Generate image using Z-Image via HuggingFace (best quality)"""
    if not hf_token:
        hf_token = os.getenv('HUGGINGFACE_TOKEN')
    
    try:
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"/videos/scene_{index}_{timestamp}.jpg"
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        headers = {"Authorization": f"Bearer {hf_token}"} if hf_token else {}
        
        print(f"🎨 Generating Z-Image {index + 1}: {prompt[:50]}...")
        
        response = requests.post(
            Z_IMAGE_HF_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=120
        )
        
        # Handle model loading
        if response.status_code == 503:
            result = response.json()
            if 'estimated_time' in result:
                wait_time = result['estimated_time']
                print(f"⏳ Model loading, waiting {wait_time}s...")
                time.sleep(wait_time + 5)
                response = requests.post(Z_IMAGE_HF_URL, headers=headers, json={"inputs": prompt}, timeout=120)
        
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Z-Image {index + 1} saved: {output_path}")
        return output_path
        
    except Exception as e:
        print(f"❌ Z-Image {index + 1} generation failed: {e}")
        return None


def generate_slideshow_images(prompts: list, topic: str, use_zimage: bool = False) -> list:
    """
    Generate multiple AI images for slideshow video
    
    Args:
        prompts: List of text prompts for each scene
        topic: Overall video topic
        use_zimage: Use Z-Image instead of Pollinations (requires HF token)
        
    Returns:
        List of image file paths
    """
    images = []
    generator = generate_image_zimage if use_zimage else generate_image_pollinations
    
    for i, prompt in enumerate(prompts):
        # Enhance prompt with topic and style
        enhanced_prompt = f"{topic}, {prompt}, professional, cinematic, vibrant colors, high quality, vertical 9:16 format"
        
        image_path = generator(enhanced_prompt, index=i)
        
        if image_path:
            images.append(image_path)
        else:
            # Fallback: create placeholder or use previous image
            print(f"⚠️ Using fallback for image {i + 1}")
            if images:  # Use last successful image as fallback
                images.append(images[-1])
        
        # Small delay to avoid rate limiting
        time.sleep(1)
    
    return images


def create_image_prompts_from_script(hook: str, content: str, cta: str, topic: str) -> list:
    """
    Generate image prompts based on script sections
    
    Returns:
        List of prompts for each scene
    """
    prompts = []
    
    # Hook scene
    prompts.append(f"attention-grabbing visual for: {hook[:100]}")
    
    # Content scenes (split into parts)
    content_parts = [p.strip() for p in content.split('\n') if p.strip()][:3]
    for part in content_parts:
        prompts.append(f"illustrative visual for: {part[:100]}")
    
    # CTA scene
    prompts.append(f"engaging call-to-action visual with: {cta[:100]}")
    
    return prompts


if __name__ == "__main__":
    # Test multi-image generation
    test_topic = "AI Tools for 2025"
    test_prompts = [
        "futuristic AI interface dashboard",
        "ChatGPT productivity workspace",
        "AI art generation showcase",
        "subscribe and follow visual"
    ]
    
    print("Testing multi-image generation...")
    images = generate_slideshow_images(test_prompts, test_topic, use_zimage=False)
    print(f"\n✅ Generated {len(images)} images:")
    for img in images:
        print(f"  - {img}")
