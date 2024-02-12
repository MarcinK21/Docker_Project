# Wybierz obraz bazowy
FROM python:3.7-alpine

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Ustaw zmienną środowiskową na app.py, jako główna aplikacja
ENV FLASK_APP=app.py
# 0.0.0.0 pozwala na przyjmowanie połączeń z każdego adresu IP
ENV FLASK_RUN_HOST=0.0.0.0

# Zainstaluj zależności systemowe
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Skopiuj resztę kodu źródłowego aplikacji do kontenera
COPY . .

# Oznacz port, na którym będzie działać aplikacja
EXPOSE 5000

# Argumenty budowy do wersjonowania
ARG BUILD_VERSION=unknown
ENV BUILD_VERSION=${BUILD_VERSION}
RUN echo "Build version: ${BUILD_VERSION}"

# Uruchom aplikację
CMD ["flask", "run"]
