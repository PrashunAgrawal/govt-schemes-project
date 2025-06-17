# import pandas as pd
# import joblib
#
# # 1. Load trained model and encoders
# model = joblib.load("eligibility_score_model.pkl")
# encoders = joblib.load("eligibility_label_encoders.pkl")
#
# # 2. Load Aadhaar mock data
# df = pd.read_csv("dummy_aadhaar_income_data_with_mobile.csv")
#
# # 3. Clean column names and mobile number format
# df.columns = df.columns.str.strip()
# df['mobile_no'] = df['mobile'].astype(str).str.strip()
#
# # 4. Chatbot function
# def chatbot():
#     print("🤖 Welcome to the Majhi Ladki Bhain Yojana Assistant")
#
#     while True:
#         mobile = input("\n📱 Enter your mobile number (or type 'exit'): ").strip()
#         if mobile.lower() == 'exit':
#             print("👋 Thank you! Stay safe.")
#             break
#
#         # Check if user exists
#         user_data = df[df['mobile_no'] == mobile]
#
#         if user_data.empty:
#             print("❌ No user found with this mobile number.")
#             continue
#
#         try:
#             user = user_data.iloc[0]
#
#             # Extract & transform input features
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
#
#             # Encode features
#             inputs = []
#             for feature in ['gender', 'age', 'annual_income', 'state', 'caste_category']:
#                 value = raw_inputs[feature]
#
#                 if pd.isna(value):
#                     inputs.append(0)
#                     missing_penalty += 10
#                     reasons.append(f"⚠️ Missing value for: {feature}")
#                 elif feature in encoders:
#                     encoded = encoders[feature].transform([value])[0]
#                     inputs.append(encoded)
#                 else:
#                     inputs.append(value)
#
#             # Predict eligibility score
#             score = model.predict([inputs])[0] - missing_penalty
#             score = max(0, min(score, 100))
#
#             print(f"\n✅ User: {user['full_name']}")
#             print(f"📊 Eligibility Score: {score:.2f}/100")
#
#             if score >= 70:
#                 print("🎉 Eligible for the scheme 🎯")
#             elif score >= 50:
#                 print("🟡 May be eligible. Please verify documents.")
#             else:
#                 print("❌ Not eligible based on current criteria.")
#
#             if reasons:
#                 print("\n📝 Influencing Factors:")
#                 for r in reasons:
#                     print(r)
#             else:
#                 print("\n👍 All required data was present and valid.")
#
#         except Exception as e:
#             print(f"⚠️ Error while processing user data: {e}")
#
#
# # 5. Run chatbot
# if __name__ == "__main__":
#     chatbot()
