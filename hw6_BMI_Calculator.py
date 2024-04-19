import streamlit as st

height = st.number_input('Height:')

height_unit = st.radio(
    "Select the unit for height",
    ('feet', 'meters'))

weight = st.number_input('Weight:')

weight_unit = st.radio(
    "Select the unit for weight",
    ('lbs', 'kilograms'))

def calculate_bmi(height, weight, height_unit, weight_unit):
    # change feet to meters
    if height_unit == "feet":
        height = height * 0.3048
    # change lbs to kilograms
    if weight_unit == "lbs":
        weight = weight * 0.45359237
    
    bmi = weight/(height ** 2)
    return bmi

if height > 0 and weight > 0:
    bmi = calculate_bmi(height, weight, height_unit, weight_unit)
    st.write("BMI: {:.2f}".format(bmi))
else:
    st.write("Please enter a valid height and weight.")