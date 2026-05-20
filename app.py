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

---

# 📦 Requirements (`requirements.txt`)

```txt
streamlit
pandas
numpy
opencv-python
pillow
tensorflow
```

---

# ▶️ Run The Project

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

# 🚀 Future AI Features You Can Add

## 1. AI Pose Detection

Use MediaPipe to check exercise form live through webcam.

## 2. Real-Time Calorie Burn Counter

Track workout movement and estimate calories burned.

## 3. AI Diet Planner

Generate personalized meals according to BMI and goals.

## 4. AI Chatbot Trainer

ChatGPT-like gym assistant inside MuscleMap.

## 5. Muscle Heatmap

Highlight muscles targeted during exercises.

## 6. Workout Streak System

Gamification with badges and rewards.

## 7. AI Progress Prediction

Predict body transformation after 30/60/90 days.

## 8. Smart Meal Portion Detection

Use YOLOv8 + Depth Estimation for accurate calories.

---

# 🧠 Best AI Upgrade (Production Level Food AI)

Most advanced calorie apps like Cal AI, HealthifyMe, and MyFitnessPal use:

* YOLOv8 for food object detection
* EfficientNet / Vision Transformers for food classification
* Food101 + Nutrition5k datasets
* Depth estimation for portion size
* OpenAI Vision / Gemini Vision APIs

---

# ✅ Best Algorithm For Your MuscleMap App

## Recommended AI Stack

### 1. YOLOv8 (Best Food Detection)

Use YOLOv8 to detect:

* Pizza
* Burger
* Rice
* Chicken
* Fruits
* Indian food
* Drinks
* Multiple food items in one image

Why YOLOv8?

* Extremely accurate
* Real-time detection
* Works on webcam + mobile
* Industry standard in 2025

Install:

```bash
pip install ultralytics
```

Example:

```python
from ultralytics import YOLO

model = YOLO("yolov8n.pt")
results = model("food.jpg")
results[0].show()
```

---

### 2. EfficientNet-B3 (Food Classification)

After YOLO detects food, EfficientNet identifies exact food type.

Example:

* Paneer Butter Masala
* Biryani
* Pasta
* Sandwich
* Salad

This gives much higher accuracy than MobileNet.

---

### 3. Nutrition5k Dataset (Calories)

Use Nutrition5k dataset for:

* calories
* protein
* carbs
* fats
* portion estimation

---

### 4. Segment Anything Model (SAM)

Use Meta SAM model to detect exact food boundaries.

This improves:

* calorie estimation
* plate segmentation
* multiple food detection

---

# 🚀 FINAL INDUSTRY LEVEL PIPELINE

```text
Image Upload
     ↓
YOLOv8 detects food objects
     ↓
EfficientNet classifies food
     ↓
SAM segments food portion
     ↓
Nutrition5k estimates calories
     ↓
AI generates meal report
```

---

# 🔥 Best Tech Stack For MuscleMap

| Feature                 | Best AI Model     |
| ----------------------- | ----------------- |
| Food Detection          | YOLOv8            |
| Food Classification     | EfficientNet-B3   |
| Portion Detection       | SAM               |
| Calories Estimation     | Nutrition5k       |
| Exercise Form Detection | MediaPipe         |
| AI Recommendations      | OpenAI/Gemini API |
| Workout Prediction      | XGBoost           |

---

# 🏆 Recommended Final Upgrade

Replace MobileNetV2 with:

```python
from ultralytics import YOLO
model = YOLO("best_food_model.pt")
```

This will improve your food detection accuracy massively and make MuscleMap look like a real startup-level AI fitness app.
