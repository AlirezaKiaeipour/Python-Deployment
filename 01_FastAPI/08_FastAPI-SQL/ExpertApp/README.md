# University System 

- University System Application Using FastAPI & SQLAlchemy
- This application is deployed on Docker and PostgreSQL database


## Installation


```
pip install -r requirements.txt

docker pull postgres

docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=PASSWORD -e POSTGRES_USER=USERNAME -e POSTGRES_DB=DATABASE_NAME -d postgres

# Change SQLAlchemy database url variable

SQLALCHEMY_DATABASE_URL = "postgresql://USERNAME:PASSWORD@localhost:5432/DATABASE_NAME"
```

## Run
You can run  Inference with the following command then copy the local IP in your browser

```
uvicorn app.main:app --reload
```

      
