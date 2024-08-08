FROM python

WORKDIR /app

# Upgrade pip and install requirements
COPY . /app
RUN pip install Flask hafez

EXPOSE 8081

ENV FLASK_APP = hafez.py

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8081"]