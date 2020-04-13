import random
import server_config as config
import string
from flask import Flask, request

app = Flask(__name__)

def get_random_word():
    return random.choice(config.WORD_POOL)

class GameSession:
    def __init__(self, player_ip: str, attempts: int = config.ATTEMPTS_COUNT) -> None:
        self.player_ip = player_ip
        self.word = get_random_word()
        self.used_letters = set()
        self.attempts_left = attempts

    def try_letter(self, letter: str) -> bool:
        if letter not in self.used_letters and letter in set(self.word):
            self.used_letters.add(letter)

            return True

        self.attempts_left -= 1
        return False

    def is_solved(self) -> bool:
        return len(self.used_letters) == len(set(self.word))

    def get_hidden_word(self) -> str:
        temp = self.word
        for letter in string.ascii_lowercase:
            if letter not in self.used_letters:
                temp = temp.replace(letter, '*')

        return temp

current_games = {}

@app.route('/chudo')
def process_attempt():
    current_game = current_games.get(request.remote_addr)
    if current_game is not None:
        letter = request.args.get("letter", '')
        if len(letter) == 1 and letter.isalpha():
            suggestion_result = current_game.try_letter(letter)

            if suggestion_result and current_game.is_solved():
                del current_games[request.remote_addr]
                return {
                    "result": config.ReturnCodes.WIN.value,
                    "data": current_game.word
                }
    
            elif suggestion_result:
                return {
                    "result": config.ReturnCodes.SUCCESSFUL_TRY.value,
                    "data":current_game.get_hidden_word()
                }

            elif not suggestion_result and current_game.attempts_left != 0:
                return {
                    "result": config.ReturnCodes.UNSUCCESSFUL_TRY.value,
                    "data": current_game.attempts_left
                }

            elif current_game.attempts_left == 0:
                del current_games[request.remote_addr]
                return {
                    "result": config.ReturnCodes.LOSE.value,
                    "data": current_game.word
                }
        else:
            return {
                "result": config.ReturnCodes.NOT_A_LETTER.value,
                "data": letter
            }
    else:
        current_game = GameSession(request.remote_addr)
        current_games[request.remote_addr] = current_game
        return {
            "result": config.ReturnCodes.NEW_GAME.value,
            "data": current_game.get_hidden_word()
        }
