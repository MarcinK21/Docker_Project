# Dokumentacja projektu aplikacji Flask z Redis

## Krótki opis

Projekt jest prostą aplikacją webową zbudowaną przy użyciu Flask, która wykorzystuje Redis do cache'owania danych.

Aplikacja pozwala na tworzenie list zadań oraz dodawanie i usuwanie zadań z tych list

## Jak ją uruchomić

1. Sklonowanie repozytorium projektu na lokalny komputer
2. docker-compose build  -> Zbudowanie obrazów Docker dla aplikacji Flask (Redis korzysta z obrazu bezpośrednio z Docker Hub)
3. docker-compose up -> uruchomienie kontenerów
4. Sprawdzenie działania aplikacji dostępnej pod adresem http://localhost:5000
5. docker exec -it <nazwa_kontenera_redis> redis-cli Połączenie z Redis za pomocą redis-cli
6. docker-compose down - zatrzymanie i usunięcie wszystkich kontenerów zdefiniowanych w docker-compose.yaml


## Struktura (opis komponentów)
* Aplikacja Flask (app.py) - Główna aplikacja backend
* Frontend (index.html) - Prosty interfejs
* Redis - używany jako system cache'owania do przechowywania list zadań
* Docker (Dockerfile i docker-compose.yaml) - konfiguracja konteneryzacji dla aplikacji Flask i Redis
* Kubernetes (w sekcji K8s)

## Opis kontenerów
Projekt wykorzystuje dwa kontenery Docker do uruchomienia aplikacji:
* kontener dla aplikacji Flask
Uruchamia aplikację webową Flask, która obsługuje logikę backendową, w tym obsługę żadań HTTP dla tworzenia list zadań, dodawania zadań do listy oraz pobierania i usuwania zadań. Aplikacja jest skonfigurowana do komunikacji z Redisem, który służy jako cache dla danych aplikacji

* kontener dla bazy danych Redis
uruchamia bazę danych Redis, która jest używana przez aplikację Flask jako system cache'owania. Redis Przechowuje listy zadań i dane zadań, umożliwiając szybki dostęp do często używanych danych i zmniejszając obciążenie aplikacji Flask


## Jak sprawdzić jej poprawne działanie - testowanie aplikacji
* Testowanie cache'owania Redis:
po uruchomieniu docker-compose należy wpisać w terminal:
docker exec -it <nazwa_kontenera_redis> redis-cli

<nazwa_kontener_redis> można skopiować po wpisaniu docker ps i skopiowania portu

Następnie sprawdzić czy dane są poprawnie cache'owane. Na przykład można sprawdzić:
* istnienie i wartośc klucza: Get nazwa_listy
* Testowanie wygaśnięcia: TTL nazwa_listy


# K8s
## Pliki k8s
* flask-deployment.yaml
* flask-serivce.yaml
* redis-deployment.yaml
* redis-service.yaml

## Jak uruchomić 
kubectl apply -f k8s/

## Weryfikacja czy wszystkie zasoby zostały pomyślnie utworzone
* kubectl get all

## Czyszczenie zasobów
Aby usunąc wdrożone zasoby Kubernetes:
* kebectl delete -f k8s/


## Dalszy rozwój
Stworzenie ConfigMaps i Secrets do zarządzania konfiguracjami i wrażliwymi danymi
