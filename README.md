# what_what


## Jak uruchomić:

Będąc na przygotowanym serwerze albo u siebie na komputerze.

#### Pobierz:

```
cd /var/www
git clone https://github.com/ZPXD/what_what.git/
```

#### Uruchom środowisko:

```
python3 -m venv flagaenv
source flagaenv/bin/activate
```

#### Zainstaluj wymagane biblioteki:
```
pip3 install -r requirements.txt
```

#### Uruchom program:

```
export FLASK_APP=app.py
flask run
```

#### Oglądaj rezultaty w przeglądarce

#### A: na własnym kompie:

Po odpaleniu aplikacji wejdź na http://127.0.0.1:5000/

#### B: na serwerze:

Otwórz nowy terminal lub powershell będąc na swoim komputerze i wpisz:

za username -  wstaw nazwę użytkownika
za nazwa_klucza - nazwę klucza
za 1.1.1.1 – ip serwera
```
ssh -L 5000:localhost:80 -i nazwa_klucza username@1.1.1.1
```

I wejdź na http://127.0.0.1:5000/

#### 
