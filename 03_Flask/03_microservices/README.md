# AI Web Application

## Overview

This is a web application that utilizes the models of DeepFace for face analysis and YOLO for object detection. And also this application utilizes BMR calculator for estimates basal metabolic rate.

## Features

* User Sign up and Login: Create an account and login to access personalized features.
* Cookie Manager: The cookie manager is used to manage user sessions and authenticate users.
* PostgreSQL: The web application uses a PostgreSQL database to store and retrieve user data.
* Face analysis using deepface package.
* Object detection using YOLO-V8.
* BMR calculator using Mifflin-St Jeor equation.
* Pose detection using mediapipe package.


## Setup and Installation

* Install Dependencies:

  ```bash
  pip install -r requirements.txt
  ```

* Run

  ```bash
  flask run
  ```
## Docker

  ```bash
  docker pull postgres
  docker run -p 5432:5432 --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=db_postgres -d postgres
  ```

  ```bash
  docker build -t ai_web_app .
  docker run --rm -p 5432:5432 -p 8080:5000 -v $(pwd):/myapp ai_web_app
  ```

## Docker Network

  ```bash
  docker network create ai_network
  ```
  ```bash
  docker build -t ai_web_app .
  ```
  ```bash
  docker run --network ai_network --name some-postgres -e POSTGRES_PASSWORD=password -e POSTGRES_USER=username -e POSTGRES_DB=db_postgres -d postgres
  ```
  ```bash
  docker run --rm --network ai_network --name ai_web_app -p 8080:5000 -v $(pwd):/myapp ai_web_app
  ```

## Docker compose

  ```bash
  docker build -t ai_web_app .
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
