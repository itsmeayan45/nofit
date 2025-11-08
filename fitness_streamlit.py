import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.graph_objects as go
import plotly.express as px
from io import StringIO

# -------------------------
# Page Configuration
# -------------------------
st.set_page_config(
    page_title="Chud AI - Professional Fitness & Nutrition Platform",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Custom CSS for Professional Styling
# -------------------------
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors - Black and Green */
    :root {
        --primary-color: #00ff88;
        --accent-color: #00cc6a;
        --success-color: #00ff88;
        --warning-color: #ffd700;
        --bg-dark: #0a0a0a;
        --bg-secondary: #1a1a1a;
        --bg-card: #141414;
        --text-primary: #ffffff;
        --text-secondary: #a0a0a0;
        --border-color: #2a2a2a;
    }
    
    /* Global styling */
    .stApp {
        background-color: var(--bg-dark);
        font-family: 'Inter', sans-serif;
    }
    
    /* Remove default Streamlit padding/margin */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 100%;
    }
    
    /* Header styling */
    .main-header {
        font-size: clamp(2rem, 5vw, 3rem);
        font-weight: 700;
        color: var(--primary-color);
        text-align: center;
        margin-top: 0;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
        text-transform: uppercase;
        padding-top: 0;
    }
    
    .sub-header {
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        color: var(--text-secondary);
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, var(--bg-secondary) 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        color: white;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.1);
        margin-bottom: 1rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
    }
    
    /* Section headers */
    .section-header {
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        font-weight: 600;
        color: var(--primary-color);
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Info boxes */
    .info-box {
        background-color: var(--bg-card);
        border-left: 4px solid var(--primary-color);
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
        color: var(--text-primary);
    }
    
    /* Workout day styling */
    .workout-day {
        background-color: var(--bg-card);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--primary-color);
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-sizing: border-box;
    }
    
    .workout-day:hover {
        border-left-width: 6px;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.15);
    }
    
    .workout-title {
        font-weight: 600;
        color: var(--primary-color);
        font-size: clamp(1rem, 2vw, 1.1rem);
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-primary);
    }
    
    /* Sidebar column alignment */
    [data-testid="stSidebar"] [data-testid="column"] {
        padding: 0.25rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="column"]:first-child {
        padding-left: 0 !important;
        padding-right: 0.25rem !important;
    }
    
    [data-testid="stSidebar"] [data-testid="column"]:last-child {
        padding-right: 0 !important;
        padding-left: 0.25rem !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        color: #000;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
        padding: 0.75rem 1rem;
        font-size: clamp(0.8rem, 2vw, 0.9rem);
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 16px rgba(0, 255, 136, 0.4);
        transform: translateY(-2px);
    }
    
    /* Input styling */
    .stTextInput input, .stNumberInput input, .stSelectbox select {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        font-size: clamp(0.85rem, 2vw, 1rem);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        background-color: var(--bg-card);
        width: 100%;
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        width: 100%;
    }
    
    /* Metric styling */
    [data-testid="stMetric"] {
        background-color: var(--bg-card);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        width: 100%;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary);
        font-size: clamp(0.75rem, 2vw, 0.9rem);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary-color);
        font-weight: 700;
        font-size: clamp(1.2rem, 3vw, 1.5rem);
    }
    
    /* Column responsiveness */
    [data-testid="column"] {
        width: 100% !important;
        flex: 1 1 auto !important;
        min-width: 0 !important;
        padding: 0.5rem !important;
    }
    
    /* Ensure columns stay aligned */
    [data-testid="column"] > div {
        width: 100%;
    }
    
    /* Fix column gaps */
    div[data-testid="column"]:first-child {
        padding-left: 0 !important;
    }
    
    div[data-testid="column"]:last-child {
        padding-right: 0 !important;
    }
    
    /* Info box responsiveness */
    .stAlert {
        width: 100%;
        font-size: clamp(0.85rem, 2vw, 1rem);
    }
    
    /* Ensure charts are responsive */
    .js-plotly-plot {
        width: 100% !important;
    }
    
    .plotly {
        width: 100% !important;
    }
    
    /* Hide Streamlit branding but keep the main menu visible so users can reopen the sidebar via the hamburger menu */
    /* Note: we intentionally do NOT hide #MainMenu — hiding it prevents reopening a closed sidebar */
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove top padding from main app */
    .main > div:first-child {
        padding-top: 0 !important;
    }
    
    /* Responsive padding */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2rem;
            margin-top: 0.5rem;
        }
        
        .sub-header {
            font-size: 0.9rem;
        }
        
        .workout-day {
            padding: 1rem;
        }
        
        [data-testid="stMetric"] {
            padding: 0.75rem;
        }
        
        .section-header {
            font-size: 1.2rem;
        }
        
        /* Stack columns on mobile */
        [data-testid="column"] {
            min-width: 100% !important;
            margin-bottom: 1rem;
        }
    }
    
    @media (max-width: 480px) {
        .main-header {
            font-size: 1.5rem;
        }
        
        .block-container {
            padding-left: 0.5rem;
            padding-right: 0.5rem;
        }
        
        .workout-day {
            padding: 0.75rem;
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.2rem;
        }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-color);
    }
</style>
""", unsafe_allow_html=True)


# -------------------------
# Compact Food DB
# -------------------------
FOOD_DB = [
    {"name": "Oats (1 cup cooked)", "cal": 150, "protein": 5, "carbs": 27, "fat": 3, "serving": "1 cup"},
    {"name": "Egg (large)", "cal": 78, "protein": 6, "carbs": 0.6, "fat": 5, "serving": "1 egg"},
    {"name": "Greek Yogurt (200g)", "cal": 120, "protein": 20, "carbs": 6, "fat": 0, "serving": "200 g"},
    {"name": "Chicken Breast (100g)", "cal": 165, "protein": 31, "carbs": 0, "fat": 3.6, "serving": "100 g"},
    {"name": "Brown Rice (1 cup cooked)", "cal": 215, "protein": 5, "carbs": 45, "fat": 1.8, "serving": "1 cup"},
    {"name": "Broccoli (1 cup)", "cal": 55, "protein": 3.7, "carbs": 11.2, "fat": 0.6, "serving": "1 cup"},
    {"name": "Salmon (100g)", "cal": 208, "protein": 20, "carbs": 0, "fat": 13, "serving": "100 g"},
    {"name": "Almonds (28g)", "cal": 164, "protein": 6, "carbs": 6, "fat": 14, "serving": "28 g"},
    {"name": "Apple (medium)", "cal": 95, "protein": 0.5, "carbs": 25, "fat": 0.3, "serving": "1 medium"},
    {"name": "Peanut Butter (2 tbsp)", "cal": 188, "protein": 8, "carbs": 7, "fat": 16, "serving": "2 tbsp"},
    {"name": "Whole Wheat Bread (1 slice)", "cal": 70, "protein": 3.6, "carbs": 12, "fat": 1, "serving": "1 slice"},
    {"name": "Banana (medium)", "cal": 105, "protein": 1.3, "carbs": 27, "fat": 0.3, "serving": "1 medium"},
    {"name": "Tofu (100g)", "cal": 76, "protein": 8, "carbs": 1.9, "fat": 4.8, "serving": "100 g"},
    {"name": "Olive Oil (1 tbsp)", "cal": 119, "protein": 0, "carbs": 0, "fat": 13.5, "serving": "1 tbsp"},
    {"name": "Quinoa (1 cup cooked)", "cal": 222, "protein": 8, "carbs": 39, "fat": 3.6, "serving": "1 cup"},
]
FOOD_DF = pd.DataFrame(FOOD_DB)


# -------------------------
# Activity & Goals
# -------------------------
ACTIVITY_FACTORS = {
    "Sedentary (little or no exercise)": 1.2,
    "Light (1-3 days/week)": 1.375,
    "Moderate (3-5 days/week)": 1.55,
    "Active (6-7 days/week)": 1.725,
    "Very active (hard exercise & physical work)": 1.9
}
GOAL_ADJUSTMENT = {
    "Lose weight (cut 20%)": 0.80,
    "Maintain weight": 1.00,
    "Gain weight (bulk 15%)": 1.15
}


# -------------------------
# Core Logic
# -------------------------
def calculate_bmr(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    if str(sex).lower().startswith('m'):
        return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161


def calculate_tdee_and_targets(sex, weight_kg, height_cm, age, activity_level, goal):
    bmr = calculate_bmr(sex, weight_kg, height_cm, age)
    activity_factor = ACTIVITY_FACTORS.get(activity_level, 1.375)
    tdee = bmr * activity_factor
    target_calories = tdee * GOAL_ADJUSTMENT.get(goal, 1.0)
    protein_g = round(2.0 * weight_kg) if "Lose" in goal else round(1.8 * weight_kg) if "Gain" in goal else round(1.6 * weight_kg)
    fat_cals = 0.25 * target_calories
    fat_g = round(fat_cals / 9)
    protein_cals = protein_g * 4
    remaining_cals = max(0, target_calories - (protein_cals + fat_cals))
    carbs_g = round(remaining_cals / 4)
    return {
        "BMR": round(bmr),
        "TDEE": round(tdee),
        "TargetCalories": round(target_calories),
        "Protein_g": int(protein_g),
        "Carbs_g": int(carbs_g),
        "Fat_g": int(fat_g)
    }


def generate_meal_plan(target_calories, protein_g, carbs_g, fat_g, meals=("Breakfast","Lunch","Dinner","Snack")):
    splits = {"Breakfast":0.25, "Lunch":0.35, "Dinner":0.30, "Snack":0.10}
    available = [m for m in meals if m]
    total_split = sum(splits[m] for m in available if m in splits)
    rows = []
    foods = FOOD_DF.copy()
    for meal in available:
        split = splits.get(meal, 0.15)
        meal_target = target_calories * (split / total_split)
        items = []; cal = prot = carb = fat = 0.0
        cand = foods.sort_values(by="cal") if meal == "Snack" else foods.assign(pdensity=foods["protein"]/(foods["cal"]+1e-6)).sort_values(by="pdensity", ascending=False)
        i = 0
        while cal < meal_target * 0.95 and i < len(cand):
            f = cand.iloc[i].to_dict()
            items.append(f)
            cal += f["cal"]; prot += f["protein"]; carb += f["carbs"]; fat += f["fat"]
            i += 1
        if cal < meal_target * 0.95:
            big = foods.sort_values(by="cal", ascending=False).iloc[0].to_dict()
            items.append(big); cal += big["cal"]; prot += big["protein"]; carb += big["carbs"]; fat += big["fat"]
        rows.append({"Meal": meal, "Items": items, "Calories": round(cal), "Protein_g": round(prot, 1), "Carbs_g": round(carb, 1), "Fat_g": round(fat, 1)})
    return pd.DataFrame(rows)


WORKOUT_TEMPLATES = {
    "beginner": [
        ("Day 1 - Full Body", ["Squats 3x8", "Push-ups 3x8", "Dumbbell Rows 3x8", "Plank 30s"]),
        ("Day 2 - Walk", ["30 min brisk walk"]),
        ("Day 3 - Full Body", ["Lunges 3x10", "Overhead Press 3x8"]),
        ("Day 4 - Recovery", ["Yoga / Mobility 20-30 min"]),
        ("Day 5 - Full Body", ["Goblet Squat 3x10", "Incline Push-ups 3x10"]),
        ("Day 6 - Cardio", ["20-30 min intervals"]),
        ("Day 7 - Rest", ["Rest"])
    ],
    "intermediate": [
        ("Day 1 - Upper Push", ["Bench Press 4x6-8", "Incline DB 3x8"]),
        ("Day 2 - Lower", ["Back Squat 4x6-8", "Deadlift 3x5"]),
        ("Day 3 - Pull/Core", ["Pull-ups 4x6", "Barbell Row 4x6"]),
        ("Day 4 - Recovery", ["Mobility"]),
        ("Day 5 - Push Hypertrophy", ["DB Press 4x10"]),
        ("Day 6 - Lower Hypertrophy", ["Lunges 3x12"]),
        ("Day 7 - Rest", ["Light walk"])
    ],
    "advanced": [
        ("Day 1 - Power", ["Power Cleans 5x3", "Box Jumps 4x5"]),
        ("Day 2 - Conditioning", ["HIIT 20 min"]),
        ("Day 3 - Strength", ["Deadlift 5x5", "Front Squat 4x6"]),
        ("Day 4 - Mobility", ["Yoga/Mobility 30 min"]),
        ("Day 5 - Speed/Agility", ["Sprints 8x60m"]),
        ("Day 6 - Mixed Strength", ["Bench 5x5", "Rows 4x6"]),
        ("Day 7 - Active Recovery", ["Light swim / walk"])
    ]
}


def generate_workout_plan(level, goal):
    template = WORKOUT_TEMPLATES.get(level, WORKOUT_TEMPLATES["beginner"])
    adapted = []
    for day, exs in template:
        ex = list(exs)
        if "Lose" in goal and not any(kw in e.lower() for e in ex for kw in ["cardio", "walk"]):
            ex.append("10-15 min cardio finisher")
        if "Gain" in goal:
            ex.append("Progressive overload: increase weight over weeks")
        adapted.append((day, ex))
    return adapted


def ai_diet_suggestions(targets, last_plan_df):
    tips = []
    tcal = targets.get("TargetCalories")
    if tcal and tcal < 1600:
        tips.append("Target calories are low — prioritize protein and nutrient-dense foods.")
    if targets and targets.get("Protein_g", 0) < 1:
        tips.append("Distribute protein across meals (20-30g per meal).")
    if last_plan_df is not None:
        for _, r in last_plan_df.iterrows():
            if any("Peanut Butter" in it["name"] and r["Meal"].lower().startswith("sn") for it in r["Items"]):
                tips.append("Swap some peanut-butter snacks for Greek yogurt + berries.")
                break
    tips.extend([
        "Include colored vegetables for vitamins and fiber.",
        "Stay hydrated (2-3 L/day depending on activity).",
        "For medical conditions, consult a dietitian."
    ])
    return tips


# -------------------------
# Initialize Session State
# -------------------------
if 'plan_generated' not in st.session_state:
    st.session_state.plan_generated = False
if 'meal_plan_df' not in st.session_state:
    st.session_state.meal_plan_df = None
if 'targets' not in st.session_state:
    st.session_state.targets = None
if 'workout_plan' not in st.session_state:
    st.session_state.workout_plan = None


# -------------------------
# Export Function
# -------------------------
def prepare_export_data():
    """Prepare data for CSV export"""
    if not st.session_state.meal_plan_df.empty:
        meal_plan_df = st.session_state.meal_plan_df
        targets = st.session_state.targets
        
        # Create export DataFrame
        export_rows = []
        for _, r in meal_plan_df.iterrows():
            items_str = "; ".join(f"{it['name']} ({it['serving']})" for it in r["Items"])
            export_rows.append({
                "Meal": r["Meal"],
                "Items": items_str,
                "Calories": r["Calories"],
                "Protein_g": r["Protein_g"],
                "Carbs_g": r["Carbs_g"],
                "Fat_g": r["Fat_g"]
            })
        
        export_df = pd.DataFrame(export_rows)
        
        # Create CSV with headers
        output = StringIO()
        output.write("# Chud AI - Personalized Nutrition Plan\n")
        output.write(f"# Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        for k, v in targets.items():
            output.write(f"# {k}: {v}\n")
        output.write("\n")
        export_df.to_csv(output, index=False)
        
        return output.getvalue()
    
    return ""


# -------------------------
# Main App
# -------------------------
def main():
    # Header
    st.markdown('<div class="main-header">CHUD AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Professional Fitness & Nutrition Platform</div>', unsafe_allow_html=True)
    
    # Sidebar - User Profile
    with st.sidebar:
        st.markdown("### USER PROFILE")
        
        name = st.text_input("Name", value="Ayan", key="name")
        
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, value=21, step=1)
            sex = st.selectbox("Sex", ["Male", "Female"])
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=64.0, step=0.1)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=173.0, step=0.1)
        
        experience = st.selectbox("Experience Level", ["beginner", "intermediate", "advanced"])
        activity_level = st.selectbox("Activity Level", list(ACTIVITY_FACTORS.keys()), index=2)
        goal = st.selectbox("Fitness Goal", list(GOAL_ADJUSTMENT.keys()), index=1)
        
        st.markdown("---")
        
        # Action Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("NUTRITION PLAN", use_container_width=True):
                with st.spinner("Calculating your personalized plan..."):
                    targets = calculate_tdee_and_targets(sex, weight, height, age, activity_level, goal)
                    meal_plan_df = generate_meal_plan(
                        targets["TargetCalories"], 
                        targets["Protein_g"], 
                        targets["Carbs_g"], 
                        targets["Fat_g"]
                    )
                    st.session_state.targets = targets
                    st.session_state.meal_plan_df = meal_plan_df
                    st.session_state.plan_generated = True
                    st.success("Plan generated successfully!")
                    st.rerun()
        
        with col2:
            if st.button("WORKOUT PLAN", use_container_width=True):
                with st.spinner("Creating your workout plan..."):
                    workout = generate_workout_plan(experience, goal)
                    st.session_state.workout_plan = workout
                    st.success("Workout plan ready!")
                    st.rerun()
        
        # Export Button
        if st.session_state.plan_generated:
            if st.button("EXPORT TO CSV", use_container_width=True):
                export_data = prepare_export_data()
                st.download_button(
                    label="Download Plan",
                    data=export_data,
                    file_name=f"chudai_plan_{datetime.datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        st.markdown("---")
        st.markdown("**Version 2.0** • Professional Guidelines")
        st.caption("Consult healthcare professionals for medical advice")
    
    # Main Content Area
    if st.session_state.plan_generated and st.session_state.targets:
        display_nutrition_plan()
    else:
        display_welcome_message()
    
    # Workout Section
    if st.session_state.workout_plan:
        display_workout_plan()
    
    # AI Suggestions
    if st.session_state.plan_generated:
        display_ai_suggestions()


def display_welcome_message():
    """Display welcome message when no plan is generated"""
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("**Step 1:** Fill in your profile details in the sidebar")
    with col2:
        st.info("**Step 2:** Click 'NUTRITION PLAN' to generate")
    with col3:
        st.info("**Step 3:** Get your personalized workout plan")
    
    st.markdown("---")
    
    # Feature highlights
    st.markdown("### PLATFORM FEATURES")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        **PERSONALIZED NUTRITION**
        - BMR & TDEE calculation
        - Macro distribution
        - Meal planning
        - Calorie tracking
        """)
    
    with col2:
        st.markdown("""
        **SMART WORKOUTS**
        - Level-based programs
        - Goal-oriented training
        - Progressive overload
        - Weekly schedules
        """)
    
    with col3:
        st.markdown("""
        **AI INSIGHTS**
        - Diet optimization tips
        - Hydration reminders
        - Health recommendations
        - Progress tracking
        """)


def display_nutrition_plan():
    """Display the nutrition plan with metrics and charts"""
    targets = st.session_state.targets
    meal_plan_df = st.session_state.meal_plan_df
    
    # Quick Stats Row
    st.markdown('<div class="section-header">NUTRITION TARGETS</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BMR", f"{targets['BMR']} kcal", help="Basal Metabolic Rate")
    with col2:
        st.metric("TDEE", f"{targets['TDEE']} kcal", help="Total Daily Energy Expenditure")
    with col3:
        st.metric("TARGET", f"{targets['TargetCalories']} kcal", help="Daily Calorie Target")
    with col4:
        bmi = round(st.session_state.get('weight', 70) / ((st.session_state.get('height', 172) / 100) ** 2), 1)
        st.metric("BMI", f"{bmi}", help="Body Mass Index")
    
    st.markdown("---")
    
    # Macros Row
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("PROTEIN", f"{targets['Protein_g']}g", f"{round(targets['Protein_g']*4/targets['TargetCalories']*100)}%")
    with col2:
        st.metric("CARBS", f"{targets['Carbs_g']}g", f"{round(targets['Carbs_g']*4/targets['TargetCalories']*100)}%")
    with col3:
        st.metric("FAT", f"{targets['Fat_g']}g", f"{round(targets['Fat_g']*9/targets['TargetCalories']*100)}%")
    
    st.markdown("---")
    
    # Charts Section
    st.markdown('<div class="section-header">DATA VISUALIZATION</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Macronutrient Pie Chart
        macro_data = {
            'Macronutrient': ['Protein', 'Carbs', 'Fat'],
            'Calories': [
                targets['Protein_g'] * 4,
                targets['Carbs_g'] * 4,
                targets['Fat_g'] * 9
            ]
        }
        
        fig_macro = go.Figure(data=[go.Pie(
            labels=macro_data['Macronutrient'],
            values=macro_data['Calories'],
            hole=0.4,
            marker=dict(colors=['#00ff88', '#00cc6a', '#00ff66']),
            textinfo='label+percent',
            textfont=dict(size=14, color='#ffffff')
        )])
        
        fig_macro.update_layout(
            title="Macronutrient Distribution",
            title_font=dict(color='#00ff88', size=16, family='Inter'),
            showlegend=True,
            height=400,
            margin=dict(t=50, b=20, l=20, r=20),
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff')
        )
        
        st.plotly_chart(fig_macro, use_container_width=True)
    
    with col2:
        # Calories per Meal Bar Chart
        fig_meal = go.Figure(data=[go.Bar(
            x=meal_plan_df['Meal'],
            y=meal_plan_df['Calories'],
            marker=dict(
                color=['#00ff88', '#00cc6a', '#00ff66', '#00dd77'],
                line=dict(color='#00ff88', width=2)
            ),
            text=meal_plan_df['Calories'],
            textposition='outside',
            textfont=dict(size=12, color='#ffffff')
        )])
        
        fig_meal.update_layout(
            title="Calories per Meal",
            title_font=dict(color='#00ff88', size=16, family='Inter'),
            xaxis_title="Meal",
            yaxis_title="Calories",
            height=400,
            margin=dict(t=50, b=50, l=50, r=20),
            showlegend=False,
            paper_bgcolor='#0a0a0a',
            plot_bgcolor='#0a0a0a',
            font=dict(color='#ffffff'),
            xaxis=dict(gridcolor='#2a2a2a'),
            yaxis=dict(gridcolor='#2a2a2a')
        )
        
        st.plotly_chart(fig_meal, use_container_width=True)
    
    # Detailed Meal Plan
    st.markdown('<div class="section-header">MEAL PLAN DETAILS</div>', unsafe_allow_html=True)
    
    # Create a display DataFrame with items as strings
    display_df = meal_plan_df.copy()
    display_df['Food Items'] = display_df['Items'].apply(
        lambda items: '; '.join([f"{it['name']} ({it['serving']})" for it in items])
    )
    display_df = display_df[['Meal', 'Food Items', 'Calories', 'Protein_g', 'Carbs_g', 'Fat_g']]
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Meal": st.column_config.TextColumn("Meal", width="medium"),
            "Food Items": st.column_config.TextColumn("Food Items", width="large"),
            "Calories": st.column_config.NumberColumn("Calories", format="%d kcal"),
            "Protein_g": st.column_config.NumberColumn("Protein", format="%.1f g"),
            "Carbs_g": st.column_config.NumberColumn("Carbs", format="%.1f g"),
            "Fat_g": st.column_config.NumberColumn("Fat", format="%.1f g"),
        }
    )


def display_workout_plan():
    """Display the workout plan"""
    st.markdown("---")
    st.markdown('<div class="section-header">WEEKLY WORKOUT PLAN</div>', unsafe_allow_html=True)
    
    workout = st.session_state.workout_plan
    
    # Workout suggestions based on day type
    workout_tips = {
        "full body": "Focus on compound movements. Rest 60-90 seconds between sets. Maintain proper form over heavy weight.",
        "upper push": "Target chest, shoulders, and triceps. Keep core engaged. Control the eccentric (lowering) phase.",
        "lower": "Prioritize form with squats and deadlifts. Warm up thoroughly. Keep back neutral throughout.",
        "pull": "Focus on back and biceps. Squeeze at peak contraction. Don't use momentum.",
        "core": "Engage abs throughout. Breathe steadily. Quality reps over quantity.",
        "walk": "Maintain a brisk pace. Keep posture upright. Great for active recovery and mental clarity.",
        "cardio": "Maintain target heart rate zone. Stay hydrated. Mix intensity levels for best results.",
        "recovery": "Focus on flexibility and mobility. Listen to your body. Essential for muscle repair.",
        "yoga": "Focus on breath control. Hold stretches 20-30 seconds. Great for flexibility and stress relief.",
        "mobility": "Dynamic stretching preferred. Focus on problem areas. Improves range of motion.",
        "rest": "Complete rest is crucial. Stay hydrated. Light walking is okay. Sleep 7-9 hours.",
        "power": "Explosive movements with proper form. Full recovery between sets (2-3 min). Focus on speed.",
        "conditioning": "High intensity, short rest. Push your limits safely. Improves cardiovascular endurance.",
        "strength": "Heavy weights, low reps. Rest 3-5 min between sets. Focus on progressive overload.",
        "speed": "Proper warm-up essential. Full recovery between sprints. Focus on technique and power.",
        "agility": "Quick directional changes. Stay light on feet. Improves coordination and reaction time.",
        "hypertrophy": "Moderate weight, higher reps (8-12). Rest 60-90 sec. Focus on muscle contraction and pump.",
        "active recovery": "Low intensity movement. Promotes blood flow. Helps reduce muscle soreness.",
    }
    
    def get_workout_tip(day_name):
        """Get relevant tip based on day name"""
        day_lower = day_name.lower()
        for key, tip in workout_tips.items():
            if key in day_lower:
                return tip
        return "Stay consistent, track progress, and adjust intensity as needed. Form first, weight second!"
    
    # Display in two columns with proper gap
    col1, col2 = st.columns(2, gap="medium")
    
    for idx, (day, exercises) in enumerate(workout):
        tip = get_workout_tip(day)
        with col1 if idx % 2 == 0 else col2:
            st.markdown(f"""
            <div class="workout-day">
                <div class="workout-title">{day}</div>
                <ul style="margin-left: 1.2rem; margin-top: 0.5rem; margin-bottom: 0.8rem;">
                    {''.join([f'<li style="margin-bottom: 0.3rem; color: #ffffff;">{ex}</li>' for ex in exercises])}
                </ul>
                <div style="font-size: 0.85rem; color: #a0a0a0; font-style: italic; padding-top: 0.5rem; border-top: 1px solid #2a2a2a;">
                    {tip}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # General Workout Tips
    st.markdown("---")
    st.markdown("### TRAINING GUIDELINES")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        **PROGRESSIVE OVERLOAD**
        - Gradually increase weight/reps
        - Track your progress
        - Aim for 2-5% weekly increase
        """)
    
    with col2:
        st.markdown("""
        **RECOVERY**
        - Sleep 7-9 hours nightly
        - Stretch after workouts
        - Listen to your body
        """)
    
    with col3:
        st.markdown("""
        **FORM & SAFETY**
        - Proper form prevents injury
        - Warm up before training
        - Use spotter for heavy lifts
        """)


def display_ai_suggestions():
    """Display AI-powered diet suggestions"""
    st.markdown("---")
    st.markdown('<div class="section-header">AI INSIGHTS & RECOMMENDATIONS</div>', unsafe_allow_html=True)
    
    targets = st.session_state.targets
    meal_plan_df = st.session_state.meal_plan_df
    
    suggestions = ai_diet_suggestions(targets, meal_plan_df)
    
    for suggestion in suggestions:
        st.markdown(f"""
        <div class="info-box">
            💡 {suggestion}
        </div>
        """, unsafe_allow_html=True)


# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    main()
