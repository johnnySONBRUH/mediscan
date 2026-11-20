import streamlit as st
from ocr_utils import perform_ocr
from AI import AI
import os
import uuid

# --- Configuration ---
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
# ---------------------

st.set_page_config(page_title="MediScan", page_icon="💊")

st.title("💊 MediScan")
st.write("Take a photo or upload a prescription label to get it translated into plain language.")

uploaded_file = st.file_uploader("Upload prescription image", type=['png', 'jpg', 'jpeg', 'webp'])

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Prescription", use_container_width=True)
    
    if st.button("Scan and Translate"):
        if not GEMINI_API_KEY:
            st.error("Configuration Error: Please set the GEMINI_API_KEY in your Streamlit secrets.")
        else:
            with st.spinner("Processing image..."):
                # Use a unique filename for each session/upload to prevent data collisions
                temp_path = f"temp_{uuid.uuid4()}.png"
                try:
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # OCR
                    extracted_text = perform_ocr(temp_path)
                    
                    if "Error" in extracted_text:
                        st.error(f"OCR failed: {extracted_text}")
                    else:
                        st.subheader("Extracted Text:")
                        st.text(extracted_text)
                        
                        if not extracted_text.strip():
                            st.warning("No text was detected in the image. Please try a clearer photo.")
                        else:
                            # AI Simplification (Streamed)
                            st.subheader("Simplified Instructions:")
                            ai = AI(GEMINI_API_KEY)
                            
                            # Use a container to stream the response
                            response_container = st.empty()
                            full_response = ""
                            
                            stream = ai.simplify_text_stream(extracted_text)
                            
                            # Display chunks
                            for chunk in stream:
                                if chunk.startswith("ERROR_API_FAILURE:"):
                                    st.error(f"AI API Error: {chunk.replace('ERROR_API_FAILURE:', '').strip()}")
                                    full_response = "" # Clear to prevent showing error as text
                                    break
                                full_response += chunk
                                response_container.markdown(full_response + "▌")
                            
                            if full_response:
                                response_container.markdown(full_response)
                
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                
                finally:
                    # Cleanup the unique file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)