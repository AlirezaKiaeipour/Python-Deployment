FROM python

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app

# Upgrade pip and install requirements
COPY requirements.txt /app
RUN pip install -r requirements.txt

EXPOSE 8080

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]