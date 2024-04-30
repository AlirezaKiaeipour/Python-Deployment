FROM python

# Expose port you want your app on
EXPOSE 8501

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install opencv-python

# Copy app code and set working directory
COPY . .
WORKDIR /app

# Run
ENTRYPOINT ["streamlit", "run", "Home.py", "--server.port=8501", "--server.address=0.0.0.0"]