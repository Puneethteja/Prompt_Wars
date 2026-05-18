import streamlit as st
import joblib
import re
import random
import pandas as pd

st.set_page_config(
    page_title="PromptWars",
    page_icon="⚔️",
    layout="centered"
)

model = joblib.load(".dist/models/detector.pkl")

vectorizer = joblib.load(".dist/models/vectorizer.pkl")

df = pd.read_csv(
    ".dist\detector\dataset.csv",
    encoding="utf-8"
)

malicious_df = df[df["label"] == 1]

attack_prompts = malicious_df["prompt"].tolist()

def normalize_text(text):

    text = text.lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()

def predict_prompt(prompt):

    normalized = normalize_text(prompt)

    vectorized = vectorizer.transform([normalized])

    prediction = model.predict(vectorized)[0]

    probability = model.predict_proba(vectorized)[0]

    risk_score = round(probability[1] * 100, 2)

    return prediction, risk_score

def mutate_attack(text):

    replacements = {
        "a": "4",
        "e": "3",
        "i": "1",
        "o": "0",
        "s": "5"
    }

    mutated = ""

    for char in text:

        if char.lower() in replacements and random.random() > 0.5:

            mutated += replacements[char.lower()]

        else:

            mutated += char

    return mutated

st.title("⚔️ PromptWars")

st.subheader(
    "Adversarial Prompt Injection Detection System"
)

st.write(
    """
    PromptWars detects malicious prompts,
    jailbreak attempts, and prompt injections
    using machine learning.
    """
)

user_prompt = st.text_area(
    "Enter Prompt",
    height=180
)

if st.button("Analyze Prompt"):

    if user_prompt.strip() == "":

        st.warning("Please enter a prompt.")

    else:

        prediction, risk_score = predict_prompt(
            user_prompt
        )

        st.markdown("## Detection Result")

        if prediction == 1:

            st.error(
                "⚠️ Malicious Prompt Detected"
            )

        else:

            st.success(
                "✅ Safe Prompt"
            )

        st.metric(
            "Risk Score",
            f"{risk_score}%"
        )

st.markdown("---")

st.markdown("## Red Team Attack Generator")

if st.button("Generate Attack"):

    attack = random.choice(attack_prompts)

    mutated_attack = mutate_attack(attack)

    st.code(mutated_attack)

    prediction, risk_score = predict_prompt(
        mutated_attack
    )

    st.markdown("### Detector Response")

    if prediction == 1:

        st.error("⚠️ Attack Detected")

    else:

        st.success("🚨 Detector Bypassed")

    st.metric(
        "Risk Score",
        f"{risk_score}%"
    )

st.markdown("---")

st.caption(
    "PromptWars • AI Prompt Security System"
)