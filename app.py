# MuscleMap AI — `app.py`

```python
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import cv2
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
from tensorflow.keras.applications import MobileNetV2

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="MuscleMap AI",
    page_icon="💪",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown(
    """
    <style>
    .main {
        background-color: #0b0f1a;
        color: white;
    }

    .stButton>button {
        background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
        color: white;
        border-radius: 12px;
        height: 50px;
        width: 100%;
        border: none;
        font-size: 18px;
        font-weight: bold;
    }

    .metric-box {
        background: #151a2d;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0px 4px 20px rgba(255,255,255,0.05);
    }

    .goal-card {
        background: #111827;
        padding: 20px;
        border-radius: 20px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# TITLE
# -----------------------------
st.title("💪 MuscleMap AI")
st.caption("AI Powered Fitness + Meal Calories Detector")

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("⚡ Navigation")
page = st.sidebar.radio(
    "Choose Feature",
    [
        "🏋️ AI Fitness Planner",
        "🍔 AI Meal Calories Detector",
        "📊 Progress Dashboard"
    ]
)

# -----------------------------
# BMI FUNCTION
# -----------------------------
def calculate_bmi(weight, height_cm):
    height_m = height_cm / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)

# -----------------------------
# BMI CATEGORY
# -----------------------------
def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# -----------------------------
# AI WORKOUT RECOMMENDATIONS
# -----------------------------
def get_workout(goal, experience):

    workouts = {
        "Weight Loss": {
            "Beginner": [
                "Walking - 30 mins",
                "Jump Rope - 10 mins",
                "Bodyweight Squats - 3x12",
                "Pushups - 3x10",
                "Cycling"
            ],
            "Intermediate": [
                "HIIT Workout",
                "Running - 5 KM",
                "Burpees - 4x15",
                "Mountain Climbers",
                "Core Workout"
            ],
            "Advanced": [
                "CrossFit",
                "Sprint Training",
                "Battle Ropes",
                "Weighted Circuits",
                "Athletic Conditioning"
            ]
        },

        "Muscle Gain": {
            "Beginner": [
                "Bench Press",
                "Lat Pulldown",
                "Shoulder Press",
                "Leg Press",
                "Protein Rich Diet"
            ],
            "Intermediate": [
                "Deadlifts",
                "Incline Dumbbell Press",
                "Barbell Rows",
                "Bulgarian Squats",
                "Pullups"
            ],
            "Advanced": [
                "Powerlifting",
                "Heavy Squats",
                "Olympic Lifting",
                "Weighted Pullups",
                "Advanced Hypertrophy"
            ]
        },

        "Strength Training": {
            "Beginner": [
                "Pushups",
                "Plank",
                "Dumbbell Press",
                "Goblet Squat",
                "Resistance Band Workout"
            ],
            "Intermediate": [
                "Bench Press",
                "Deadlifts",
                "Barbell Squats",
                "Military Press",
                "Weighted Dips"
            ],
            "Advanced": [
                "Powerlifting Program",
                "Heavy Deadlifts",
                "Front Squats",
                "Clean and Jerk",
                "Athlete Conditioning"
            ]
        }
    }

    return workouts[goal][experience]

# -----------------------------
# FITNESS PAGE
# -----------------------------
if page == "🏋️ AI Fitness Planner":

    st.header("🔥 Build Your AI Fitness Plan")

    col1, col2, col3 = st.columns(3)

    with col1:
        age = st.number_input("Age", 15, 80, 22)
        gender = st.selectbox("Gender", ["Male", "Female"])

    with col2:
        height = st.number_input("Height (cm)", 120, 250, 170)
        weight = st.number_input("Weight (kg)", 30.0, 200.0, 70.0)

    with col3:
        goal = st.selectbox(
            "Primary Goal",
            ["Weight Loss", "Muscle Gain", "Strength Training"]
        )

        experience = st.selectbox(
            "Gym Experience",
            ["Beginner", "Intermediate", "Advanced"]
        )

    if st.button("🚀 Generate AI Plan"):

        bmi = calculate_bmi(weight, height)
        category = bmi_category(bmi)

        st.markdown("---")

        colA, colB = st.columns(2)

        with colA:
            st.markdown(
                f"""
                <div class='metric-box'>
                    <h2>📊 Your BMI</h2>
                    <h1>{bmi}</h1>
                    <h3>{category}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        with colB:
            if goal == "Weight Loss":
                calories = int(weight * 24 - 500)
            elif goal == "Muscle Gain":
                calories = int(weight * 24 + 350)
            else:
                calories = int(weight * 24)

            st.markdown(
                f"""
                <div class='metric-box'>
                    <h2>🍽️ Recommended Calories</h2>
                    <h1>{calories} kcal/day</h1>
                    <h3>Based on your goal</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("## 🤖 AI Recommended Exercises")

        workouts = get_workout(goal, experience)

        for workout in workouts:
            st.success(workout)

        st.markdown("## 🥗 AI Diet Suggestion")

        if goal == "Weight Loss":
            st.info("High protein + low calorie meals. Avoid sugary drinks.")

        elif goal == "Muscle Gain":
            st.info("Increase protein intake, healthy carbs, and calorie surplus.")

        else:
            st.info("Balanced protein, carbs, and healthy fats.")

# -----------------------------
# MEAL DETECTOR
# -----------------------------
elif page == "🍔 AI Meal Calories Detector":

    st.header("🍕 AI Meal Calories Detector")

    st.write(
        "Upload a meal image and AI will try to detect the food and estimate calories."
    )

    uploaded_file = st.file_uploader(
        "Upload Meal Image",
        type=["jpg", "jpeg", "png"]
    )

    # LOAD MODEL
    model = MobileNetV2(weights="imagenet")

    calorie_database = {
        "pizza": 285,
        "burger": 295,
        "hotdog": 290,
        "icecream": 207,
        "banana": 89,
        "apple": 52,
        "orange": 47,
        "sandwich": 250,
        "spaghetti": 158,
        "french_loaf": 250
    }

    if uploaded_file:

        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Meal", use_container_width=True)

        img = np.array(image)
        img = cv2.resize(img, (224, 224))

        img_array = np.expand_dims(img, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)
        decoded = decode_predictions(predictions, top=3)[0]

        st.subheader("🔍 AI Predictions")

        detected_food = decoded[0][1]

        for pred in decoded:
            st.write(f"{pred[1]} — Confidence: {round(pred[2]*100,2)}%")

        calories = calorie_database.get(detected_food, 200)

        st.markdown("---")

        st.markdown(
            f"""
            <div class='metric-box'>
                <h2>Estimated Meal Calories</h2>
                <h1>{calories} kcal</h1>
                <h3>{detected_food}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "AI calories are estimated values and may vary depending on portion size."
        )

# -----------------------------
# DASHBOARD
# -----------------------------
elif page == "📊 Progress Dashboard":

    st.header("📈 Fitness Progress Dashboard")

    progress_data = {
        "Week": [1, 2, 3, 4, 5],
        "Weight": [78, 77, 76, 75, 74],
        "Calories Burned": [2000, 2400, 2800, 3200, 3500]
    }

    df = pd.DataFrame(progress_data)

    st.subheader("🏋️ Weight Progress")
    st.line_chart(df.set_index("Week")["Weight"])

    st.subheader("🔥 Calories Burned")
    st.bar_chart(df.set_index("Week")["Calories Burned"])

    st.dataframe(df)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit + OpenCV + TensorFlow")
```



# 📦 Requirements (`requirements.txt`)

