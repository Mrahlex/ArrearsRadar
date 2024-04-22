
import streamlit as st
import joblib
import pandas as pd

# Load the saved pipeline
pipeline = joblib.load('pipeline.joblib')

# Define function to make prediction
def make_prediction(age, gender, employment_status, income_level, socio_economic_background, highest_education,
                    location, property_type, size, num_amenities, rental_price, property_age, property_condition,
                    tenancy_by_entirety, benefit_cap, satisfaction, timeliness_score, credit_score, household_size,
                    presence_of_guarantor, rental_price_income_ratio):
    # Prepare input data for prediction
    input_data = {
        'Tenant Age': age,
        'Gender': gender,
        'Employment Status': employment_status,
        'Income Level': income_level,
        'Socio-economic Background': socio_economic_background,
        'Highest Education': highest_education,
        'Location': location,
        'Property Type': property_type,
        'Property Size': size,
        'Num Amenities': num_amenities,
        'Rental Price': rental_price,
        'Property Age': property_age,
        'Property Condition': property_condition,
        'Tenancy by Entirety': tenancy_by_entirety,
        'Benefit Cap': benefit_cap,
        'Satisfaction': satisfaction,
        'Timeliness Score': timeliness_score,
        'Credit Score': credit_score,
        'Household Size': household_size,
        'Presence of Guarantor': presence_of_guarantor,
        'Rental Price to Income Ratio': rental_price_income_ratio
    }

    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])

    # Make prediction
    probability_arrears = pipeline.predict_proba(input_df)[:, 1]

    return f"The probability of the tenant running into arrears is: {probability_arrears[0]:.2%}"

# Streamlit app layout for risk prediction
def app():
    st.title('Tenant Arrears Prediction')
    st.write('Enter tenant details below to predict the probability of arrears.')

    # Input fields for tenant details
    with st.form("tenant_details_form"):
        st.header("Tenant Details")
        age = st.slider('Tenant Age', 18, 90, 50)
        gender = st.selectbox('Gender', ['Male', 'Female'])
        employment_status = st.selectbox('Employment Status', ['Employed', 'Unemployed', 'Student', 'Retired'])
        income_level = st.slider('Income Level', 10000, 140000, 70000)
        socio_economic_background = st.selectbox('Socio-economic Background', ['Low', 'Medium', 'High'])
        highest_education = st.selectbox('Highest Education', ['High School', 'Bachelor', 'Master', 'PhD'])
        location = st.selectbox('Location', ['Worcestershire', 'Shropshire', 'West Yorkshire', 'Surrey',
                                              'Wiltshire', 'West Sussex', 'Staffordshire', 'Somerset', 'West Midlands',
                                              'Rutland', 'Suffolk', 'South Yorkshire', 'Northumberland', 'Warwickshire',
                                              'Nottinghamshire', 'Tyne and Wear', 'Oxfordshire'])
        property_type = st.selectbox('Property Type', ['Apartment', 'House', 'Condominium'])
        size = st.slider('Property Size', 500, 3000, 1500)
        num_amenities = st.slider('Num Amenities', 1, 5, 3)
        rental_price = st.slider('Rental Price', 500, 3000, 1500)
        property_age = st.slider('Property Age', 1, 50, 20)
        property_condition = st.selectbox('Property Condition', ['New', 'Renovated', 'Outdated'])
        tenancy_by_entirety = st.selectbox('Tenancy by Entirety', ['Yes', 'No'])
        benefit_cap = st.selectbox('Benefit Cap', ['Yes', 'No'])
        satisfaction = st.slider('Satisfaction', 1, 5, 3)
        timeliness_score = st.slider('Timeliness Score', 0, 100, 50)
        credit_score = st.slider('Credit Score', 300, 850, 600)
        household_size = st.slider('Household Size', 1, 5, 3)
        presence_of_guarantor = st.selectbox('Presence of Guarantor', ['Yes', 'No'])
        rental_price_income_ratio = st.slider('Rental Price to Income Ratio', 0.1, 1.0, 0.5)
        submit_button = st.form_submit_button("Predict")

    # Button to make prediction
    if submit_button:
        prediction_result = make_prediction(age, gender, employment_status, income_level, socio_economic_background,
                                            highest_education, location, property_type, size, num_amenities,
                                            rental_price, property_age, property_condition, tenancy_by_entirety,
                                            benefit_cap, satisfaction, timeliness_score, credit_score, household_size,
                                            presence_of_guarantor, rental_price_income_ratio)
        st.success(prediction_result)
