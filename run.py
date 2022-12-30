import random
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('wheel-of-fortune')

GUESSED_LETTERS = []
VOWELS = ["a", "e", "i", "o", "u"]
PLAYER1 = ""
PLAYER2 = ""
PLAYER1CASH = 0
PLAYER2CASH = 0
WHEEL = ["Bankrupt", 600, 400, 300, "Pass your turn",
         800, 350, 450, 700, 300, 600, 5000, 600, 500, 300, 500,
         800, 550, 400, 300, 900, 500, 300, 900]

title = SHEET.worksheet('title')
data = title.get_all_values()


def play_game():
    """
    The function opens the game.
    """
    print("Hello and welcome to the Wheel ... of ...  Fortuuuuuune!")
    print("\n")
    print("My Name is Mr Boty and I will be your host")
    print("\n")    
    print("The rules are simple:")
    print("\n")
    print("Turn the wheel to get a cash value and guess a consonent.")
    print("\n")
    print("The cash value will be multiplied by the number of consonent")
    print("found in the mystery sentence and will be added to your jackpot.")
    print("\n")
    print("After guessing a correct consonent, you will be able to either:")
    print("a - buy a Vowel for 250$")
    print("b - guess the mystery sentence")
    print("\n")
    print("You will pass your turn if:")
    print("a - your consonent is not in the mystery sentence")   
    print("b - you guess incorrecty the mystery sentence")
    print("c - you fall on the 'Pass your turn' case in the wheel")
    print("d - you fall on the 'Bankrupt' case in the wheel in which case")
    print("you also lose all your earnings. OUCH!! THOUGH LUCK!")
    print("\n")


def select_row():
    """
    The function selects randomly a row in the google 
    worksheet called "title" and creates a quote 
    said by Mr Boty and the sentence to guess in the turn.
    """
    row = random.choice(list(data))
    sentence = row[0]
    print(f"In the '{row[4]}' category.\n")
    print(f"The guess contains {row[1]} words and {row[2]} letters.\n")
    print("Take it away!")
    print(sentence)
    return sentence


def convert_letter(sentence):
    """
    The function turns each letter of the sentence 
    created in the function in an underscore and therefore
    creates the guess users will try to solve.
    The function is inspired by Hayley Guillou on stack overflow 
    https://stackoverflow.com/questions/32960141/how-can-i-replace-the-letters-of-a-string-with-underscores
    """
    guess = sentence
    for i in range(0, len(sentence)):
        if ord(sentence[i]) != 32:
            guess = guess.replace(sentence[i], '_ ')
    print(guess)


def main():
    play_game()
    convert_letter(select_row())


main()
