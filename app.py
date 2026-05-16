import streamlit as st
from PIL import Image
import numpy as np
import time

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Cal AI",
    page_icon="🍱",
    layout="wide",
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');

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
    font-size: 18px;
    color: #B0B3B8;
}

.glass {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

.metric-card {
    background: linear-gradient(
        135deg,
        rgba(0,255,255,0.08),
        rgba(138,43,226,0.08)
    );
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

.scan-btn button {
    width: 100%;
    height: 55px;
    border-radius: 15px;
    border: none;
    background: linear-gradient(90deg,#00F5FF,#8A2BE2);
    color: white;
    font-size: 18px;
    font-weight: 600;
}

.stFileUploader {
    background: rgba(255,255,255,0.03);
    padding: 20px;
    border-radius: 20px;
}

.sidebar .sidebar-content {
    background-color: #0B0D13;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #
st.sidebar.title("🔥 Cal AI")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Meal Scanner", "BMI Calculator", "Workout Plan"]
)

# ---------------- DASHBOARD ---------------- #
if page == "Dashboard":

    st.markdown('<div class="title">Cal AI Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Track your meals, calories and fitness goals with AI.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>🔥</h2>
            <h1>1850</h1>
            <p>Calories</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🥩</h2>
            <h1>120g</h1>
            <p>Protein</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <h2>💧</h2>
            <h1>3.2L</h1>
            <p>Water</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-card">
            <h2>⚡</h2>
            <h1>78%</h1>
            <p>Goal</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    st.markdown("""
    <div class="glass">
        <h3>📈 Daily Progress</h3>
        <p>Your calorie intake is within your target range today.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------------- MEAL SCANNER ---------------- #
elif page == "Meal Scanner":

    st.markdown('<div class="title">AI Meal Scanner</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Upload a meal image and let AI detect calories.</div>',
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

            if st.button("🔍 Scan Meal"):

                progress = st.progress(0)

                for i in range(100):
                    time.sleep(0.01)
                    progress.progress(i + 1)

                st.success("AI Scan Complete")

                # Dummy Results
                st.markdown("### 🍕 Detected Foods")
                st.write("- Pizza")
                st.write("- French Fries")
                st.write("- Cola")

                st.markdown("### 📊 Nutrition")
                st.write("Calories: 850 kcal")
                st.write("Protein: 24g")
                st.write("Carbs: 90g")
                st.write("Fat: 40g")

                st.markdown("### 🤖 AI Recommendation")
                st.info(
                    "High calorie meal detected. Consider adding more protein and vegetables."
                )

            st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BMI CALCULATOR ---------------- #
elif page == "BMI Calculator":

    st.markdown('<div class="title">BMI Calculator</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        weight = st.number_input("Weight (kg)", 30, 200)

    with col2:
        height = st.number_input("Height (cm)", 100, 250)

    if st.button("Calculate BMI"):

        bmi = weight / ((height / 100) ** 2)

        st.markdown(f"""
        <div class="glass">
            <h2>Your BMI: {bmi:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

        if bmi < 18.5:
            st.warning("Underweight")
        elif bmi < 25:
            st.success("Normal Weight")
        elif bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")

# ---------------- WORKOUT PLAN ---------------- #
elif page == "Workout Plan":

    st.markdown('<div class="title">AI Workout Recommendation</div>', unsafe_allow_html=True)

    goal = st.selectbox(
        "Select Goal",
        ["Fat Loss", "Muscle Gain", "Strength Training"]
    )

    if st.button("Generate Plan"):

        st.markdown('<div class="glass">', unsafe_allow_html=True)

        if goal == "Fat Loss":
            st.write("🏃 HIIT Cardio")
            st.write("🔥 Treadmill - 20 mins")
            st.write("💪 Pushups - 3x15")
            st.write("🦵 Squats - 3x20")

        elif goal == "Muscle Gain":
            st.write("🏋️ Bench Press - 4x10")
            st.write("💪 Deadlift - 4x8")
            st.write("🦵 Leg Press - 4x12")

        else:
            st.write("⚡ Powerlifting")
            st.write("🏋️ Squats - 5x5")
            st.write("💪 Bench Press - 5x5")
            st.write("🔥 Deadlift - 5x5")

        st.markdown('</div>', unsafe_allow_html=True)
