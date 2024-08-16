FROM python

WORKDIR /app

# Upgrade pip and install requirements
COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8000


# Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]