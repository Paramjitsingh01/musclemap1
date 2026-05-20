import streamlit as st
from PIL import Image
import google.generativeai as genai

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Cal AI",
    page_icon="🔥",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1, h2, h3 {
    color: white;
}

.stButton > button {
    background: linear-gradient(90deg, #00C6FF, #7F00FF);
    color: white;
    border: none;
    padding: 0.7rem 1.5rem;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
}

.stButton > button:hover {
    transform: scale(1.03);
}

.css-1d391kg {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# =========================
# GEMINI API CONFIG
# =========================
try:

    genai.configure(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

    model = genai.GenerativeModel(
        "gemini-1.5-pro"
    )

except Exception as e:

    st.error("Gemini API Configuration Error")
    st.code(str(e))
    st.stop()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🔥 Cal AI")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "AI Meal Scanner",
        "BMI Calculator"
    ]
)

# =========================
# DASHBOARD
# =========================
if page == "Dashboard":

    st.title("🔥 Cal AI Dashboard")

    st.markdown("""
    ### Welcome to Cal AI

    Features:
    - 🍔 AI Meal Scanner
    - 📸 Food Detection
    - 🔥 Calories Estimation
    - 💪 Protein / Carbs / Fat Analysis
    - 📊 BMI Calculator
    """)

# =========================
# AI MEAL SCANNER
# =========================
elif page == "AI Meal Scanner":

    st.title("🍔 AI Meal Scanner")

    st.write(
        "Upload a meal image and let AI analyze calories & nutrition."
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

                st.image(
                    image,
                    caption="Uploaded Meal",
                    use_container_width=True
                )

            with col2:

                st.write("")

                if st.button("🔍 Analyze Meal"):

                    with st.spinner("Analyzing meal..."):

                        prompt = """
                        Analyze this food image and provide:

                        1. Food items detected
                        2. Estimated calories
                        3. Protein estimate
                        4. Carbohydrates estimate
                        5. Fat estimate
                        6. Health rating out of 10
                        7. Suggest whether this meal is healthy or not
                        """

                        try:

                            response = model.generate_content(
                                [
                                    prompt,
                                    image
                                ]
                            )

                            st.success("✅ AI Scan Complete")

                            st.markdown("## 🤖 AI Analysis")

                            st.write(response.text)

                        except Exception as e:

                            st.error("Gemini API Error")

                            st.code(str(e))

        except Exception as e:

            st.error("Image Processing Error")

            st.code(str(e))

# =========================
# BMI CALCULATOR
# =========================
elif page == "BMI Calculator":

    st.title("📊 BMI Calculator")

    height = st.number_input(
        "Enter Height (cm)",
        min_value=50.0,
        max_value=300.0,
        value=170.0
    )

    weight = st.number_input(
        "Enter Weight (kg)",
        min_value=10.0,
        max_value=300.0,
        value=70.0
    )

    if st.button("Calculate BMI"):

        bmi = weight / ((height / 100) ** 2)

        st.success(f"Your BMI is: {bmi:.2f}")

        if bmi < 18.5:
            st.warning("Underweight")

        elif bmi < 25:
            st.success("Normal Weight")

        elif bmi < 30:
            st.warning("Overweight")

        else:
            st.error("Obese")
