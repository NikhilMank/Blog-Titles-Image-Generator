# AI Blog Header Generator

Automatically generates 10 coherent, brand-consistent header images for blog titles using OpenAI's DALL-E API.

## 🎨 How Coherence is Achieved

### 1. **Style DNA System**
Every image shares the same foundational style prompt:
- **Art Style**: Digital illustration, flat design with subtle gradients
- **Color Palette**: Deep navy blue, vibrant cyan, warm coral accents
- **Mood**: Innovative, trustworthy, forward-thinking
- **Composition**: Centered, balanced negative space

### 2. **Smart Prompt Engineering**
Each prompt = `Brand Style DNA + Topic Essence + Coherence Instruction`

Example for "The Future of AI":
```
Blog header image: neural networks, AI brain, futuristic tech. 
modern minimalist design, clean geometric shapes, professional tech aesthetic, 
color scheme: deep navy blue, vibrant cyan, warm coral accents, white space, 
mood: innovative, trustworthy, forward-thinking, centered composition, 
balanced negative space, subtle depth, digital illustration, flat design with 
subtle gradients, vector-style. part of a cohesive blog header series, 
consistent visual language. Professional website banner, 16:9 aspect ratio, 
no text overlay
```

### 3. **Topic Mapping**
Intelligent extraction of visual concepts from titles ensures relevant imagery while maintaining style consistency.

### 4. **Metadata Tracking**
All prompts, revisions, and generation details are logged for reproducibility and refinement.

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

Or create a `.env` file (copy from `.env.example`)

3. Run the generator:
```bash
python generate_headers.py
```

## 📁 Output

- `generated_headers/` - Contains all 10 PNG images
- `generation_metadata.json` - Full generation details for each image

## 💡 Customization

Edit the `BRAND_STYLE` dictionary in `generate_headers.py` to match your brand:
- Change colors, mood, art style
- Modify composition preferences
- Adjust visual identity

Edit `BLOG_TITLES` list to generate images for your actual blog posts.

## 💰 Cost Estimate

DALL-E 3 Standard: ~$0.04 per image × 10 = **$0.40 per run**
