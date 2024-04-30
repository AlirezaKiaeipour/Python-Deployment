import streamlit as st
import numpy as np
import cv2
from PIL import Image


# def image_blured(image_file, degree_blurred):
#     image = Image.open(image_file)
#     image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
#     image = cv2.blur(image, (degree_blurred,degree_blurred))
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     image = Image.fromarray(image)
#     return image

# st.title(":blue[Image Blur]")

# image_file = st.file_uploader("Select Your Image",type=["png", "jpg", "jpeg"])

# if image_file is not None:
#     st.success("Image uploaded successfully")
#     col1, col2 = st.columns(2)
#     degree_blurred = st.slider("Degree of image Blur",min_value=1, max_value=99, value=21, step=2)

#     blurred_image = image_blured(image_file,degree_blurred)
#     orginal_image = Image.open(image_file)
#     with col1:
#         st.image(orginal_image,"Orginal Image")
#     with col2:
#         st.image(blurred_image, "Blurred Image")

# else:
#     st.warning("No image have been uploaded")
