# AI Blog Header Generator

Automatically generates 10 coherent, brand-consistent header images for blog titles using OpenAI's DALL-E API.

## 🎨 How Coherence is Achieved

### 1. **Style DNA System (BRAND_STYLE)**
Every image shares the same foundational style prompt defined in the BRAND_STYLE dictionary:
- **Art Style**: Digital illustration, flat design with subtle gradients, vector-style
- **Visual Identity**: Modern minimalist design, clean geometric shapes, professional tech aesthetic
- **Color Palette**: Deep navy blue, vibrant cyan, warm coral accents, lots of white space
- **Mood**: Innovative, trustworthy, forward-thinking
- **Composition**: Centered composition, balanced negative space, subtle depth

### 2. **Style Anchor System**
A dedicated STYLE_ANCHOR constant reinforces series coherence:
```
This image is part of a cohesive blog header illustration series.
All images must share the same visual language, color palette,
composition style and illustration technique.
Clean modern design suitable for a professional technology blog.
```

### 3. **Smart Prompt Engineering**
Each prompt = `Topic Visual Concept + Brand Style DNA + Style Anchor + Technical Requirements`

Example for "The Future of Artificial Intelligence":
```
Blog header illustration for the article:

"The Future of Artificial Intelligence"

Visual concept:
neural networks, AI brain, futuristic tech, circuit patterns, machine learning symbols, robotic elements

Design system:
Art style: digital illustration, flat design with subtle gradients, vector-style
Visual identity: modern minimalist design, clean geometric shapes, professional tech aesthetic
Color palette: deep navy blue, vibrant cyan, warm coral accents, lots of white space
Mood: innovative, trustworthy, forward-thinking
Composition: centered composition, balanced negative space, subtle depth

Series requirement:
This image is part of a cohesive blog header illustration series.
All images must share the same visual language, color palette,
composition style and illustration technique.
Clean modern design suitable for a professional technology blog.

Technical requirements:
• modern blog header illustration
• 16:9 aspect ratio
• minimal design
• clean background
• no text in image
```

### 4. **Intelligent Topic Mapping**
The extract_topic_essence function maps blog titles to relevant visual concepts:
- "Artificial Intelligence" → neural networks, AI brain, futuristic tech, circuit patterns, machine learning symbols, robotic elements
- "Python" → python logo, code snippets, programming, learning symbols, computer screen
- "Blockchain" → connected blocks, chain network, cryptography, decentralized symbols, digital ledger icons
- And 7 more mappings for consistent topic representation

### 5. **Metadata Tracking**
All prompts and generation details are logged to generation_metadata.json for reproducibility and refinement.

## 🚀 Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
# Windows
set OPENAI_API_KEY=sk-your-key-here

# Linux/Mac
export OPENAI_API_KEY=sk-your-key-here
```
or create a .env file (copy from .env.example)

3. Run the generator:
```bash
python generate_headers.py
```

## ⚙️ Technical Implementation

- **Model**: gpt-image-1 (OpenAI's image generation model - DALL-E)
- **Image Size**: 1792x1024 (16:9 aspect ratio)
- **Response Format**: Base64 encoded images
- **Rate Limiting**: 1 second delay between generations
- **Error Handling**: Graceful failure with error logging in metadata

## 📁 Output

- `generated_headers/` - Contains all 10 PNG images
- `generation_metadata.json` - Full generation details for each image

## 💡 Customization

### Brand Style
Edit the `BRAND_STYLE` dictionary in `generate_headers.py` to match your brand:
```python
BRAND_STYLE = {
    "visual_identity": "your visual style here",
    "color_palette": "your brand colors",
    "mood": "your desired mood",
    "composition": "your composition preferences",
    "art_style": "your art style"
}
```

### Style Anchor
Modify `STYLE_ANCHOR` to adjust the coherence instructions given to the AI.

### Topic Mapping
Expand the `topic_map` dictionary in extract_topic_essence to add custom visual concepts for your specific blog topics.

### Blog Titles
Edit the `BLOG_TITLES` list to generate images for your actual blog posts.

## 💰 Cost Estimation

**gpt-image-1 model pricing (1792x1024):**
- Standard quality: ~$0.08 per image → **$0.80 for 10 images**
- HD quality: ~$0.12 per image → **$1.20 for 10 images**

Note: Pricing may vary. Check [OpenAI Pricing](https://openai.com/api/pricing/) for current rates.
