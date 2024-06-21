FROM python

EXPOSE 5000

WORKDIR /app
COPY .

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install -r requirements.txt

# Run
CMD ["flask", "run", "--port=5000", "--host=0.0.0.0"]