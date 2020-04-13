# Chudo Game

## Что это?

В России абсолютно все люди просто без ума от игры "Поле Чудес". На протяжении часа гости говорят прекрасному мужчине-ведущему буквы, пытаясь угадать, какое же слово было загадано.

В связи с режимом повышенной готовности мы потеряли возможность поиграть так вживую. К счастью, на помощь к нам пришли инновации и высокие технологии.

## Как это работает?

Сервер для игры реализован с помощью веб-фреймворка `Flask`. В нашем случае на него возлагается всего две задачи:

1. Не забывать, с кем он играет
2. Собственно, играть, то есть обрабатывать запросы

Первая проблема в маленьких масштабах решается довольно просто: мы храним IP-адреса игроков и соответствующую игровую сессию `GameSession`. Если бы мы хотели вести глобальную таблицу игроков, то в игру бы вошли СУБД (для хранения данных для входа и достижений пользователей) и немного криптографии (мы же не хотим хранить пароли юзеров plaintext'ом), но, увы, не сегодня. Как только пользователь выиграл или проиграл, мы удаляем его сессию. Если он случайно вышел, он может снова подключиться и продолжить.

Вторая проблема довольно тривиальна. Введём систему кодов возврата `ReturnCode`, чтобы сервер говорил клиенту только то, что тот поймёт (в нашем случае просто по-разному будем уведомлять пользователя о результатах его действий). Кстати говоря, `ReturnCode` сделан `enum`'ом, чтобы мы случайно в коде не указали некорректное возвращаемое значение.

Работа клиента совершенно элементарна: с помощью библиотеки `requests` мы посылаем серверу `GET`-запросы, а затем обрабатываем данные `data` из ответа в соответствии с кодами возврата `result`.

Конфигурировать игру можно с помощью `server_config.py`, там есть как и ограничение на число попыток, так и возможность расширить пул слов. Пользователь же может себе поменять адрес игрового сервара (`GAME_URL` в `client.py`), если на предыдущем его забанили за DDoS.

## Как играть?

Поднять тестовый сервер на `localhost` можно так:

```
$ env FLASK_APP=server.py flask run
```

Играть начинаем вот так (заранее указав правильный `GAME_URL`):

```
$ python3 client.py
```

## Примеры игр

Если играть самому не хочется, можно посмотреть на логи ниже, чтобы прочувствовать атмосферу уюта "Поля Чудес":

Абсолютная победа:
```
You have started a new game! You have 5 attempts to guess a word ******
Guess a letter: m
You are really good at it, now word is m*****.
Guess a letter: o
You are really good at it, now word is mo****.
Guess a letter: t
You are really good at it, now word is mot***.
Guess a letter: h
You are really good at it, now word is moth**.
Guess a letter: e
You are really good at it, now word is mothe*.
Guess a letter: r
WOW YOU'RE SUCH A GUESSER! It really was "mother".
```

Абсолютный проигрыш:
```
You have started a new game! You have 5 attempts to guess a word ******
Guess a letter: a
Sorry, but you've failed. Only 4 attempts left.
Guess a letter: a
Sorry, but you've failed. Only 3 attempts left.
Guess a letter: a
Sorry, but you've failed. Only 2 attempts left.
Guess a letter: a
Sorry, but you've failed. Only 1 attempts left.
Guess a letter: a
That's not your day, sorry. The word was "python"
```

Переподключение:
```
You have started a new game! You have 5 attempts to guess a word ******
Guess a letter: a
Sorry, but you've failed. Only 4 attempts left.
Guess a letter: <Keyboard interrupt>
<Переподключение>
Wow, you can continue your game!
Guess a letter: y
Sorry, but you've failed. Only 3 attempts left.
Guess a letter: m
You are really good at it, now word is m*****.
Guess a letter: o
You are really good at it, now word is mo****.
Guess a letter: t
You are really good at it, now word is mot***.
Guess a letter: h
You are really good at it, now word is moth**.
Guess a letter: e
You are really good at it, now word is mothe*.
Guess a letter: r
WOW YOU'RE SUCH A GUESSER! It really was "mother".
```
