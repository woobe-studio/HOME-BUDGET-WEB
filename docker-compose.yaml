version: '3.8'
services:
  db:
    image: postgres
    environment:
      POSTGRES_USER: ${DATABASE_USER}
      POSTGRES_PASSWORD: ${DATABASE_PASSWORD}
      POSTGRES_DB: ${DATABASE_NAME}
    ports:
      - "${DATABASE_PORT}:5432"
  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_TYPE: ${DATABASE_TYPE}
      DATABASE_HOST: ${DATABASE_HOST}
      DATABASE_PORT: ${DATABASE_PORT}
      DATABASE_USER: ${DATABASE_USER}
      DATABASE_PASSWORD: ${DATABASE_PASSWORD}
      DATABASE_NAME: ${DATABASE_NAME}
      SMTP_HOST: ${SMTP_HOST}
      SMTP_PORT: ${SMTP_PORT}
      SMTP_USER: ${SMTP_USER}
      SMTP_PASSWORD: ${SMTP_PASSWORD}
      SOCIAL_AUTH_GITHUB_KEY: ${SOCIAL_AUTH_GITHUB_KEY}
      SOCIAL_AUTH_GITHUB_SECRET: ${SOCIAL_AUTH_GITHUB_SECRET}
      SOCIAL_AUTH_GOOGLE_OAUTH2_KEY: ${SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}
      SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET: ${SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET}
    env_file:
      - .env
