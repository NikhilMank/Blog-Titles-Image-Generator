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

# -------------------------------
# Load .env
# -------------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("❌ OpenAI API key not found! Please check your .env file.")
    st.stop()

client = openai.OpenAI(api_key=OPENAI_API_KEY)

# -------------------------------
# Configuration
# -------------------------------
OUTPUT_DIR = "generated_headers"
Path(OUTPUT_DIR).mkdir(exist_ok=True)

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

# -------------------------------
# Helper Functions
# -------------------------------
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

def create_zip_with_metadata(files, metadata):
    """Create a single ZIP containing all images and metadata.json"""
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, "w") as zip_file:
        # Add images to folder inside ZIP
        for fpath in files:
            zip_file.write(fpath, arcname=f"images/{Path(fpath).name}")
        # Add metadata.json
        zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))
    zip_buffer.seek(0)
    return zip_buffer

# -------------------------------
# Streamlit UI
# -------------------------------
st.title("AI Blog Header Generator")
st.markdown("Generate cohesive blog header images and download all images + metadata as a single ZIP.")

blog_titles_input = st.text_area(
    "Enter one blog title per line:",
    value="10 Tips for Effective Time Management\nThe Future of Artificial Intelligence",
    height=200
)

if st.button("Generate"):
    titles = [t.strip() for t in blog_titles_input.split("\n") if t.strip()]
    metadata_list = []
    generated_files = []

    progress_bar = st.progress(0)
    for i, title in enumerate(titles):

        prompt = generate_prompt(title)

        try:
            filename, _ = generate_image(title)
            generated_files.append(filename)

            st.image(filename, caption=title)

            metadata_list.append({
                "index": i + 1,
                "title": title,
                "status": "success",
                "filename": Path(filename).name,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            })

        except Exception as e:

            error_message = str(e)

            st.error(f"Error generating image '{title}': {error_message}")

            metadata_list.append({
                "index": i + 1,
                "title": title,
                "status": "error",
                "error": error_message,
                "prompt": prompt,
                "timestamp": datetime.now().isoformat()
            })

        time.sleep(1)
        progress_bar.progress((i + 1) / len(titles))

    zip_buffer = create_zip_with_metadata(generated_files, metadata_list)
    st.download_button(
        label="Download All Images + Metadata as ZIP",
        data=zip_buffer,
        file_name="blog_headers_with_metadata.zip",
        mime="application/zip"
    )

    st.success("All images generated and packaged in ZIP with metadata!")