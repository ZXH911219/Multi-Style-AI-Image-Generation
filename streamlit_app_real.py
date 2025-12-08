# coding: utf-8
"""
Multi-Style AI Image Generator - Streamlit Web App
Real AI image generation with 5 art styles
"""

import streamlit as st
import torch
from PIL import Image
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Multi-Style AI Image Generator",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Art styles mapping
STYLES_DISPLAY = {
    "0": "Realistic",
    "1": "Anime 2D",
    "2": "Fantasy Art",
    "3": "3D Rendering",
    "4": "Oil Painting"
}

# Real style names - using Unicode escape to avoid encoding issues
REAL_STYLES = {
    "0": "\u5beb\u5be6\u98a8\u683c",
    "1": "\u4e8c\u6b21\u5143\u52d5\u6f2b",
    "2": "\u5922\u5e7b\u85dd\u8853",
    "3": "3D\u6e32\u67d3",
    "4": "\u6cb9\u756b\u98a8\u683c"
}

@st.cache_resource
def load_generator():
    """Load the image generator (cached)"""
    try:
        from multi_style_image_generator import MultiStyleImageGenerator
        generator = MultiStyleImageGenerator()
        return generator, "cuda" if torch.cuda.is_available() else "cpu"
    except Exception as e:
        st.error("Failed to load: " + str(e))
        return None, None

if "generation_history" not in st.session_state:
    st.session_state.generation_history = []

st.title("AI Image Generator")
st.markdown("### Multi-Style AI Image Generation")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("## Input Prompt")
    
    prompt = st.text_area(
        "Enter prompt (Chinese or English)",
        placeholder="A beautiful sunset...",
        height=100
    )
    
    st.markdown("### Select Style")
    style_idx = st.radio(
        "Style",
        options=list(STYLES_DISPLAY.keys()),
        format_func=lambda x: STYLES_DISPLAY[x],
        horizontal=True
    )

with col2:
    st.markdown("## Settings")
    
    num_images = st.slider("Number of Images", 1, 4, 1)
    num_steps = st.slider("Quality Steps", 10, 50, 30, 5)
    guidance = st.slider("Guidance Strength", 1.0, 15.0, 7.5, 0.5)

device = "GPU (NVIDIA)" if torch.cuda.is_available() else "CPU"
st.info("Device: " + device + " | Style: " + STYLES_DISPLAY[style_idx])

col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    gen_btn = st.button("Generate", use_container_width=True)

with col_btn2:
    demo_btn = st.button("Demo", use_container_width=True)

with col_btn3:
    clear_btn = st.button("Clear", use_container_width=True)

if gen_btn:
    if not prompt:
        st.warning("Please enter a prompt")
    else:
        try:
            gen, dev = load_generator()
            if gen is None:
                st.error("Generator failed to load")
            else:
                with st.spinner("Generating " + str(num_images) + " image(s)..."):
                    style_name = REAL_STYLES[style_idx]
                    st.write("Using style: " + style_name)
                    
                    result = gen.engine.generate_images(
                        prompt_text=prompt,
                        style_name=style_name,
                        num_images=num_images,
                        guidance_scale=guidance,
                        num_inference_steps=num_steps
                    )
                
                if result and "images" in result:
                    st.success("Successfully generated " + str(num_images) + " image(s)!")
                    
                    if "grid" in result:
                        st.image(result["grid"], use_column_width=True)
                    
                    cols = st.columns(min(num_images, 2))
                    for idx, img in enumerate(result["images"]):
                        with cols[idx % len(cols)]:
                            st.image(img, caption="Image " + str(idx+1))
                    
                    st.session_state.generation_history.append({
                        "time": datetime.now().strftime("%H:%M:%S"),
                        "prompt": prompt,
                        "style": STYLES_DISPLAY[style_idx],
                        "count": num_images
                    })
                else:
                    st.error("Failed to generate images")
                    
        except Exception as e:
            error_msg = str(e)
            st.error("Error: " + error_msg)
            
            if "out of memory" in error_msg.lower():
                st.warning("GPU out of memory - try fewer images or lower steps")

if demo_btn:
    st.info("Available Art Styles Demo")
    
    demos = {
        "0": "A beautiful mountain landscape with clear blue sky",
        "1": "An anime girl character with magical aura",
        "2": "A mystical forest with magical creatures",
        "3": "A modern futuristic city with neon lights",
        "4": "A field of sunflowers at golden hour sunset"
    }
    
    for i in range(5):
        idx = str(i)
        with st.expander("Style " + str(i+1) + ": " + STYLES_DISPLAY[idx], expanded=(i==0)):
            st.markdown("Example prompt:")
            st.code(demos[idx], language="text")
            st.markdown("This style will create images with the specified artistic approach.")

if clear_btn:
    st.session_state.generation_history = []
    st.rerun()

st.sidebar.markdown("# Control Panel")

st.sidebar.markdown("## System Status")
if torch.cuda.is_available():
    st.sidebar.success("GPU Available: " + torch.cuda.get_device_name(0))
else:
    st.sidebar.warning("GPU Not Available - Using CPU")

with st.sidebar.expander("Quick Start Guide", expanded=True):
    st.markdown("""
    **3 Simple Steps:**
    
    1. Enter your image description
    2. Select an art style
    3. Click Generate
    
    **First Run Note:**
    - Will download AI models (5-30 minutes)
    - Only required once
    - Requires internet connection
    """)

with st.sidebar.expander("FAQ"):
    st.markdown("""
    **Q: Why slow on first run?**
    A: Downloading large AI models (5-50 GB)
    
    **Q: Can I use CPU?**
    A: Yes, but much slower (1-3 min per image)
    
    **Q: How to improve quality?**
    A: Increase steps to 50 and guidance to 10+
    
    **Q: Languages supported?**
    A: Both Chinese and English prompts work
    
    **Q: How many styles?**
    A: 5 different art styles available
    """)

st.sidebar.markdown("---")
st.sidebar.markdown("## Generation History")

if st.session_state.generation_history:
    st.sidebar.info("Recent generations: " + str(len(st.session_state.generation_history)))
    for i, rec in enumerate(st.session_state.generation_history[-5:], 1):
        with st.sidebar.expander("Entry " + str(i) + ": " + rec["time"]):
            st.write("**Prompt:** " + rec["prompt"][:50] + "...")
            st.write("**Style:** " + rec["style"])
            st.write("**Images:** " + str(rec["count"]))
else:
    st.sidebar.info("No generation history yet")

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px; font-size: 12px;">
    <p><strong>Multi-Style AI Image Generator</strong></p>
    <p>Version 1.0.0 | Powered by Stable Diffusion</p>
    <p>Location: c:\\Users\\user\\Desktop\\HW4</p>
</div>
""", unsafe_allow_html=True)
