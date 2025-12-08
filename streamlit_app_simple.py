"""
Streamlit Web Application for Multi-Style AI Image Generator
Simple Version - ASCII Only for Compatibility
"""

import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Page configuration
st.set_page_config(
    page_title="Multi-Style AI Image Generator",
    page_icon="8",
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

# Load configuration
def load_config():
    config_path = Path("config.json")
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# System health check
def check_system():
    status = {
        "python": True,
        "streamlit": False,
        "torch": False,
        "diffusers": False,
        "transformers": False,
        "pillow": False,
    }
    
    try:
        import streamlit
        status["streamlit"] = True
    except:
        pass
    try:
        import torch
        status["torch"] = True
    except:
        pass
    try:
        import diffusers
        status["diffusers"] = True
    except:
        pass
    try:
        import transformers
        status["transformers"] = True
    except:
        pass
    try:
        from PIL import Image
        status["pillow"] = True
    except:
        pass
    
    return status

# Initialize session state
if "config" not in st.session_state:
    st.session_state.config = load_config()
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
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
        help="Supports Chinese and English prompts"
    )
    
    st.markdown("### Art Styles")
    col_style1, col_style2 = st.columns(2)
    
    with col_style1:
        st.markdown("""
        **1. Realistic**
        - Photography style
        - Best for: Landscapes, portraits
        """)
        st.markdown("""
        **2. Anime 2D**
        - Japanese anime style
        - Best for: Characters, scenes
        """)
        st.markdown("""
        **3. Fantasy Art**
        - Fantasy style
        - Best for: Magic, creatures
        """)
    
    with col_style2:
        st.markdown("""
        **4. 3D Rendering**
        - CGI and 3D effects
        - Best for: Architecture, products
        """)
        st.markdown("""
        **5. Oil Painting**
        - Painting style
        - Best for: Landscapes, artistic
        """)
    
    style = st.radio(
        "Select Style",
        options=["Realistic", "Anime 2D", "Fantasy Art", "3D Rendering", "Oil Painting"],
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
        help="How many images to generate (1-4)"
    )
    
    num_steps = st.slider(
        "Inference Steps",
        min_value=10,
        max_value=50,
        value=30,
        step=5,
        help="More steps = better quality, slower speed"
    )
    
    guidance_scale = st.slider(
        "Guidance Strength",
        min_value=1.0,
        max_value=15.0,
        value=7.5,
        step=0.5,
        help="How much to follow the prompt"
    )
    
    device = st.selectbox(
        "Device",
        options=["cuda", "cpu"],
        help="cuda: GPU (fast), cpu: CPU (slow)"
    )

# Performance info
st.markdown("---")
with st.expander("Performance Information"):
    col_perf1, col_perf2, col_perf3 = st.columns(3)
    
    with col_perf1:
        st.markdown("""
        **Fast (15 steps)**
        - Time: 10-20 sec
        - Quality: Medium
        - GPU: Good
        """)
    
    with col_perf2:
        st.markdown("""
        **Standard (30 steps)**
        - Time: 30-50 sec
        - Quality: Good
        - GPU: Recommended
        """)
    
    with col_perf3:
        st.markdown("""
        **High Quality (50 steps)**
        - Time: 50-100 sec
        - Quality: Excellent
        - GPU: Required
        """)

# Generation section
st.markdown("---")
st.markdown("## Generate Images")

col_btn1, col_btn2, col_btn3 = st.columns(3)

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
        help="View style examples (no GPU needed)"
    )

with col_btn3:
    reset_btn = st.button(
        "Reset",
        key="reset",
        use_container_width=True,
        help="Clear settings"
    )

# Handle button actions
if generate_btn:
    if not prompt:
        st.warning("Enter a prompt first")
    else:
        # Try to import the generator
        try:
            from multi_style_image_generator import MultiStyleImageGenerator
            generator_available = True
        except ImportError as e:
            generator_available = False
            st.error(f"Cannot import generator module: {e}")
        
        if generator_available:
            with st.spinner(f"Generating {num_images} image(s) with {num_steps} steps..."):
                try:
                    generator = MultiStyleImageGenerator(
                        device=device,
                        num_inference_steps=num_steps
                    )
                    
                    result = generator.generate_images(
                        prompt=prompt,
                        style=style.lower().replace(" ", "_"),
                        num_images=num_images,
                        guidance_scale=guidance_scale,
                        num_inference_steps=num_steps
                    )
                    
                    record = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "prompt": prompt,
                        "style": style,
                        "num_images": num_images,
                        "num_steps": num_steps,
                        "guidance_scale": guidance_scale,
                        "device": device,
                        "status": "success"
                    }
                    st.session_state.generation_history.append(record)
                    
                    st.success("Image generation successful!")
                    st.json(record)
                    
                    if isinstance(result, dict) and "images" in result:
                        st.markdown("### Generated Images")
                        cols = st.columns(min(num_images, 2))
                        for idx, img in enumerate(result.get("images", [])):
                            with cols[idx % len(cols)]:
                                st.image(img, caption=f"Image {idx+1}")
                    
                except Exception as e:
                    error_msg = str(e)
                    st.error(f"Generation failed: {error_msg}")
                    
                    if "cuda" in error_msg.lower() or "gpu" in error_msg.lower():
                        st.warning("""
                        GPU Error - Try:
                        - Select CPU mode
                        - Check NVIDIA drivers
                        - Check CUDA installation
                        """)
                    elif "module" in error_msg.lower() or "import" in error_msg.lower():
                        st.warning("""
                        Missing Dependencies - Run:
                        pip install -r requirements.txt
                        """)
        else:
            st.error("Cannot proceed without dependencies")
            st.warning("""
            Installation Steps:
            
            1. Install dependencies:
            pip install -r requirements.txt
            
            2. Verify installation:
            python -c "import torch; import diffusers; print('OK')"
            
            3. Restart Streamlit
            """)

if demo_btn:
    st.info("Demo Mode - 5 Art Styles Showcase")
    
    st.markdown("### Art Styles Overview")
    
    demos = [
        {
            "name": "Realistic",
            "desc": "Photography style - High quality realistic images",
            "prompt": "A beautiful mountain landscape with sunlight",
            "tips": "Best for: Landscapes, architecture, products"
        },
        {
            "name": "Anime 2D",
            "desc": "Japanese anime style - Vibrant anime artwork",
            "prompt": "A magic girl in a battle pose with sparkles",
            "tips": "Best for: Characters, scenes, illustrations"
        },
        {
            "name": "Fantasy Art",
            "desc": "Fantasy style - Surreal magical effects",
            "prompt": "A mysterious dragon flying through clouds",
            "tips": "Best for: Magic, creatures, fantasy scenes"
        },
        {
            "name": "3D Rendering",
            "desc": "CGI style - 3D rendered graphics",
            "prompt": "A futuristic city with tall buildings",
            "tips": "Best for: Architecture, products, tech"
        },
        {
            "name": "Oil Painting",
            "desc": "Painting style - Artistic oil paintings",
            "prompt": "A sunflower field under sunlight",
            "tips": "Best for: Landscapes, artistic, decorative"
        }
    ]
    
    for i, demo in enumerate(demos, 1):
        with st.expander(f"{i}. {demo['name']} - {demo['desc']}", expanded=(i==1)):
            st.markdown(f"**{demo['tips']}**")
            st.code(demo['prompt'], language="text")
            st.markdown("""
            Expected Generation Time:
            - Fast (15 steps): 10-20 seconds
            - Standard (30 steps): 30-50 seconds
            - High Quality (50 steps): 50-100 seconds
            """)
    
    st.success("""
    Demo Complete! Now you can:
    1. Enter your own prompt above
    2. Select a style
    3. Adjust parameters
    4. Click "Generate Images"
    
    Note: First run will download AI models (10-30 minutes)
    """)

if reset_btn:
    st.session_state.generation_history = []
    st.session_state.generated_images = []
    st.rerun()

# Sidebar
st.sidebar.markdown("# Control Panel")

# System Status
st.sidebar.markdown("## System Status")

system_status = check_system()
all_ready = all(list(system_status.values())[1:])

status_text = ""
for pkg, status_val in system_status.items():
    icon = "[OK]" if status_val else "[XX]"
    status_text += f"{icon} {pkg.upper()}\n"

if all_ready:
    st.sidebar.success("System is ready to generate images!")
else:
    st.sidebar.error("Missing required packages")
    st.sidebar.code(status_text, language="text")
    st.sidebar.warning("""
    Install dependencies:
    pip install -r requirements.txt
    """)

st.sidebar.markdown("---")

st.sidebar.info("""
Python: 3.10.19
Streamlit: 1.52.0
Location: c:\\Users\\user\\Desktop\\HW4
""")

# Quick Install
with st.sidebar.expander("Quick Install", expanded=not all_ready):
    st.markdown("""
    **Step 1: Install Dependencies**
    ```powershell
    cd c:\\Users\\user\\Desktop\\HW4
    pip install -r requirements.txt
    ```
    
    **Step 2: Verify**
    ```powershell
    python -c "import torch; import diffusers; print('OK')"
    ```
    
    **Step 3: Restart App**
    Press Ctrl+C then run:
    ```powershell
    streamlit run streamlit_app.py
    ```
    """)

# FAQ
with st.sidebar.expander("FAQ"):
    st.markdown("""
    **Q: Why is it slow on first run?**
    A: Downloading AI models (5-50 GB) takes 10-30 minutes
    
    **Q: Can I use CPU instead of GPU?**
    A: Yes, select CPU mode (slower)
    
    **Q: How to improve quality?**
    A: Increase steps to 50 and guidance strength
    
    **Q: What languages are supported?**
    A: Chinese prompts auto-translate to English
    """)

# History
st.sidebar.markdown("---")
st.sidebar.markdown("## Generation History")

if st.session_state.generation_history:
    for i, record in enumerate(st.session_state.generation_history[-5:], 1):
        with st.sidebar.expander(f"#{i} {record['timestamp']}", expanded=False):
            st.json(record)
else:
    st.sidebar.info("No generation history yet")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666;">
    <p><strong>Multi-Style AI Image Generator</strong></p>
    <p>Version 1.1.0 | Streamlit Web Application</p>
    <p style="font-size: 12px;">
        Location: c:\\Users\\user\\Desktop\\HW4<br>
        Python 3.10.19 | Streamlit 1.52.0
    </p>
</div>
""", unsafe_allow_html=True)

# Additional info
st.markdown("---")

col_info1, col_info2 = st.columns(2)

with col_info1:
    with st.expander("User Guide"):
        st.markdown("""
        **3 Quick Steps:**
        
        1. Enter your prompt
           - Support Chinese and English
           - Describe what you want
        
        2. Select style and parameters
           - 5 art styles available
           - Adjust quality vs speed
        
        3. Generate images
           - Click "Generate Images"
           - Wait for results
           - Download and share
        """)

with col_info2:
    with st.expander("Technical Info"):
        st.markdown("""
        **Technology Stack:**
        
        - Streamlit: Web framework
        - PyTorch: Deep learning
        - Stable Diffusion: AI models
        - Hugging Face: Model hub
        - Python: Programming
        
        **Requirements:**
        
        - GPU: NVIDIA (recommended)
        - RAM: 8+ GB
        - Storage: 50+ GB for models
        """)
