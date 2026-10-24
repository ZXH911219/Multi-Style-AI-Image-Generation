"""Multi-Style AI Image Generator - Streamlit Web App."""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import random
from PIL import Image, ImageDraw
import io
import requests

# Page configuration
st.set_page_config(
    page_title="Multi-Style AI Image Generator",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main { max-width: 1200px; margin: 0 auto; }
    .feature-box {
        background-color: #e8f4f8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# Art style definitions
STYLES = {
    "realistic": {
        "name": "Realistic",
        "description": "Photography and realistic rendering",
        "color": "#FF6B6B"
    },
    "anime_2d": {
        "name": "Anime 2D",
        "description": "Japanese anime and manga style",
        "color": "#4ECDC4"
    },
    "fantasy_art": {
        "name": "Fantasy Art",
        "description": "Fantasy and magical style",
        "color": "#95E1D3"
    },
    "3d_rendering": {
        "name": "3D Rendering",
        "description": "3D CGI and rendered style",
        "color": "#F38181"
    },
    "oil_painting": {
        "name": "Oil Painting",
        "description": "Oil painting and artistic style",
        "color": "#AA96DA"
    }
}

HF_MODEL = "runwayml/stable-diffusion-v1-5"
HF_ENDPOINT = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"
STYLE_PROMPTS = {
    "realistic": "photorealistic, natural lighting, highly detailed",
    "anime_2d": "2D anime illustration, expressive, vibrant colors, clean line art",
    "fantasy_art": "fantasy concept art, magical atmosphere, cinematic lighting",
    "3d_rendering": "high-quality 3D render, detailed materials, studio lighting",
    "oil_painting": "oil painting, visible brush strokes, rich artistic texture"
}


def generate_ai_image(style_key, prompt, width, height, quality, guidance):
    """Generate an image through the Hugging Face Inference API."""
    try:
        token = st.secrets.get("HF_TOKEN")
    except Exception:
        token = None

    if not token:
        raise RuntimeError(
            "HF_TOKEN is not configured. Add it in Streamlit Cloud: "
            "Manage app > Settings > Secrets."
        )

    steps = {"Fast": 20, "Standard": 30, "High": 40}[quality]
    styled_prompt = f"{prompt}, {STYLE_PROMPTS[style_key]}"
    payload = {
        "inputs": styled_prompt,
        "parameters": {
            "width": width,
            "height": height,
            "num_inference_steps": steps,
            "guidance_scale": guidance,
            "negative_prompt": "blurry, low quality, distorted, malformed"
        }
    }

    response = requests.post(
        HF_ENDPOINT,
        headers={"Authorization": f"Bearer {token}"},
        json=payload,
        timeout=180
    )
    content_type = response.headers.get("content-type", "")
    if response.ok and content_type.startswith("image/"):
        return Image.open(io.BytesIO(response.content)).convert("RGB")

    try:
        error_details = response.json().get("error", response.text)
    except ValueError:
        error_details = response.text
    raise RuntimeError(
        f"Hugging Face API failed ({response.status_code}): {error_details}"
    )

def create_demo_image(style_key, prompt, width=512, height=512):
    """Create a demo image based on style"""
    style_info = STYLES[style_key]
    
    # Create base image with gradient
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Create style-specific colored background
    colors = {
        "realistic": [(100, 150, 200), (150, 180, 220)],
        "anime_2d": [(200, 220, 255), (240, 200, 255)],
        "fantasy_art": [(180, 200, 255), (220, 180, 220)],
        "3d_rendering": [(150, 150, 200), (200, 150, 150)],
        "oil_painting": [(200, 150, 100), (255, 200, 150)]
    }
    
    color_pair = colors.get(style_key, [(100, 100, 100), (200, 200, 200)])
    
    # Draw gradient
    for y in range(height):
        r = int(color_pair[0][0] + (color_pair[1][0] - color_pair[0][0]) * y / height)
        g = int(color_pair[0][1] + (color_pair[1][1] - color_pair[0][1]) * y / height)
        b = int(color_pair[0][2] + (color_pair[1][2] - color_pair[0][2]) * y / height)
        draw.rectangle([(0, y), (width, y+1)], fill=(r, g, b))
    
    # Add style indicator
    style_text = f"[{style_info['name']}]"
    draw.text((20, 20), style_text, fill=(255, 255, 255))
    
    # Add prompt text
    prompt_text = prompt[:50] + "..." if len(prompt) > 50 else prompt
    draw.text((20, height - 60), prompt_text, fill=(255, 255, 255))
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((20, height - 40), timestamp, fill=(255, 255, 255))
    
    return img

# Initialize session state
if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

# Header
st.markdown("# Multi-Style AI Image Generator")
st.markdown("### Web Interface for AI Image Generation")
st.markdown("---")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Setup & Parameters")
    
    prompt = st.text_area(
        "Enter prompt (Chinese or English)",
        placeholder="Example: A beautiful forest with sunlight...",
        height=100,
        help="Describe the image you want to generate"
    )
    
    st.markdown("### Art Styles")
    style_cols = st.columns(3)
    
    style_descriptions = {
        "realistic": "Photography\nBest for: Landscapes, portraits",
        "anime_2d": "Anime\nBest for: Characters, scenes",
        "fantasy_art": "Fantasy\nBest for: Magic, creatures",
        "3d_rendering": "3D CGI\nBest for: Architecture, products",
        "oil_painting": "Painting\nBest for: Landscapes, artistic"
    }
    
    col_idx = 0
    for style_key, style_info in STYLES.items():
        with style_cols[col_idx % 3]:
            st.markdown(f"**{style_info['name']}**")
            st.markdown(style_descriptions[style_key])
        col_idx += 1
    
    style = st.radio(
        "Select Art Style",
        options=list(STYLES.keys()),
        format_func=lambda x: STYLES[x]['name'],
        horizontal=True,
        help="Choose the art style for generation"
    )

with col2:
    st.markdown("## Advanced Settings")
    
    num_images = st.slider(
        "Number of Images",
        min_value=1,
        max_value=4,
        value=1,
        help="How many images to generate"
    )
    
    image_quality = st.selectbox(
        "Quality Level",
        options=["Fast", "Standard", "High"],
        help="Affects generation time"
    )
    
    image_size = st.selectbox(
        "Image Size",
        options=["512x512", "768x768"],
        help="Larger = slower but better detail"
    )
    
    guidance = st.slider(
        "Guidance Strength",
        min_value=1.0,
        max_value=15.0,
        value=7.5,
        step=0.5,
        help="How much to follow the prompt"
    )

# Info boxes
st.markdown("---")
with st.expander("Performance Information", expanded=False):
    col_perf1, col_perf2, col_perf3 = st.columns(3)
    
    with col_perf1:
        st.markdown("""
        **Fast**
        - Size: 512x512
        - Quality: Medium
        - Time: 10-20 sec
        """)
    
    with col_perf2:
        st.markdown("""
        **Standard**
        - Size: 512x512
        - Quality: Good
        - Time: 30-50 sec
        """)
    
    with col_perf3:
        st.markdown("""
        **High Quality**
        - Size: 768x768
        - Quality: Excellent
        - Time: 50-100 sec
        """)

# Generation section
st.markdown("---")
st.markdown("## Generate Images")

col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    generate_btn = st.button(
        "Generate Images",
        key="generate",
        use_container_width=True,
        help="Start generating images"
    )

with col_btn2:
    demo_btn = st.button(
        "Demo Mode",
        key="demo",
        use_container_width=True,
        help="View style examples"
    )

with col_btn3:
    test_btn = st.button(
        "Test Generation",
        key="test",
        use_container_width=True,
        help="Test with sample image"
    )

with col_btn4:
    reset_btn = st.button(
        "Reset",
        key="reset",
        use_container_width=True,
        help="Clear everything"
    )

# Handle button actions
if generate_btn:
    if not prompt:
        st.warning("Please enter a prompt first")
    else:
        st.info(f"Generating {num_images} image(s) with Hugging Face AI in {STYLES[style]['name']} style...")
        size_map = {"512x512": (512, 512), "768x768": (768, 768)}
        width, height = size_map[image_size]
        
        with st.spinner(f"Generating {num_images} image(s)..."):
            cols = st.columns(min(num_images, 2))
            
            try:
                for idx in range(num_images):
                    img = generate_ai_image(style, prompt, width, height, image_quality, guidance)
                    with cols[idx % len(cols)]:
                        st.image(img, caption=f"Image {idx+1} ({STYLES[style]['name']})")
            except RuntimeError as error:
                st.error(str(error))
            else:
                record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "prompt": prompt,
                    "style": STYLES[style]['name'],
                    "num_images": num_images,
                    "quality": image_quality,
                    "size": image_size,
                    "status": "Hugging Face API"
                }
                st.session_state.generation_history.append(record)
                st.success("AI images generated successfully!")

if demo_btn:
    st.info("Demo Mode - 5 Art Styles Showcase")
    
    st.markdown("### Art Styles Overview")
    
    demos = [
        {
            "key": "realistic",
            "prompt": "A beautiful mountain landscape with sunlight",
            "tips": "Best for: Landscapes, architecture, products"
        },
        {
            "key": "anime_2d",
            "prompt": "A magic girl in a battle pose with sparkles",
            "tips": "Best for: Characters, scenes, illustrations"
        },
        {
            "key": "fantasy_art",
            "prompt": "A mysterious dragon flying through clouds",
            "tips": "Best for: Magic, creatures, fantasy scenes"
        },
        {
            "key": "3d_rendering",
            "prompt": "A futuristic city with tall buildings",
            "tips": "Best for: Architecture, products, tech"
        },
        {
            "key": "oil_painting",
            "prompt": "A sunflower field under beautiful sunlight",
            "tips": "Best for: Landscapes, artistic, decorative"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        style_info = STYLES[demo['key']]
        with st.expander(f"{i}. {style_info['name']} - {style_info['description']}", expanded=(i==1)):
            st.markdown(f"**{demo['tips']}**")
            st.code(demo['prompt'], language="text")
            
            # Show demo image
            img = create_demo_image(demo['key'], demo['prompt'])
            st.image(img, caption=f"Example: {style_info['name']}")
            
            st.markdown("""
            **Generation Time Estimates:**
            - Fast (512x512): 10-20 seconds
            - Standard (512x512): 30-50 seconds
            - High Quality (768x768): 50-100 seconds
            """)
    
    st.success("""
    Demo Complete! Now you can:
    1. Enter your own prompt above
    2. Select a style
    3. Click "Generate Images"
    
    This demo shows placeholder images. Enable real AI generation by installing dependencies.
    """)

if test_btn:
    st.info("Test Generation - Creating sample images...")
    
    test_prompts = [
        "A serene lake at sunset",
        "An enchanted forest",
        "A modern city skyline",
        "A field of wildflowers"
    ]
    
    cols = st.columns(2)
    
    for idx, test_prompt in enumerate(test_prompts[:4]):
        with cols[idx % 2]:
            img = create_demo_image(style, test_prompt, 512, 512)
            st.image(img, caption=test_prompt)
    
    st.success("Test generation complete!")

if reset_btn:
    st.session_state.generation_history = []
    st.rerun()

# Sidebar
st.sidebar.markdown("# Control Panel")

# System Status
st.sidebar.markdown("## Status")

st.sidebar.success("""
Streamlit App is Running

Version: 1.0.0
Location: c:\\Users\\user\\Desktop\\HW4
""")

st.sidebar.info("""
**AI Generation Active**

Generation uses the Hugging Face Inference API.

Required Streamlit secret: `HF_TOKEN`
""")

# Instructions
with st.sidebar.expander("Setup Instructions", expanded=True):
    st.markdown("""
    **Current Status:** Hugging Face Inference API
    
    **Configure the API:**
    
    1. Create a Hugging Face access token with inference permissions.
    
    2. In Streamlit Cloud, open Manage app > Settings > Secrets.
    
    3. Add `HF_TOKEN = "hf_your_token"` and save.
    
    4. Reboot the app and generate an image.
    """)

# FAQ
with st.sidebar.expander("Frequently Asked Questions"):
    st.markdown("""
    **Q: Why are these placeholder images?**
    A: This demo version works without GPU/extra packages. Install dependencies for real generation.
    
    **Q: How to install dependencies?**
    A: Run: `pip install -r requirements.txt`
    
    **Q: Why download models?**
    A: AI models are 5-50 GB. Only needed once.
    
    **Q: Can I use CPU?**
    A: Yes, but it's slow (1-2 min per image). GPU is recommended.
    
    **Q: What languages are supported?**
    A: Chinese and English prompts work best.
    """)

# Generation History
st.sidebar.markdown("---")
st.sidebar.markdown("## Generation History")

if st.session_state.generation_history:
    st.sidebar.info(f"Total generations: {len(st.session_state.generation_history)}")
    
    for i, record in enumerate(st.session_state.generation_history[-5:], 1):
        with st.sidebar.expander(f"#{i} {record['timestamp']}", expanded=False):
            st.write(f"**Prompt:** {record['prompt']}")
            st.write(f"**Style:** {record['style']}")
            st.write(f"**Count:** {record['num_images']}")
            st.write(f"**Quality:** {record['quality']}")
else:
    st.sidebar.info("No generation history yet")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p><strong>Multi-Style AI Image Generator</strong></p>
    <p>Version 1.0.0 | Streamlit Web Application</p>
    <p style="font-size: 12px;">
        Location: c:\\Users\\user\\Desktop\\HW4<br>
        Built with: Python + Streamlit<br>
        Features 5 AI art styles
    </p>
</div>
""", unsafe_allow_html=True)

# Additional sections
col_info1, col_info2 = st.columns(2)

with col_info1:
    with st.expander("How to Use"):
        st.markdown("""
        **3 Quick Steps:**
        
        1. **Enter Your Prompt**
           - Describe what you want
           - Supports Chinese and English
           - Be specific for better results
        
        2. **Select Style**
           - 5 art styles available
           - Each creates different look
           - Experiment to find favorites
        
        3. **Generate**
           - Click "Generate Images"
           - Wait for results
           - Download and share
        """)

with col_info2:
    with st.expander("Technical Details"):
        st.markdown("""
        **Current: Demo Version**
        - Works immediately
        - No dependencies needed
        - Shows sample images
        
        **With Dependencies:**
        - Real AI image generation
        - PyTorch + GPU support
        - Stable Diffusion models
        - 5 art styles
        - Chinese auto-translate
        
        **Requirements:**
        - Python 3.10+
        - Streamlit 1.52.0+
        - 8+ GB RAM
        - 50+ GB storage
        """)
