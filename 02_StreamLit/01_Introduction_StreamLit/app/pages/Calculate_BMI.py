import streamlit as st
from PIL import Image

st.title(":green[Calculate BMI]")

def calculate_bmi(Weight,height):
    bmi = weight / ((height/100)**2)
    if bmi < 18.5:
        bmi_text = "You Are UnderWeight"
        image_dir = "pages/img/under.png"

    elif 18.5<= bmi < 25:
        bmi_text = "You Are Normal"
        image_dir = "pages/img/normal.png"

    elif 25<= bmi < 30:
        bmi_text = "You Are OverWeight"
        image_dir = "pages/img/over.png"

    elif 30<= bmi < 35:
        bmi_text = "You Are Obese"
        image_dir = "pages/img/obese.png"

    elif 35<= bmi:
        bmi_text = "You Are Extremely Obese"
        image_dir = "pages/img/exobese.png"

    return bmi_text, image_dir


weight = st.number_input("Enter Your Weight (kg)")
height = st.number_input("Enter Your Height (cm)")
btn_bmi = st.button(":green[Calculate BMI]")
if btn_bmi:
    if weight and height is not None:
        text_bmi, image_dir,  = calculate_bmi(weight,height)
        st.info(text_bmi)

        image_bmi = Image.open(image_dir)
        st.columns(3)[1].image(image_bmi)
    else:
        st.error("Enter Your Weight & Height")  
    