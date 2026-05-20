import streamlit as st
from PIL import Image
from groq import Groq
import io
import time

# ================= PAGE CONFIG ================= #

st.set_page_config(
    page_title="Cal AI",
    page_icon="🍱",
    layout="wide"
)

# ================= GROQ API ================= #

try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

    client = Groq(
        api_key=GROQ_API_KEY
    )

except Exception as e:
    st.error("Groq API Setup Error")
    st.code(str(e))
    st.stop()

# ================= CUSTOM CSS ================= #

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
    background-color: #0E1117;
    color: white;
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

.result-card {
    background: rgba(255,255,255,0.05);
    padding: 25px;
    border-radius: 25px;
    border: 1px solid rgba(255,255,255,0.08);
    line-height: 1.8;
    font-size: 17px;
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
        '<div class="subtitle">Personalized Fitness & Nutrition Tracker</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col_left, col_right = st.columns(2)

    with col_left:

        age = st.number_input(
            "Age",
            min_value=10,
            max_value=100,
            value=22
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female"]
        )

    with col_right:

        height = st.number_input(
            "Height (cm)",
            min_value=100,
            max_value=250,
            value=170
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=20,
            max_value=250,
            value=70
        )

    st.write("")

    # BMI Calculation

    bmi = weight / ((height / 100) ** 2)

    # BMI Category + Calorie Goal

    if bmi < 18.5:
        category = "Underweight"
        calorie_goal = weight * 35
        goal = "Weight Gain"

    elif bmi < 25:
        category = "Normal"
        calorie_goal = weight * 30
        goal = "Maintain Fitness"

    elif bmi < 30:
        category = "Overweight"
        calorie_goal = weight * 25
        goal = "Fat Loss"

    else:
        category = "Obesity"
        calorie_goal = weight * 22
        goal = "Weight Reduction"

    # Daily Nutrition Requirements

    protein = round(weight * 1.6)
    carbs = round(weight * 4)
    water = round(weight * 0.035, 1)

    # Dashboard Cards

    col1, col2, col3, col4 = st.columns(4)

    cards = [
        ("🔥", f"{int(calorie_goal)} kcal", "Calories"),
        ("🥩", f"{protein} gm", "Protein"),
        ("🍞", f"{carbs} gm", "Carbs"),
        ("💧", f"{water} L", "Water")
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

    st.write("")

    st.markdown(
        f"""
        <div class="result-card">

        <h2>📊 BMI Analysis</h2>

        <h3>BMI Score: {bmi:.1f}</h3>

        <h3>Category: {category}</h3>

        <h3>🎯 Goal: {goal}</h3>

        <hr>

        <h3>💪 Daily Nutrition Recommendation</h3>

        <ul>
            <li>🔥 Calories Needed: <b>{int(calorie_goal)} kcal/day</b></li>
            <li>🥩 Protein Needed: <b>{protein} gm/day</b></li>
            <li>🍞 Carbohydrates Needed: <b>{carbs} gm/day</b></li>
            <li>💧 Water Intake Needed: <b>{water} liters/day</b></li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )

# ================= AI MEAL SCANNER ================= #

elif menu == "AI Meal Scanner":

    st.markdown(
        '<div class="title">AI Meal Scanner</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Upload food image and get nutrition analysis</div>',
        unsafe_allow_html=True
    )

    st.write("")

    uploaded_file = st.file_uploader(
        "Upload Meal Image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        try:

            image = Image.open(uploaded_file).convert("RGB")

            col1, col2 = st.columns([1, 1])

            with col1:

                st.image(
                    image,
                    use_container_width=True
                )

            with col2:

                st.markdown(
                    '<div class="glass">',
                    unsafe_allow_html=True
                )

                if st.button("🔍 Analyze Meal"):

                    with st.spinner("Analyzing Meal..."):

                        progress = st.progress(0)

                        for i in range(100):
                            time.sleep(0.01)
                            progress.progress(i + 1)

                        buffered = io.BytesIO()
                        image.save(buffered, format="JPEG")

                        prompt = """
                        You are an AI nutrition expert.

                        Analyze the uploaded meal image carefully.

                        IMPORTANT:
                        - Keep response short and clean.
                        - Give approximate nutrition values.
                        - Format exactly like below.

                        Example Format:

                        🍕 Food Name:
                        Pizza, Fries, Cold Drink

                        🥩 Protein:
                        10 gm

                        🍞 Carbohydrates:
                        45 gm

                        🧈 Fat:
                        15 gm

                        🔥 Calories:
                        550 kcal

                        ❤️ Healthy or Unhealthy:
                        This meal is high in calories and fats.
                        Eating it occasionally is fine.

                        Only follow this format.
                        """

                        try:

                            response = client.chat.completions.create(
                                model="llama-3.3-70b-versatile",
                                messages=[
                                    {
                                        "role": "user",
                                        "content": prompt
                                    }
                                ],
                                temperature=0.5,
                                max_tokens=400
                            )

                            result = response.choices[0].message.content

                            st.success("✅ AI Scan Complete")

                            st.markdown("## 🤖 AI Analysis")

                            st.markdown(
                                f"""
                                <div class="result-card">
                                {result}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                        except Exception as e:

                            st.error("Groq API Error")
                            st.code(str(e))

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )

        except Exception as e:

            st.error("Image Upload Error")
            st.code(str(e))

# ================= BMI CALCULATOR ================= #

elif menu == "BMI Calculator":

    st.markdown(
        '<div class="title">BMI Calculator</div>',
        unsafe_allow_html=True
    )

    st.write("")

    left_col, right_col = st.columns([1, 1.2])

    with left_col:

        st.markdown(
            '<div class="glass">',
            unsafe_allow_html=True
        )

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

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )

    with right_col:

        if calculate:

            bmi = weight / ((height / 100) ** 2)

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

            st.markdown(
                '<div class="result-card">',
                unsafe_allow_html=True
            )

            st.markdown(f"""
            <h1>BMI = {bmi:.1f} kg/m²</h1>
            <h2 style="color:{color};">{category}</h2>
            """, unsafe_allow_html=True)

            healthy_min = 18.5 * ((height / 100) ** 2)
            healthy_max = 25 * ((height / 100) ** 2)

            st.markdown(f"""
            ### 📌 Health Information

            - Healthy BMI Range:
              **18.5 - 25**

            - Healthy Weight:
              **{healthy_min:.1f} kg - {healthy_max:.1f} kg**

            - BMI Category:
              **{category}**

            - Gender:
              **{gender}**
            """)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )
