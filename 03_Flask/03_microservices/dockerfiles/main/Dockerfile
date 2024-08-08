FROM python

WORKDIR /app

# Upgrade pip and install requirements
COPY . /app
RUN pip install Flask

EXPOSE 8080

ENV FLASK_APP = main.py

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]