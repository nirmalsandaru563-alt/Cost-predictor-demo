import streamlit as st
import pandas as pd
import joblib

# 1. Load the saved AI Brain and the Column Structure
model = joblib.load('cost_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("🏗️ Construction Cost Predictor")

# 2. User Inputs
# IMPORTANT: These names can be whatever you want for the UI
p_type = st.selectbox("Select Project Type", ['Residential', 'Commercial', 'Industrial', 'Other'])
area = st.number_input("Floor Area (sqft)", value=1000)
floors = st.number_input("Number of Floors", min_value=1, value=1)

# 3. CREATE DATA FRAME (This is where we fix the error)
# We create an empty row with the EXACT columns the AI saw during training
input_df = pd.DataFrame(0, index=[0], columns=model_columns)

# 4. MAP USER INPUT TO THE AI COLUMNS
# We look for the exact names in 'model_columns' and fill them
if 'floor area' in input_df.columns:
    input_df['floor area'] = area
if 'nr of floors' in input_df.columns:
    input_df['nr of floors'] = floors

# Map the Project Type (This handles the 'One-Hot Encoding' error)
target_col = f"project type_{p_type.lower()}"
if target_col in input_df.columns:
    input_df[target_col] = 1

# 5. PREDICT
if st.button("Predict Cost"):
    try:
        # We ensure the columns are in the EXACT order the AI expects
        prediction = model.predict(input_df[model_columns])[0]
        st.success(f"### Estimated Cost: LKR {prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction Error: {e}")
        st.write("Columns expected by AI:", model_columns)
        st.write("Columns provided by App:", list(input_df.columns))
