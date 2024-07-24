# Personal Website

This is personal website and it was built using Flask

## Setup and Installation

* Install Dependencies:

  ```
  pip install -r requirements.txt
  ```

* Run

  ```
  flask run
  ```

## Docker

  ```bash
  docker pull postgres
  docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=db_postgres -d postgres
  ```

  ```bash
  docker build -t my_web .
  docker run --rm -p 5432:5432 -p 8080:5000 -v $(pwd):/myapp my_web
  ```

## Docker Network

  ```bash
  docker network create web_network
  ```
  ```bash
  docker build -t my_web .
  ```
  ```bash
  docker run --network web_network --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=db_postgres -d postgres
  ```
  ```bash
  docker run --rm --network web_network --name my_web -p 8080:5000 -v $(pwd):/myapp my_web
  ```

## Docker compose

  ```bash
  docker build -t my_web .
  ```
  ```bash
  docker compose up -d
  ```
  ```bash
  docker compose stop
  ```
  ```bash
  docker compose down
  ```
