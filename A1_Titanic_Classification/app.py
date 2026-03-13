import streamlit as st
import pandas as pd
import joblib
import random

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Titanic Survival Predictor",
    page_icon="🚢",
    layout="centered",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Google Font ---- */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Inter:wght@300;400;500&display=swap');

/* ---- Global ---- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- Hero header ---- */
.hero {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 1px solid rgba(201, 168, 76, 0.25);
    margin-bottom: 2rem;
}
.hero h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.6rem;
    color: #C9A84C;
    margin: 0;
    letter-spacing: 0.02em;
}
.hero p {
    color: #94A3B8;
    font-size: 0.95rem;
    font-weight: 300;
    margin-top: 0.5rem;
}

/* ---- Section labels ---- */
.section-label {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #C9A84C;
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
}

/* ---- Predict button ---- */
div.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #C9A84C, #a8893e);
    color: #0A1628;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.05em;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 0;
    margin-top: 1.5rem;
    transition: opacity 0.2s;
}
div.stButton > button:hover {
    opacity: 0.85;
    color: #0A1628;
}

/* ---- Result cards ---- */
.result-card {
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    margin-top: 2rem;
}
.result-survived {
    background: rgba(34, 197, 94, 0.08);
    border: 1px solid rgba(34, 197, 94, 0.35);
}
.result-died {
    background: rgba(239, 68, 68, 0.08);
    border: 1px solid rgba(239, 68, 68, 0.35);
}
.result-emoji {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.5rem;
}
.result-label {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 600;
    margin: 0;
}
.result-survived .result-label { color: #4ADE80; }
.result-died    .result-label { color: #F87171; }
.result-prob {
    font-size: 0.85rem;
    color: #94A3B8;
    margin-top: 0.5rem;
}
.result-message {
    font-size: 0.95rem;
    font-style: italic;
    color: #CBD5E1;
    margin-top: 0.6rem;
    margin-bottom: 0;
}

/* ---- Probability bar ---- */
.prob-bar-wrap {
    background: rgba(255,255,255,0.07);
    border-radius: 999px;
    height: 8px;
    margin: 1rem auto 0;
    max-width: 260px;
    overflow: hidden;
}
.prob-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.6s ease;
}
.prob-bar-survived { background: linear-gradient(90deg, #22c55e, #4ade80); }
.prob-bar-died     { background: linear-gradient(90deg, #ef4444, #f87171); }

/* ---- Divider ---- */
hr { border-color: rgba(201, 168, 76, 0.15); }
</style>
""", unsafe_allow_html=True)

# ── Model ──────────────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load('titanic_model.pkl')

model = load_model()

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🚢 Titanic Survival Predictor</h1>
    <p>Enter a passenger's details to estimate their survival probability using a trained ML model.</p>
</div>
""", unsafe_allow_html=True)

# ── Model explainer ───────────────────────────────────────────────────────────
with st.expander("How does the model work?"):
    st.markdown("""
    This app is powered by a **Random Forest** — a machine learning model trained on real data
    from the Titanic disaster (891 passengers, April 1912).

    **How it works:**
    A Random Forest builds hundreds of decision trees, each trained on a slightly different
    slice of the data. When you hit *Predict*, every tree casts a vote — survived or not —
    and the majority wins. The final probability score reflects how confident the model is.

    **What the model looks at:**
    - 🎫 **Ticket class & fare** — a proxy for wealth and deck location
    - 👤 **Sex & age** — the "women and children first" protocol was real and measurable
    - 👨‍👩‍👧 **Family size** — travelling alone vs. with family affected survival chances
    - ⚓ **Port of embarkation** — correlated with passenger socioeconomic profile

    **One derived feature:**
    The model also uses *Alone* — a custom binary feature engineered
    during training to capture the solo traveller effect more directly.

    **Output:**
    A probability between 0% and 100%, plus a binary prediction based on a 0.5 threshold.
    """)

# ── Form ───────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-label">Passenger Profile</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    pclass = st.selectbox(
        'Ticket Class',
        [1, 2, 3],
        format_func=lambda x: {1: '1st Class', 2: '2nd Class', 3: '3rd Class'}[x]
    )
    sex = st.selectbox('Sex', ['male', 'female'], format_func=str.capitalize)
    embarked = st.selectbox(
        'Port of Embarkation',
        ['Southampton', 'Cherbourg', 'Queenstown']
    )

with col2:
    age = st.slider('Age', 0, 80, 29)
    fare = st.number_input('Ticket Fare (USD)', 0.0, 512.0, 32.0, format="%.2f")
    st.caption('In 1912, the average 3rd class ticket cost ~£7 (~$36 today).')

st.markdown('<p class="section-label">Family aboard</p>', unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    sibsp = st.number_input('Siblings & Spouses', 0, 8, 0)
with col4:
    parch = st.number_input('Parents & Children', 0, 6, 0)

# ── Predict ────────────────────────────────────────────────────────────────────
if st.button('Predict Survival'):

    # Preprocessing
    sex_numeric = 1 if sex == 'female' else 0
    embarked_Q  = 1 if embarked == 'Queenstown'  else 0
    embarked_S  = 1 if embarked == 'Southampton' else 0
    alone       = 1 if (sibsp + parch) == 0      else 0

    feature_names = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'alone', 'embarked_Q', 'embarked_S']
    features_df = pd.DataFrame(
        [[pclass, sex_numeric, age, sibsp, parch, fare, alone, embarked_Q, embarked_S]],
        columns=feature_names
    )

    prediction  = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0]

    # Result messages
    survived_messages = [
        "The lifeboats had a seat with your name on it.",
        "Against all odds, you make it. History remembers the lucky ones.",
        "You would have stood on that deck in New York harbour. Alive.",
        "Fate was on your side. You survive to tell the tale.",
        "First class treatment — even from the Atlantic Ocean.",
        "You clearly knew which side of the ship to stand on.",
        "Rose would have made room on that door. For you, at least.",
        "The Atlantic tried. The Atlantic failed.",
        "You had the right name on the right manifest. Lucky you.",
        "Somewhere in an alternate 1912, you're sipping brandy in New York.",
    ]
    died_messages = [
        "You would have had an unscheduled meeting with the ocean floor.",
        "Turns out, \"unsinkable\" was a strong word. For you too.",
        "The iceberg: 1. Your survival odds: 0.",
        "You had the wrong ticket, the wrong deck, or just very bad luck.",
        "History would have remembered you as a statistic. A cold, wet one.",
        "You would have gone down with the ship. Literally.",
        "Not all stories have a happy ending. Yours is one of them.",
        "The ocean is vast. Your survival odds were not.",
        "They would have named a deckchair after you. Small comfort.",
        "Jack made it onto the door. You did not even get a door.",
    ]

    # Result card
    if prediction == 1:
        prob_pct   = probability[1] * 100
        card_class = "result-survived"
        bar_class  = "prob-bar-survived"
        emoji      = "🎉"
        label      = "Survived"
        message    = random.choice(survived_messages)
        prob_text  = f"Estimated survival probability: <strong>{prob_pct:.1f}%</strong>"
    else:
        prob_pct   = probability[0] * 100
        card_class = "result-died"
        bar_class  = "prob-bar-died"
        emoji      = "💀"
        label      = "Did Not Survive"
        message    = random.choice(died_messages)
        prob_text  = f"Estimated survival probability: <strong>{100 - prob_pct:.1f}%</strong>"

    st.markdown(f"""
    <div class="result-card {card_class}">
        <span class="result-emoji">{emoji}</span>
        <p class="result-label">{label}</p>
        <p class="result-message">{message}</p>
        <p class="result-prob">{prob_text}</p>
        <div class="prob-bar-wrap">
            <div class="prob-bar-fill {bar_class}" style="width:{prob_pct:.1f}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)