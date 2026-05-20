import streamlit as st
from PIL import Image
import google.generativeai as genai
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Cal AI",
    page_icon="🍱",
    layout="wide"
)

# ================= GEMINI SETUP =================
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

    genai.configure(api_key=GEMINI_API_KEY)

    model = genai.GenerativeModel(
        "models/gemini-1.5-flash"
    )

except Exception as e:
    st.error("Gemini Setup Error")
    st.code(str(e))

# ================= CUSTOM CSS =================
st.markdown("""
<style>

body {
    background-color: #0E1117;
    color: white;
}

.title {
    font-size: 50px;
    font-weight: bold;
    color: white;
}

.subtitle {
    color: #AAAAAA;
    font-size: 18px;
}

.stButton>button {
    background: linear-gradient(90deg,#00F5FF,#8A2BE2);
    color: white;
    border-radius: 12px;
    border: none;
    height: 50px;
    width: 100%;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================
st.sidebar.title("🔥 Cal AI")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "AI Meal Scanner", "BMI Calculator"]
)

# ================= DASHBOARD =================
if menu == "Dashboard":

    st.markdown(
        '<p class="title">Cal AI Dashboard</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">AI-powered calorie tracking</p>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Calories", "1850")
    col2.metric("Protein", "120g")
    col3.metric("Water", "3.2L")

# ================= AI SCANNER =================
elif menu == "AI Meal Scanner":

    st.markdown(
        '<p class="title">AI Meal Scanner</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Upload food image for calorie analysis</p>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Meal Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        try:

            image = Image.open(uploaded_file)

            col1, col2 = st.columns(2)

            with col1:
                st.image(image, use_container_width=True)

            with col2:

                if st.button("🔍 Analyze Meal"):

                    progress = st.progress(0)

                    for i in range(100):
                        time.sleep(0.01)
                        progress.progress(i + 1)

                    prompt = """
                    Analyze this food image.

                    Tell:
                    1. Food name
                    2. Estimated calories
                    3. Protein
                    4. Carbs
                    5. Fat
                    6. Health rating

                    Keep response clean and short.
                    """

                    try:

                        response = model.generate_content(
                            [prompt, image]
                        )

                        st.success("Analysis Complete")

                        st.markdown("## 🤖 AI Result")

                        st.write(response.text)

                    except Exception as e:

                        st.error("Gemini API Error")

                        st.code(str(e))

        except Exception as e:

            st.error("Image Error")

            st.code(str(e))

# ================= BMI CALCULATOR =================
elif menu == "BMI Calculator":

    st.markdown(
        '<p class="title">BMI Calculator</p>',
        unsafe_allow_html=True
    )

    height = st.number_input(
        "Height (cm)",
        value=170
    )

    weight = st.number_input(
        "Weight (kg)",
        value=70
    )

    if st.button("Calculate BMI"):

        try:

            bmi = weight / ((height / 100) ** 2)

            if bmi < 18.5:
                category = "Underweight"

            elif bmi < 25:
                category = "Normal"

            elif bmi < 30:
                category = "Overweight"

            else:
                category = "Obese"

            st.success(f"BMI: {bmi:.1f}")

            st.info(f"Category: {category}")

        except Exception as e:

            st.error("BMI Error")

            st.code(str(e))
