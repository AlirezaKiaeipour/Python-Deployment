FROM python

WORKDIR /myapp

# Upgrade pip and install requirements
COPY requirements.txt /myapp
RUN pip install -r requirements.txt

EXPOSE 5000

# Run
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]