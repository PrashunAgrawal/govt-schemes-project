# # build_dataset.py
# import pandas as pd
# import joblib
# import numpy as np
#
# # Load model, encoders, and data
# model = joblib.load("eligibility_score_model.pkl")
# encoders = joblib.load("eligibility_label_encoders.pkl")
# df = pd.read_csv("dummy_aadhaar_income_data_with_mobile.csv")
# df.columns = df.columns.str.strip()
# df['mobile_no'] = df['mobile'].astype(str)
#
# def get_feature_scores(user):
#     scores = {}
#     if not pd.isna(user['age']):
#         scores['age'] = 0.2 * user['age']
#     if not pd.isna(user['annual_income']):
#         scores['annual_income'] = -0.00005 * user['annual_income']
#     if not pd.isna(user['gender']):
#         scores['gender'] = 5 if user['gender'].lower()=='female' else 0
#     if not pd.isna(user['caste_category']):
#         scores['caste_category'] = 10 if user['caste_category']=='SC' else 5 if user['caste_category']=='ST' else 3 if user['caste_category']=='OBC' else 0
#     if not pd.isna(user['state']):
#         scores['state'] = np.random.randint(0,5)
#     return scores
#
# def explain(scores):
#     parts = []
#     for feat, val in scores.items():
#         if val < 5:
#             parts.append(f"{feat} contributed only {val:.2f} pts")
#         else:
#             parts.append(f"{feat} contributed {val:.2f} pts")
#     return "; ".join(parts)
#
# out = []
# for _, row in df.iterrows():
#     user = row
#     raw_inputs = []
#     for feat in ['gender','age','annual_income','state','caste_category']:
#         v = user[feat]
#         if pd.isna(v): raw_inputs.append(0)
#         elif feat in encoders:
#             raw_inputs.append(encoders[feat].transform([v])[0])
#         else:
#             raw_inputs.append(v)
#     score = model.predict([raw_inputs])[0]
#     score = max(0, min(score,100))
#     feat_scores = get_feature_scores(user)
#     explanation = explain(feat_scores)
#     out.append({
#         "full_name": user['full_name'],
#         "mobile_no": user['mobile_no'],
#         "score": round(score,2),
#         "explanation": explanation
#     })
#
# pd.DataFrame(out).to_csv("eligibility_dataset.csv", index=False)
# print("✅ eligibility_dataset.csv generated.")
