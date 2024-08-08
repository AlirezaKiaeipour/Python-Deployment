FROM python

WORKDIR /app

# Upgrade pip and install requirements
COPY . /app
RUN pip install Flask khayyam

EXPOSE 8082

ENV FLASK_APP = khayyam.py

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8082"]