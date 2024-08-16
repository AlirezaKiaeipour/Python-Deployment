FROM python

WORKDIR /app

# Upgrade pip and install requirements
COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

EXPOSE 5000

ENV FLASK_APP = app.py

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]