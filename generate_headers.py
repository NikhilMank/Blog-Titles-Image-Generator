import openai
import requests
import json
import os
from datetime import datetime
from pathlib import Path

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-api-key-here')
OUTPUT_DIR = 'generated_headers'
METADATA_FILE = 'generation_metadata.json'

# Brand Identity - This is our "Style DNA"
BRAND_STYLE = {
    'visual_identity': 'modern minimalist design, clean geometric shapes, professional tech aesthetic',
    'color_palette': 'deep navy blue, vibrant cyan, warm coral accents, white space',
    'mood': 'innovative, trustworthy, forward-thinking',
    'composition': 'centered composition, balanced negative space, subtle depth',
    'art_style': 'digital illustration, flat design with subtle gradients, vector-style'
}

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

def build_style_prompt():
    """
    Creates the consistent style foundation for all images
    """
    return (f"{BRAND_STYLE['art_style']}, {BRAND_STYLE['visual_identity']}, "
            f"color scheme: {BRAND_STYLE['color_palette']}, "
            f"mood: {BRAND_STYLE['mood']}, {BRAND_STYLE['composition']}")

def extract_topic_essence(title):
    """
    Extracts key visual concepts from blog title
    """
    topic_map = {
        'time management': 'clock, calendar, productivity symbols',
        'artificial intelligence': 'neural networks, AI brain, futuristic tech, circuit patterns',
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
    for key, visual in topic_map.items():
        if key in title_lower:
            return visual
    return 'abstract concept visualization'

def generate_coherent_prompt(title, index):
    """
    Combines brand style + topic + coherence elements
    """
    style_base = build_style_prompt()
    topic_visual = extract_topic_essence(title)
    
    # Coherence instruction to ensure all images feel like part of a series
    coherence = "part of a cohesive blog header series, consistent visual language"
    
    prompt = (f"Blog header image: {topic_visual}. "
              f"{style_base}. {coherence}. "
              f"Professional website banner, 16:9 aspect ratio, no text overlay")
    
    return prompt

def generate_image(title, index):
    """
    Generates single image using DALL-E
    """
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    prompt = generate_coherent_prompt(title, index)
    
    print(f"\n[{index+1}/10] Generating: {title}")
    print(f"Prompt: {prompt[:100]}...")
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        n=1
    )
    
    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt
    
    # Download image
    img_data = requests.get(image_url).content
    filename = f"{OUTPUT_DIR}/header_{index+1:02d}_{title[:30].replace(' ', '_').replace(':', '')}.png"
    
    with open(filename, 'wb') as f:
        f.write(img_data)
    
    print(f"✓ Saved: {filename}")
    
    return {
        'index': index + 1,
        'title': title,
        'original_prompt': prompt,
        'revised_prompt': revised_prompt,
        'filename': filename,
        'url': image_url,
        'timestamp': datetime.now().isoformat()
    }

def save_metadata(metadata_list):
    """
    Saves generation details for reproducibility
    """
    with open(f"{OUTPUT_DIR}/{METADATA_FILE}", 'w') as f:
        json.dump({
            'brand_style': BRAND_STYLE,
            'generation_date': datetime.now().isoformat(),
            'images': metadata_list
        }, f, indent=2)
    print(f"\n✓ Metadata saved to {OUTPUT_DIR}/{METADATA_FILE}")

def main():
    # Initial Setup
    Path(OUTPUT_DIR).mkdir(exist_ok=True)
    
    print("=" * 60)
    print("AI-Powered Blog Header Generator")
    print("=" * 60)
    print(f"\nBrand Style DNA:")
    for key, value in BRAND_STYLE.items():
        print(f"  • {key}: {value}")
    
    print(f"\n\nGenerating {len(BLOG_TITLES)} coherent header images...")
    
    # Generate all images
    metadata_list = []
    for i, title in enumerate(BLOG_TITLES):
        try:
            metadata = generate_image(title, i)
            metadata_list.append(metadata)
        except Exception as e:
            print(f"✗ Error generating image {i+1}: {e}")
            metadata_list.append({
                'index': i + 1,
                'title': title,
                'error': str(e)
            })
    
    # Saves metadata
    save_metadata(metadata_list)
    
    print("\n" + "=" * 60)
    print(f"✓ Complete! {len(metadata_list)} images generated")
    print(f"✓ All files saved to '{OUTPUT_DIR}/' directory")
    print("=" * 60)

if __name__ == "__main__":
    main()
