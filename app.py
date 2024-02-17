import streamlit as st
from utils import *

st.set_page_config(layout='wide')

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.header("Image Generator")
        input_text = st.text_input("Enter text to generate image:")
        if st.button("Generate"):
            if input_text:
                # path_image = text_to_image(input_text)
                st.session_state['generated_image_path'] = text_to_image(input_text)
                st.session_state['generated_image'] = Image.open(st.session_state['generated_image_path'])
                st.image(st.session_state['generated_image_path'], caption='Imagen Mostrada')

                # Create a button to download the image
                with open(st.session_state['generated_image_path'], "rb") as file:
                    btn = st.download_button(
                        label="Download Image",
                        data=file,
                        file_name="downloaded_image.jpg",
                        mime="image/jpeg"
                    )
            else:
                st.error("Please enter some text.")

    with col2:
        st.header("Classify Image")
        uploaded_file = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'])
        if 'generated_image' in st.session_state and st.session_state['generated_image'] is not None:
            if st.button("Classificar Imagen Generada"):
                st.image(st.session_state['generated_image'], caption='Imagen para Clasificar')
                classification = classification_image(st.session_state['generated_image'])
                st.success(f"Classification predict: {classification}")
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image')
            if st.button("Classify"):
                classification = classification_image(image)
                st.success(f"Classification predict: {classification}")

# Footer
st.markdown("-"*11)
st.text("Streamlit App for Image Generation and Classification")