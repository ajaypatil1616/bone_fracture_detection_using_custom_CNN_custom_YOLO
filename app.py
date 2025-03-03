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
        h1 {{ color: white !important; }}
        div[role="radiogroup"] p {{ color: white !important; }}
        label {{ color: white !important; }}
        
        div.stFileUploader label {{ color: white !important; }}
        div.stButton button {{
            color: white !important;
            background-color: #4CAF50 !important; /* Green color */
            border: none !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            border-radius: 5px !important;
            cursor: pointer !important;
        }}
        div.stButton button:hover {{
            background-color: #45a049 !important;
        }}
        .stMarkdown, .stText {{ color: white !important; }}
        div.stMarkdown strong {{ color: white !important; }}
        .medical-report-section {{
            color: white !important;
        }}
        .medical-report-section h1 {{
            color: white !important;
        }}
        .medical-report-section div.stFileUploader label {{
            color: white !important;
        }}
        .medical-report-section div.stButton button {{
            color: white !important;
        }}
        .medical-report-section .stMarkdown,
        .medical-report-section .stText {{
            color: white !important;
        }}
        .medical-report-section {{
            background-color: #222222 !important;
            padding: 20px;
            border-radius: 10px;
        }}
        .user-message, .bot-message {{
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 80%;
            clear: both;
        }}
        .user-message {{
            background-color: #DCF8C6;
            color: black;
            float: right;
        }}
        .bot-message {{
            background-color: #E8E8E8 !important;
            color: #000000 !important;
            text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.6);
        }}
        .stMarkdown .bot-message strong {{
            color: #000000 !important;
        }}
        .clear-float {{
            clear: both;
            height: 10px;
        }}
        .stRadio label {{
            color: white !important;
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
    
    temp_path = "temp_image.jpg"
    image.save(temp_path)  

    if st.button("🔍 Detect Fracture"):
        prediction = predict_fracture(image)
        st.write(f"<span style='color:white'><strong>Prediction:</strong> {prediction}</span>", unsafe_allow_html=True)

        if prediction == "fractured":
            st.write("<span style='color:lightgreen'><strong>✅ Fracture detected !!!! Locating the Fracture</strong></span>", unsafe_allow_html=True)
            result_image = localize_fracture(temp_path)

            if result_image:
                st.image(result_image, caption="Fracture Localization", use_container_width=True)
            else:
                st.write("<span style='color:yellow'><strong>⚠️ No clear localization detected.</strong></span>", unsafe_allow_html=True)
        else:
            st.write("<span style='color:red'><strong>🛑 No fracture detected.</strong></span>", unsafe_allow_html=True)

    if os.path.exists(temp_path):
        os.remove(temp_path)
