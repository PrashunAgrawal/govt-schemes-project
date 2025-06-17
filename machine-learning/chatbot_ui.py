# import pandas as pd
# import joblib
# import streamlit as st
#
# # Load trained model and encoders
# model = joblib.load("eligibility_score_model.pkl")
# encoders = joblib.load("eligibility_label_encoders.pkl")
#
# # Load Aadhaar mock data
# df = pd.read_csv("dummy_aadhaar_income_data_with_mobile.csv")
# df.columns = df.columns.str.strip()
# df['mobile_no'] = df['mobile'].astype(str).str.strip()
#
# # Streamlit UI
# st.set_page_config(page_title="Ladki Bhain Yojana Chatbot", page_icon="🤖")
# st.title("🤖 Majhi Ladki Bhain Yojana Assistant")
#
# mobile = st.text_input("📱 Enter your mobile number:")
#
# if mobile:
#     user_data = df[df['mobile_no'] == mobile.strip()]
#     if user_data.empty:
#         st.error("❌ No user found with this mobile number.")
#     else:
#         try:
#             user = user_data.iloc[0]
#             raw_inputs = {
#                 'gender': user['gender'],
#                 'age': user['age'],
#                 'annual_income': user['annual_income'],
#                 'state': user['state'],
#                 'caste_category': user['caste_category']
#             }
#
#             reasons = []
#             missing_penalty = 0
#             inputs = []
#
#             for feature in ['gender', 'age', 'annual_income', 'state', 'caste_category']:
#                 value = raw_inputs[feature]
#                 if pd.isna(value):
#                     inputs.append(0)
#                     missing_penalty += 10
#                     reasons.append(f"⚠️ Missing: {feature}")
#                 elif feature in encoders:
#                     encoded = encoders[feature].transform([value])[0]
#                     inputs.append(encoded)
#                 else:
#                     inputs.append(value)
#
#             # Predict score
#             score = model.predict([inputs])[0] - missing_penalty
#             score = max(0, min(score, 100))
#
#             st.success(f"✅ User: {user['full_name']}")
#             st.write(f"📊 **Eligibility Score**: `{score:.2f} / 100`")
#
#             if score >= 70:
#                 st.markdown("🎉 **Eligible for the scheme** 🎯")
#             elif score >= 50:
#                 st.markdown("🟡 **May be eligible. Please verify documents.**")
#             else:
#                 st.markdown("❌ **Not eligible based on current criteria.**")
#
#             if reasons:
#                 st.warning("📝 Influencing Factors:")
#                 for r in reasons:
#                     st.write(r)
#             else:
#                 st.info("👍 All required data was present and valid.")
#
#         except Exception as e:
#             st.error(f"⚠️ Error: {e}")

import pandas as pd
import joblib
import streamlit as st
import numpy as np

# Load model and encoders
model = joblib.load("eligibility_score_model.pkl")
encoders = joblib.load("eligibility_label_encoders.pkl")

# Load and clean dataset
df = pd.read_csv("dummy_aadhaar_income_data_with_mobile.csv")
df.columns = df.columns.str.strip()
df['mobile_no'] = df['mobile'].astype(str).str.strip()

# Scoring logic explanation helpers
def get_feature_scores(user):
    age = user['age']
    income = user['annual_income']
    gender = user['gender']
    caste = user['caste_category']
    state = user['state']

    scores = {}

    if pd.notna(age):
        scores['age'] = 0.2 * age
    if pd.notna(income):
        scores['annual_income'] = -0.00005 * income
    if pd.notna(gender):
        scores['gender'] = 5 if gender.lower() == 'female' else 5
    if pd.notna(caste):
        scores['caste_category'] = 10 if caste == 'SC' else 5 if caste == 'ST' else 3 if caste == 'OBC' else 0
    if pd.notna(state):
        scores['state'] = np.random.randint(0, 5)

    return scores

def calculate_score(user):
    raw_inputs = {
        'gender': user['gender'],
        'age': user['age'],
        'annual_income': user['annual_income'],
        'state': user['state'],
        'caste_category': user['caste_category']
    }

    inputs = []
    missing_penalty = 0
    missing_reasons = []

    for feature in ['gender', 'age', 'annual_income', 'state', 'caste_category']:
        value = raw_inputs[feature]
        if pd.isna(value):
            inputs.append(0)
            missing_penalty += 10
            missing_reasons.append(f" Missing value for: {feature}")
        elif feature in encoders:
            inputs.append(encoders[feature].transform([value])[0])
        else:
            inputs.append(value)

    predicted_score = model.predict([inputs])[0]
    final_score = max(0, min(predicted_score - missing_penalty, 100))
    return final_score, missing_penalty, missing_reasons

# Streamlit UI
st.set_page_config(page_title="Majhi Ladki Bhain Yojana Assistant")
st.title("Majhi Ladki Bhain Yojana Assistant")
st.write("Check your eligibility score and see what's affecting it.")

mobile = st.text_input("📱 Enter your mobile number:")

if mobile:
    user_data = df[df['mobile_no'] == mobile.strip()]

    if user_data.empty:
        st.error("❌ No user found with this mobile number.")
    else:
        user = user_data.iloc[0]
        st.success(f" User: {user['full_name']}")

        score, penalty, reasons = calculate_score(user)
        st.metric("Eligibility Score", f"{score:.2f}/100")

        if score >= 70:
            st.success(" Eligible for the scheme ")
        elif score >= 50:
            st.warning(" May be eligible. Please verify documents.")
        else:
            st.error("❌ Not eligible based on current criteria.")

        if score < 70:
            st.subheader(" Factors that reduced your score:")
            reasons = reasons or []

            feature_scores = get_feature_scores(user)
            for feature, points in feature_scores.items():
                if points < 5:
                    reasons.append(f" Low score for {feature}: {points:.2f} points")

            for reason in reasons:
                st.write(reason)
        else:
            st.info(" All required data was present and contributed well.")

