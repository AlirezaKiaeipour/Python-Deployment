import streamlit as st
import pandas as pd

def convert_to_dataframe(file):
    df = pd.read_csv(file)
    data = df[["Date","Close"]]
    data["Date"] = pd.to_datetime(data["Date"])
    return df, data


st.title(":blue[Uber Stock]")
st.header("")

st.sidebar.title("About")
st.sidebar.write("Uber is transportation company that provides ride-hailing services, courier services, food delivery, and freight transport.")
st.sidebar.write("This is a simple app for Uber stock and  you can view Uber stock details.")

uploaded_file = st.file_uploader("Upload your csv file", type=["csv"])

if uploaded_file is not None:
    st.success("File uploaded successfully")
    st.header("")
    df, data = convert_to_dataframe(uploaded_file)
    st.write(df)    
    st.line_chart(data, x="Date", y="Close", color="#ffaa0088")
     
else:
    st.warning("No file have been uploaded")
