import streamlit as st
from PIL import Image
import google.generativeai as genai

# PAGE CONFIG
st.set_page_config(page_title="Cal AI", layout="wide")

st.title("🔥 Cal AI")
st.subheader("AI Meal Scanner")

# GEMINI API
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-pro")

# FILE UPLOAD
uploaded_file = st.file_uploader(
    "Upload Meal Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(image, caption="Uploaded Meal", use_container_width=True)

    if st.button("🔍 Analyze Meal"):

        with st.spinner("Analyzing meal..."):

            prompt = """
            Analyze this food image and provide:

            1. Food items detected
            2. Estimated calories
            3. Protein estimate
            4. Carb estimate
            5. Fat estimate
            6. Health rating
            """

            try:

                response = model.generate_content([
                    prompt,
                    image
                ])

                st.success("AI Scan Complete")

                st.markdown("## 🤖 AI Analysis")

                st.write(response.text)

            except Exception as e:

                st.error("Gemini API Error")

                st.code(str(e))
