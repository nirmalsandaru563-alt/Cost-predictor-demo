import streamlit as st
import pandas as pd
import joblib

# 1. Load files
model = joblib.load('cost_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("🏗️ QS Cost Predictor (M² / LKR Millions)")

# 2. User Inputs
p_type = st.selectbox("Project Type", ['Residential', 'Commercial', 'Industrial', 'Other'])
area = st.number_input("Floor Area (m²)", value=100.0)
floors = st.number_input("No. of Floors", min_value=1, value=1)

# 3. Create the input row with Zeros
input_df = pd.DataFrame(0, index=[0], columns=model_columns)

# 4. Map inputs (Using your EXACT Excel names)
if 'Floor Area (m²)' in input_df.columns:
    input_df['Floor Area (m²)'] = area
if 'No. of Floors' in input_df.columns:
    input_df['No_of_Floors'] = floors # If Excel had 'No. of Floors', use that exactly

# Map Project Type
target_col = f"Project Type_{p_type}"
if target_col in input_df.columns:
    input_df[target_col] = 1

# 5. Predict
if st.button("Calculate Estimate"):
    # Ensure columns match the training order
    prediction = model.predict(input_df[model_columns])[0]
    st.success(f"### Estimated Cost: {prediction:.2f} LKR Million")
    st.caption("Note: Prediction is based on the 'LKR Million' scale from your dataset.")
