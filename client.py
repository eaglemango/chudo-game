import enum
import requests

class ReturnCodes(enum.Enum):
    NEW_GAME = 0
    SUCCESSFUL_TRY = 1
    UNSUCCESSFUL_TRY = 2
    WIN = 3
    LOSE = 4
    NOT_A_LETTER = 5

GAME_URL = "http://127.0.0.1:5000/chudo"

if __name__ == "__main__":
    response = requests.get(GAME_URL).json()
    if response['result'] == ReturnCodes.NEW_GAME.value:
        print("You have started a new game! You have 5 attempts to guess a word %s" % response['data'])
    else:
        print("Wow, you can continue your game!")

    while True:
        letter = input("Guess a letter: ")
        response = requests.get(GAME_URL + "?letter=" + letter).json()

        if response['result'] == ReturnCodes.SUCCESSFUL_TRY.value:
            print("You are really good at it, now word is %s." % response['data'])
        elif response['result'] == ReturnCodes.UNSUCCESSFUL_TRY.value:
            print("Sorry, but you've failed. Only %d attempts left." % response['data'])
        elif response['result'] == ReturnCodes.WIN.value:
            print("WOW YOU'RE SUCH A GUESSER! It really was \"%s\"." % response['data'])
            exit(0)

        elif response['result'] == ReturnCodes.LOSE.value:
            print("That's not your day, sorry. The word was \"%s\"" % response['data'])
            exit(0)

        elif response['result'] == ReturnCodes.NOT_A_LETTER.value:
            print("Do you really think I can accept \"%s\" as a word?" % response['data'])
