# coding: utf-8
"""
Simple Streamlit test app for AI Image Generator
"""
import streamlit as st
import torch
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

st.set_page_config(
    page_title="AI Image Generator Test",
    layout="wide"
)

st.title("Multi-Style AI Image Generator")
st.markdown("### Test Application - 5 Styles")

# Test styles
STYLES = {
    "0": "Realistic (寫實風格)",
    "1": "Anime 2D (二次元動漫)",
    "2": "Fantasy Art (夢幻藝術)",
    "3": "3D Rendering (3D渲染)",
    "4": "Oil Painting (油畫風格)"
}

REAL_STYLES = {
    "0": "\u5beb\u5be6\u98a8\u683c",
    "1": "\u4e8c\u6b21\u5143\u52d5\u6f2b",
    "2": "\u5922\u5e7b\u85dd\u8853",
    "3": "3D\u6e32\u67d3",
    "4": "\u6cb9\u756b\u98a8\u683c"
}

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Enter Your Prompt")
    prompt = st.text_area(
        "Prompt",
        placeholder="A beautiful sunset...",
        height=80
    )
    
    st.markdown("### Select Style")
    style_idx = st.radio(
        "Style",
        options=list(STYLES.keys()),
        format_func=lambda x: STYLES[x],
        horizontal=True
    )

with col2:
    st.markdown("### Settings")
    num_images = st.slider("Images", 1, 4, 1)
    steps = st.slider("Steps", 10, 50, 30, 5)
    guidance = st.slider("Guidance", 1.0, 15.0, 7.5, 0.5)

device = "GPU (NVIDIA)" if torch.cuda.is_available() else "CPU"
st.info(f"Device: {device} | Style: {STYLES[style_idx]}")

col_gen, col_demo = st.columns(2)

with col_gen:
    if st.button("Generate Images", use_container_width=True):
        if not prompt:
            st.warning("Please enter a prompt")
        else:
            try:
                from multi_style_image_generator import MultiStyleImageGenerator
                
                st.info(f"Starting generation with style: {REAL_STYLES[style_idx]}")
                
                generator = MultiStyleImageGenerator()
                
                with st.spinner("Generating..."):
                    result = generator.generate(
                        prompt_text=prompt,
                        style_name=REAL_STYLES[style_idx],
                        num_images=num_images,
                        num_inference_steps=steps,
                        guidance_scale=guidance,
                        save_output=False
                    )
                
                st.success(f"Generated {num_images} image(s)!")
                
                # Display grid
                if "grid" in result:
                    st.image(result["grid"], use_column_width=True, caption="Generated Grid")
                
                # Display individual images
                cols = st.columns(min(num_images, 2))
                for idx, img in enumerate(result["images"]):
                    with cols[idx % len(cols)]:
                        st.image(img, caption=f"Image {idx+1}")
                
                generator.cleanup()
                
            except Exception as e:
                st.error(f"Error: {str(e)}")

with col_demo:
    if st.button("Show Available Styles", use_container_width=True):
        st.markdown("### Available Art Styles")
        for i in range(5):
            idx = str(i)
            st.markdown(f"**{i+1}. {STYLES[idx]}**")
            st.caption(f"Real name: {REAL_STYLES[idx]}")

st.markdown("---")
st.markdown("""
### How to Use:
1. Enter your image description in the prompt box
2. Select an art style
3. Adjust settings if needed
4. Click "Generate Images"

### First Run:
- Will download AI models (5-30 minutes)
- Only needed once
- Requires internet connection
""")
