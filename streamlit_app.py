# import streamlit as st
# import os
# import tempfile
# from PIL import Image
# from main import process_pdf
# from src.config import Config

# # Page configuration
# st.set_page_config(
#     page_title="Document Layout Analyzer",
#     page_icon="📄",
#     layout="wide"
# )

# # Custom CSS
# st.markdown("""
# <style>
#     .main-header {
#         font-size: 3rem;
#         color: #1f77b4;
#         text-align: center;
#     }
#     .entity-button {
#         width: 100%;
#         margin-bottom: 10px;
#     }
#     .image-grid {
#         display: grid;
#         grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
#         gap: 10px;
#         margin-top: 20px;
#     }
#     .image-container {
#         border: 1px solid #ddd;
#         border-radius: 5px;
#         padding: 5px;
#         text-align: center;
#     }
# </style>
# """, unsafe_allow_html=True)

# # App title
# st.markdown('<h1 class="main-header">Document Layout Analyzer</h1>', unsafe_allow_html=True)

# # File upload
# uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

# if uploaded_file is not None:
#     # Save uploaded file to temporary location
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
#         tmp_file.write(uploaded_file.getvalue())
#         pdf_path = tmp_file.name
    
#     # Process button
#     if st.button("Analyze Document Layout", type="primary"):
#         with st.spinner("Processing document..."):
#             # Process the PDF
#             entities = process_pdf(pdf_path)
            
#             # Store in session state
#             st.session_state.entities = entities
#             st.session_state.processed = True
    
#     # Display results if processing is complete
#     if hasattr(st.session_state, 'processed') and st.session_state.processed:
#         st.success("Document processing complete!")
        
#         # Create buttons for each entity type
#         entity_types = sorted(st.session_state.entities.keys())
        
#         # Display entity type buttons
#         cols = st.columns(4)
#         for i, entity_type in enumerate(entity_types):
#             with cols[i % 4]:
#                 if st.button(
#                     f"{entity_type} ({len(st.session_state.entities[entity_type])})", 
#                     key=f"btn_{entity_type}",
#                     use_container_width=True
#                 ):
#                     st.session_state.selected_entity = entity_type
        
#         # Display images for selected entity type
#         if hasattr(st.session_state, 'selected_entity'):
#             st.subheader(f"{st.session_state.selected_entity} Entities")
            
#             # Create image grid
#             st.markdown('<div class="image-grid">', unsafe_allow_html=True)
            
#             entity_files = st.session_state.entities[st.session_state.selected_entity]
#             for img_path in entity_files:
#                 try:
#                     img = Image.open(img_path)
#                     st.image(img, caption=os.path.basename(img_path), use_column_width=True)
#                 except Exception as e:
#                     st.error(f"Error loading image {img_path}: {e}")
            
#             st.markdown('</div>', unsafe_allow_html=True)
    
#     # Clean up temporary file
#     os.unlink(pdf_path)
# else:
#     st.info("Please upload a PDF document to begin analysis.")

# # Footer
# st.markdown("---")
# st.markdown("### How to use:")
# st.markdown("""
# 1. Upload a PDF document
# 2. Click the 'Analyze Document Layout' button
# 3. Click on any entity type button to view extracted elements
# """)

import streamlit as st
import os
import tempfile
from PIL import Image
from main import process_pdf
from src.config import Config

# Page configuration
st.set_page_config(
    page_title="Document Layout Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
    }
    .entity-button {
        width: 100%;
        margin-bottom: 10px;
    }
    .image-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr); /* 4 columns = quarter screen each */
        gap: 10px;
        margin-top: 20px;
    }
    .image-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 5px;
        text-align: center;
    }
    .stImage img {
        width: 25%  !important;   /* fill its grid cell */
        height: auto !important;  /* keep aspect ratio */
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# App title
st.markdown('<h1 class="main-header">Document Layout Analyzer</h1>', unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_file is not None:
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        pdf_path = tmp_file.name
    
    # Process button
    if st.button("Analyze Document Layout", type="primary"):
        with st.spinner("Processing document..."):
            # Process the PDF
            entities = process_pdf(pdf_path)
            
            # Store in session state
            st.session_state.entities = entities
            st.session_state.processed = True
    
    # Display results if processing is complete
    if hasattr(st.session_state, 'processed') and st.session_state.processed:
        st.success("Document processing complete!")
        
        # Create buttons for each entity type
        entity_types = sorted(st.session_state.entities.keys())
        
        # Display entity type buttons
        cols = st.columns(4)
        for i, entity_type in enumerate(entity_types):
            with cols[i % 4]:
                if st.button(
                    f"{entity_type} ({len(st.session_state.entities[entity_type])})", 
                    key=f"btn_{entity_type}",
                    use_container_width=True
                ):
                    st.session_state.selected_entity = entity_type
        
        # Display images for selected entity type
        if hasattr(st.session_state, 'selected_entity'):
            st.subheader(f"{st.session_state.selected_entity} Entities")
            
            # Create image grid
            st.markdown('<div class="image-grid">', unsafe_allow_html=True)
            
            entity_files = st.session_state.entities[st.session_state.selected_entity]
            for img_path in entity_files:
                try:
                    img = Image.open(img_path)
                    st.image(img, caption=os.path.basename(img_path), use_container_width=True)
                except Exception as e:
                    st.error(f"Error loading image {img_path}: {e}")
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Clean up temporary file
    os.unlink(pdf_path)
else:
    st.info("Please upload a PDF document to begin analysis.")

# Footer
st.markdown("---")
st.markdown("### How to use:")
st.markdown("""
1. Upload a PDF document
2. Click the 'Analyze Document Layout' button
3. Click on any entity type button to view extracted elements
""")
