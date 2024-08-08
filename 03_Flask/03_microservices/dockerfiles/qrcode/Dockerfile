FROM python

WORKDIR /app

# Upgrade pip and install requirements
COPY . /app
RUN pip install Flask qrcode

EXPOSE 8083

ENV FLASK_APP = qr_code.py

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8083"]