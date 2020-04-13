import enum

WORD_POOL = ["programming", "python", "mother"]

ATTEMPTS_COUNT = 5

class ReturnCodes(enum.Enum):
    NEW_GAME = 0
    SUCCESSFUL_TRY = 1
    UNSUCCESSFUL_TRY = 2
    WIN = 3
    LOSE = 4
    NOT_A_LETTER = 5
