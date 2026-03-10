"""
    A Streamlit app to generate AI-powered blog header images based on a defined brand style system
    and a list of blog titles. The app uses OpenAI's image generation capabilities to create cohesive 
    illustrations that visually represent the essence of each blog topic while adhering to a consistent
    visual language. Users can input their blog titles, generate images, and download them along with
    metadata about the generation process.
"""



import streamlit as st
from pathlib import Path
import base64
import time
import json
import re
from datetime import datetime
import openai
from zipfile import ZipFile
import io
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# ----------------------------------------------------
# Configuration
# ----------------------------------------------------
# Get your OpenAI API key from .env 
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

OUTPUT_DIR = "generated_headers"
METADATA_FILE = "generation_metadata.json"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

# ----------------------------------------------------
# Brand Style
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
# Helper Functions
# ----------------------------------------------------
def build_style_prompt():
    return f"""
Art style: {BRAND_STYLE['art_style']}
Visual identity: {BRAND_STYLE['visual_identity']}
Color palette: {BRAND_STYLE['color_palette']}
Mood: {BRAND_STYLE['mood']}
Composition: {BRAND_STYLE['composition']}
"""

def extract_topic_essence(title):
    topic_map = {
        "time management": "clock, calendar, productivity symbols",
        "artificial intelligence": "neural network, AI brain, futuristic circuits",
        "python": "python programming, code snippets, learning programming",
        "sustainable living": "green leaves, earth, eco friendly lifestyle",
        "digital marketing": "analytics dashboards, marketing megaphone, social media icons",
        "web applications": "browser window, cloud infrastructure, servers and APIs",
        "healthy eating": "fresh vegetables, balanced healthy meal",
        "remote work": "laptop workspace, home office environment",
        "blockchain": "interconnected blocks, decentralized network",
        "creative writing": "open notebook, pen, imagination symbols"
    }
    title_lower = title.lower()
    for key, value in topic_map.items():
        if key in title_lower:
            return value
    return "abstract representation of the article topic"

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
• 16:9 aspect ratio
• minimal design
• clean background
• no text in image
"""
    return prompt

def sanitize_filename(title):
    safe = re.sub(r"[^a-zA-Z0-9_ ]", "", title)
    safe = safe.replace(" ", "_")
    return safe[:40]

def generate_image(title):
    prompt = generate_prompt(title)
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    image_base64 = response.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)
    filename = f"{OUTPUT_DIR}/header_{sanitize_filename(title)}.png"
    with open(filename, "wb") as f:
        f.write(image_bytes)
    return filename, prompt

def create_zip(files):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        for fpath in files:
            zip_file.write(fpath, arcname=Path(fpath).name)
    zip_buffer.seek(0)
    return zip_buffer

def save_metadata(metadata_list):
    """Save metadata to JSON file"""
    metadata_path = Path(OUTPUT_DIR) / METADATA_FILE
    with open(metadata_path, "w") as f:
        json.dump({
            "brand_style": BRAND_STYLE,
            "generated_at": datetime.now().isoformat(),
            "images": metadata_list
        }, f, indent=2)
    return metadata_path

# ----------------------------------------------------
# Streamlit UI
# ----------------------------------------------------
st.title("AI Blog Header Generator")
st.markdown("Generate **cohesive header images** for your blog titles and download them all as a ZIP or metadata JSON.")

blog_titles_input = st.text_area(
    "Enter one blog title per line:",
    value="10 Tips for Effective Time Management\nThe Future of Artificial Intelligence",
    height=200
)

if st.button("Generate Headers"):
    titles = [t.strip() for t in blog_titles_input.split("\n") if t.strip()]
    metadata = []
    generated_files = []

    progress_bar = st.progress(0)
    for i, title in enumerate(titles):
        try:
            filename, prompt = generate_image(title)
            generated_files.append(filename)
            st.image(filename, caption=title)
            metadata.append({
                "index": i + 1,
                "title": title,
                "filename": filename,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            })
            time.sleep(1)  # rate-limit safety
            progress_bar.progress((i + 1) / len(titles))
        except Exception as e:
            st.error(f"Error generating image '{title}': {e}")

    # Save metadata file
    metadata_path = save_metadata(metadata)

    # ZIP download button
    zip_buffer = create_zip(generated_files)
    st.download_button(
        label="Download All Images as ZIP",
        data=zip_buffer,
        file_name="blog_headers.zip",
        mime="application/zip"
    )

    # Metadata download button
    with open(metadata_path, "rb") as f:
        metadata_bytes = f.read()
    st.download_button(
        label="Download Metadata JSON",
        data=metadata_bytes,
        file_name=METADATA_FILE,
        mime="application/json"
    )

    st.success("All images generated, metadata saved, and ZIP ready!")