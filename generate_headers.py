""" A script to generate AI-powered blog header images based on a defined brand style system
    and a list of blog titles. The script uses OpenAI's image generation capabilities to 
    create cohesive illustrations that visually represent the essence of each blog topic while
    adhering to a consistent visual language. Metadata about the generation process is saved
    for future reference and analysis.
"""

import openai
import requests
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OUTPUT_DIR = "generated_headers"
METADATA_FILE = "generation_metadata.json"

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# ----------------------------------------------------
# Brand Style System (Style DNA)
# ----------------------------------------------------

BRAND_STYLE = {
    "visual_identity": "modern minimalist design, clean geometric shapes, professional tech aesthetic",
    "color_palette": "deep navy blue, vibrant cyan, warm coral accents, lots of white space",
    "mood": "innovative, trustworthy, forward-thinking",
    "composition": "centered composition, balanced negative space, subtle depth",
    "art_style": "digital illustration, flat design with subtle gradients, vector-style"
}

STYLE_ANCHOR = """
This image is part of a cohesive blog header illustration series.
All images must share the same visual language, color palette,
composition style and illustration technique.
Clean modern design suitable for a professional technology blog.
"""

# ----------------------------------------------------
# Blog Titles
# ----------------------------------------------------

BLOG_TITLES = [
    "10 Tips for Effective Time Management",
    "The Future of Artificial Intelligence",
    "Mastering Python in 30 Days",
    "Sustainable Living: A Beginner's Guide",
    "The Art of Digital Marketing",
    "Building Scalable Web Applications",
    "Healthy Eating on a Budget",
    "Remote Work Best Practices",
    "Understanding Blockchain Technology",
    "Creative Writing Techniques"
]

# ----------------------------------------------------
# Style Prompt Builder
# ----------------------------------------------------

def build_style_prompt():
    return f"""
Art style: {BRAND_STYLE['art_style']}
Visual identity: {BRAND_STYLE['visual_identity']}
Color palette: {BRAND_STYLE['color_palette']}
Mood: {BRAND_STYLE['mood']}
Composition: {BRAND_STYLE['composition']}
"""


# ----------------------------------------------------
# Topic Extraction
# ----------------------------------------------------

def extract_topic_essence(title):

    topic_map = {
        'time management': 'clock, calendar, productivity symbols',
        'artificial intelligence': 'neural networks, AI brain, futuristic tech, circuit patterns, machine learning symbols, robotic elements',
        'python': 'python logo, code snippets, programming, learning symbols, computer screen',
        'sustainable living': 'green leaves, earth, eco-friendly symbols, recycling icons, renewable energy',
        'digital marketing': 'social media icons, analytics graphs, megaphone, digital ads, online engagement symbols',
        'web applications': 'browser windows, cloud architecture, servers, code snippets, scalable infrastructure, network diagrams',
        'healthy eating': 'fresh vegetables, balanced meal, nutrition, healthy lifestyle symbols, food icons',
        'remote work': 'laptop, home office, video call interface, digital nomad symbols, flexible workspace icons',
        'blockchain': 'connected blocks, chain network, cryptography, decentralized symbols, digital ledger icons',
        'creative writing': 'pen, paper, imagination symbols, storytelling, creative flow icons, literary motifs, typewriter, open book'
    }

    title_lower = title.lower()

    for key, value in topic_map.items():
        if key in title_lower:
            return value

    return "abstract representation of the article topic"


# ----------------------------------------------------
# Prompt Generator
# ----------------------------------------------------

def generate_prompt(title):

    topic_visual = extract_topic_essence(title)

    prompt = f"""
Blog header illustration for the article:

"{title}"

Visual concept:
{topic_visual}

Design system:
{build_style_prompt()}

Series requirement:
{STYLE_ANCHOR}

Technical requirements:
• modern blog header illustration
• minimal design
• clean background
• no text in image
"""

    return prompt


# ----------------------------------------------------
# Filename Generator
# ----------------------------------------------------

def generate_filename(title):

    name = re.sub(r"[^a-zA-Z0-9_ ]", "", title)
    name = name.replace(" ", "_")

    return name[:40]


# ----------------------------------------------------
# Image Generation
# ----------------------------------------------------

def generate_image(title, index):

    prompt = generate_prompt(title)

    print(f"\n[{index+1}/10] Generating: {title}")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = response.data[0].b64_json

    import base64
    image_bytes = base64.b64decode(image_base64)

    filename = f"{OUTPUT_DIR}/header_{index+1:02d}_{generate_filename(title)}.png"

    with open(filename, "wb") as f:
        f.write(image_bytes)

    print(f"✓ Saved: {filename}")

    return {
        "index": index + 1,
        "title": title,
        "prompt": prompt,
        "filename": filename,
        "timestamp": datetime.now().isoformat()
    }


# ----------------------------------------------------
# Metadata
# ----------------------------------------------------

def save_metadata(metadata_list):

    with open(f"{OUTPUT_DIR}/{METADATA_FILE}", "w") as f:

        json.dump(
            {
                "brand_style": BRAND_STYLE,
                "generated_at": datetime.now().isoformat(),
                "images": metadata_list
            },
            f,
            indent=2
        )

    print(f"\n✓ Metadata saved to {OUTPUT_DIR}/{METADATA_FILE}")


# ----------------------------------------------------
# Main Pipeline
# ----------------------------------------------------

def main():

    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    print("=" * 60)
    print("AI Blog Header Generator")
    print("=" * 60)

    print("\nBrand Style System\n")

    for k, v in BRAND_STYLE.items():
        print(f"{k}: {v}")

    print(f"\nGenerating {len(BLOG_TITLES)} images...\n")

    metadata = []

    for i, title in enumerate(BLOG_TITLES):

        try:

            result = generate_image(title, i)
            metadata.append(result)

            # Rate limit safety
            time.sleep(1)

        except Exception as e:

            print(f"Error generating image {i+1}: {e}")

            metadata.append({
                "title": title,
                "error": str(e)
            })

    save_metadata(metadata)

    print("\nGeneration complete!")
    print(f"Images saved to: {OUTPUT_DIR}")


# ----------------------------------------------------

if __name__ == "__main__":
    main()