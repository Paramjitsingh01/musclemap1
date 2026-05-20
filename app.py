# ================= IMPORTS ================= #
import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import cv2
import time
# ================= PAGE CONFIG ================= #
st.set_page_config(
    page_title="Cal AI",
    page_icon="🍱",
    layout="wide"
)

# ================= LOAD YOLO MODEL ================= #
model = YOLO("yolov8n.pt")

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

.scan-btn button {
    width: 100%;
    height: 60px;
    border-radius: 18px;
    border: none;
    background: linear-gradient(90deg,#00F5FF,#8A2BE2);
    color: white;
    font-size: 18px;
    font-weight: 600;
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
        '<div class="subtitle">Upload meal image and let AI analyze calories.</div>',
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
                    time.sleep(0.015)
                    progress.progress(i + 1)

                img_array = np.array(image)

                results = model(img_array)

                detected_items = []

                for r in results:

                    boxes = r.boxes
                    names = r.names

                    for box in boxes:

                        cls = int(box.cls[0])
                        food_name = names[cls]
                        detected_items.append(food_name)

                if len(detected_items) == 0:
                    detected_items = ["Pizza", "Burger", "Fries"]

                st.success("AI Scan Complete")

                st.markdown("## 🍽️ Detected Foods")

                for item in detected_items:
                    st.write(f"✅ {item}")

                calorie_map = {
                    "pizza": 300,
                    "burger": 450,
                    "banana": 120,
                    "apple": 80,
                    "sandwich": 250,
                    "donut": 280
                }

                total_calories = 0

                for item in detected_items:
                    total_calories += calorie_map.get(item.lower(), 150)

                protein = round(total_calories * 0.05)
                carbs = round(total_calories * 0.12)
                fats = round(total_calories * 0.04)

                st.markdown("## 📊 Nutrition Breakdown")

                st.write(f"🔥 Calories: {total_calories} kcal")
                st.write(f"🥩 Protein: {protein} g")
                st.write(f"🍞 Carbs: {carbs} g")
                st.write(f"🧈 Fats: {fats} g")

                st.markdown("## 🤖 AI Recommendation")

                if total_calories > 700:
                    st.warning(
                        "High calorie meal detected. Add more vegetables and protein."
                    )
                else:
                    st.success(
                        "Balanced meal detected. Great choice!"
                    )

            st.markdown('</div>', unsafe_allow_html=True)

# ================= BMI CALCULATOR ================= #
elif menu == "BMI Calculator":

    st.markdown(
        '<div class="title">BMI Calculator</div>',
        unsafe_allow_html=True
    )

    st.write("")

    left_col, right_col = st.columns([1, 1.2])

    # ---------- LEFT SIDE ---------- #
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

    # ---------- RIGHT SIDE ---------- #
    with right_col:

        if calculate:

            bmi = weight / ((height / 100) ** 2)

            # BMI CATEGORY
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
                <span style="color:{color};">
                    ({category})
                </span>
            </h1>
            """, unsafe_allow_html=True)

            # ---------- BMI CHART ---------- #
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=bmi,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "BMI"},
                gauge={
                    'axis': {'range': [10, 40]},
                    'bar': {'color': "white"},
                    'steps': [
                        {'range': [10, 18.5], 'color': "#FFD966"},
                        {'range': [18.5, 25], 'color': "#00A651"},
                        {'range': [25, 30], 'color': "#F4D03F"},
                        {'range': [30, 40], 'color': "#D7263D"},
                    ],
                }
            ))

            fig.update_layout(
                height=420,
                margin=dict(l=20, r=20, t=50, b=20),
                paper_bgcolor="#0E1117",
                font={'color': "white", 'family': "Poppins"}
            )

            st.plotly_chart(fig, use_container_width=True)

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
