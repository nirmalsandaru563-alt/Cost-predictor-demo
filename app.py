import streamlit as st
import pandas as pd
import joblib

# 1. Load the saved AI Brain
model = joblib.load('cost_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("Construction Cost Predictor")

# 2. User Inputs (Matching your Excel format)
p_type = st.selectbox("Select Project Type", ['Residential', 'Commercial', 'Industrial', 'Other'])
area = st.number_input("Floor Area (sqft)", value=1000)
floors = st.number_input("Number of Floors", min_value=1, value=1)

# 3. Logic to translate User Input for the AI
input_data = pd.DataFrame([[area, floors]], columns=['floor area', 'nr of floors'])
for col in model_columns:
    if "project type_" in col:
        input_data[col] = 1 if col == f"project type_{p_type}" else 0

# 4. Make the Prediction
if st.button("Predict Cost"):
    prediction = model.predict(input_data)[0]
    st.header(f"Estimated Cost: LKR {prediction:,.2f}")
