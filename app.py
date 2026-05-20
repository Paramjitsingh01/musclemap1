# ================= IMPORTS ================= #
import google.generativeai as genai
import streamlit as st
from PIL import Image
import google.generativeai as genai
import time

# ================= PAGE CONFIG ================= #
st.set_page_config(
    page_title="Cal AI",
    page_icon="🍱",
    layout="wide"
)

# ================= GEMINI API ================= #
GEMINI_API_KEY = "AIzaSyB40Ryu_9p3EPkfp0ilK5KptonJ3HwILY0"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

# ================= CUSTOM CSS ================= #
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #0E1117;
    color: white;
}

.main {
    background-color: #0E1117;
}

.title {
    font-size: 52px;
    font-weight: 700;
    color: white;
}

.subtitle {
    color: #B0B3B8;
    font-size: 18px;
}

.glass {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
}

.metric-card {
    background: linear-gradient(
        135deg,
        rgba(0,255,255,0.08),
        rgba(138,43,226,0.08)
    );
    padding: 25px;
    border-radius: 25px;
    text-align: center;
}

.stButton>button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg,#00F5FF,#8A2BE2);
    color: white;
    font-size: 17px;
    font-weight: 600;
}

.result-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR ================= #
st.sidebar.title("🔥 Cal AI")

menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "AI Meal Scanner", "BMI Calculator"]
)

# ================= DASHBOARD ================= #
if menu == "Dashboard":

    st.markdown(
        '<div class="title">Cal AI Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">AI-powered calorie tracking & nutrition analysis</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("🔥", "1850", "Calories"),
        ("🥩", "120g", "Protein"),
        ("💧", "3.2L", "Water"),
        ("⚡", "78%", "Goal")
    ]

    for col, card in zip([col1, col2, col3, col4], cards):

        with col:
            st.markdown(f"""
            <div class="metric-card">
                <h2>{card[0]}</h2>
                <h1>{card[1]}</h1>
                <p>{card[2]}</p>
            </div>
            """, unsafe_allow_html=True)

# ================= AI MEAL SCANNER ================= #
elif menu == "AI Meal Scanner":

    st.markdown(
        '<div class="title">AI Meal Scanner</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload meal image and let AI analyze food & calories.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    uploaded_file = st.file_uploader(
        "Upload Meal Image",
        type=["jpg", "png", "jpeg"]
    )

    if uploaded_file:

        image = Image.open(uploaded_file)

        col1, col2 = st.columns([1,1])

        with col1:
            st.image(image, use_container_width=True)

        with col2:

            st.markdown('<div class="glass">', unsafe_allow_html=True)

            if st.button("🔍 Analyze Meal"):

                progress = st.progress(0)

                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)

                # ================= GEMINI AI ================= #
                prompt = """
                Analyze this food image.

                Tell:
                1. Food names
                2. Estimated calories
                3. Protein
                4. Carbs
                5. Fat
                6. Health recommendation

                Keep response short and clean.
                """

                response = model.generate_content(
                    [prompt, image]
                )

                st.success("AI Scan Complete")

                st.markdown("## 🤖 AI Analysis")

                st.write(response.text)

            st.markdown('</div>', unsafe_allow_html=True)

# ================= BMI CALCULATOR ================= #
elif menu == "BMI Calculator":

    st.markdown(
        '<div class="title">BMI Calculator</div>',
        unsafe_allow_html=True
    )

    st.write("")

    left_col, right_col = st.columns([1, 1.2])

    # ================= LEFT SIDE ================= #
    with left_col:

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        age = st.number_input(
            "Age",
            min_value=2,
            max_value=120,
            value=25
        )

        gender = st.radio(
            "Gender",
            ["Male", "Female"],
            horizontal=True
        )

        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=180
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=300,
            value=65
        )

        calculate = st.button("Calculate BMI")

        st.markdown('</div>', unsafe_allow_html=True)

    # ================= RIGHT SIDE ================= #
    with right_col:

        if calculate:

            bmi = weight / ((height / 100) ** 2)

            # ================= BMI CATEGORY ================= #
            if bmi < 18.5:
                category = "Underweight"
                color = "orange"

            elif bmi < 25:
                category = "Normal"
                color = "green"

            elif bmi < 30:
                category = "Overweight"
                color = "gold"

            else:
                category = "Obesity"
                color = "red"

            st.markdown('<div class="result-card">', unsafe_allow_html=True)

            st.markdown(f"""
            <h1>
                BMI = {bmi:.1f} kg/m²
            </h1>

            <h2 style="color:{color};">
                {category}
            </h2>
            """, unsafe_allow_html=True)

            healthy_min = 18.5 * ((height / 100) ** 2)
            healthy_max = 25 * ((height / 100) ** 2)

            st.markdown(f"""
            ### 📌 Health Information

            - Healthy BMI range:
              **18.5 kg/m² - 25 kg/m²**

            - Healthy weight for your height:
              **{healthy_min:.1f} kg - {healthy_max:.1f} kg**

            - BMI Category:
              **{category}**

            - Gender:
              **{gender}**
            """)

            st.markdown('</div>', unsafe_allow_html=True)
