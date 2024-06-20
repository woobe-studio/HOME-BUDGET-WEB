# Użyj oficjalnego obrazu Pythona jako bazy
FROM python:3.8

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj pliki projektu do kontenera
COPY . .

# Zainstaluj zależności
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Ustaw zmienną środowiskową
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

# Uruchom aplikację
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
