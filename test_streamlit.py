# Test Streamlit App
import streamlit as st

st.set_page_config(page_title="Test App", layout="wide")

st.title("Test Streamlit Application")
st.write("If you see this, Streamlit is working!")

st.info("This is a test - the app loaded successfully")

# Test the core module
try:
    from multi_style_image_generator import StyleModelsConfig
    st.success("Core module imported successfully!")
    
    st.write("Available styles:")
    for style_name in StyleModelsConfig.STYLE_MODELS.keys():
        st.write(f"  - {style_name}")
except Exception as e:
    st.error(f"Error: {e}")
