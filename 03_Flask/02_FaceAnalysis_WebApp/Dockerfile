FROM python

# Expose port you want your app on
EXPOSE 5000

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY . .
WORKDIR .

# Run
ENTRYPOINT ["flask", "run", "--port=5000", "--host=0.0.0.0"]