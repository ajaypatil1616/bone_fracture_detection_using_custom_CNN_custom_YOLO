import streamlit as st
from PIL import Image
import os
import base64
from utils import predict_fracture, localize_fracture

st.set_page_config(page_title="Bone Fracture Detection", layout="centered")

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

bg_image = "bg.jpg"
st.markdown(
    f"""
    <style>
        .stApp {{
            background: url("data:image/png;base64,{get_base64_image(bg_image)}") no-repeat center center fixed;
            background-size: cover;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
st.title("Bone Fracture Detection System")
st.write("Upload an X-ray image to check for fractures.")

uploaded_file = st.file_uploader("Choose an X-ray image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    # st.image(image, caption="Uploaded Image", use_container_width=True)
    
    temp_path = "temp_image.jpg"
    image.save(temp_path)  

    if st.button("🔍 Detect Fracture"):
        prediction = predict_fracture(image)
        st.write(f"**Prediction:** {prediction}")

        if prediction == "fractured":
            st.write("✅ Fracture detected !!!!   Locating the Fracture")
            result_image = localize_fracture(temp_path)

            if result_image:
                st.image(result_image, caption="Fracture Localization", use_container_width=True)
            else:
                st.write("⚠️ No clear localization detected.")
        else:
            st.write("🛑 No fracture detected.")

    # Clean up temporary file
    if os.path.exists(temp_path):
        os.remove(temp_path)
